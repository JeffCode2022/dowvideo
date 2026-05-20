# app.py
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
from urllib.parse import urlparse
import time
import re

app = Flask(__name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            
            # Format duration to MM:SS
            duration_raw = info.get('duration')
            duration = "Desconocida"
            if duration_raw:
                mins, secs = divmod(int(duration_raw), 60)
                duration = f"{mins:02d}:{secs:02d}"
            
            # Extract available formats
            formats = info.get('formats', [])
            available_options = []
            
            # 1. Video Options
            # We want standard resolutions: 1080, 720, 480, 360
            for res in [1080, 720, 480, 360]:
                # Check if there is any format at this resolution
                res_formats = [f for f in formats if f.get('height') == res]
                if res_formats:
                    # Find format with highest size or bitrate
                    best_vf = max(res_formats, key=lambda x: x.get('filesize') or x.get('filesize_approx') or 0, default=None)
                    
                    size_str = "Desconocido"
                    if best_vf:
                        v_size = best_vf.get('filesize') or best_vf.get('filesize_approx') or 0
                        # Get best audio size to add to the total estimation
                        audio_formats = [f for f in formats if f.get('vcodec') == 'none']
                        best_af = max(audio_formats, key=lambda x: x.get('filesize') or x.get('filesize_approx') or 0, default=None)
                        a_size = (best_af.get('filesize') or best_af.get('filesize_approx') or 0) if best_af else 0
                        
                        total_size = v_size + a_size
                        if total_size > 0:
                            size_mb = total_size / (1024 * 1024)
                            size_str = f"{size_mb:.1f} MB"
                    
                    available_options.append({
                        'id': f'video_{res}',
                        'type': 'video',
                        'label': f'Video MP4 ({res}p)',
                        'quality': f'{res}p',
                        'ext': 'mp4',
                        'size': size_str
                    })
            
            # If no standard resolutions were found, add the best available video combined
            if not any(opt['type'] == 'video' for opt in available_options):
                available_options.append({
                    'id': 'video_best',
                    'type': 'video',
                    'label': 'Video MP4 (Mejor calidad)',
                    'quality': 'Original',
                    'ext': 'mp4',
                    'size': 'Estimado 15-40 MB'
                })
            
            # 2. Audio Options
            # We estimate audio sizes based on duration (192kbps and 320kbps)
            duration_raw = info.get('duration') or 0
            
            size_320_str = "Desconocido"
            size_192_str = "Desconocido"
            size_native_str = "Desconocido"
            
            if duration_raw > 0:
                # 320kbps = 40 KB/s
                size_320 = duration_raw * 40 * 1024
                size_320_str = f"{size_320 / (1024*1024):.1f} MB"
                # 192kbps = 24 KB/s
                size_192 = duration_raw * 24 * 1024
                size_192_str = f"{size_192 / (1024*1024):.1f} MB"
            
            # Find native audio format size
            audio_formats = [f for f in formats if f.get('vcodec') == 'none']
            best_af = max(audio_formats, key=lambda x: x.get('filesize') or x.get('filesize_approx') or 0, default=None)
            if best_af:
                a_size = best_af.get('filesize') or best_af.get('filesize_approx') or 0
                if a_size > 0:
                    size_native_str = f"{a_size / (1024*1024):.1f} MB"
            
            available_options.append({
                'id': 'audio_mp3_320',
                'type': 'audio',
                'label': 'Audio MP3 (Alta Calidad - 320kbps)',
                'quality': '320 kbps',
                'ext': 'mp3',
                'size': size_320_str
            })
            available_options.append({
                'id': 'audio_mp3_192',
                'type': 'audio',
                'label': 'Audio MP3 (Estándar - 192kbps)',
                'quality': '192 kbps',
                'ext': 'mp3',
                'size': size_192_str
            })
            available_options.append({
                'id': 'audio_m4a',
                'type': 'audio',
                'label': 'Audio M4A (Formato Nativo)',
                'quality': 'Nativo',
                'ext': 'm4a',
                'size': size_native_str if size_native_str != "Desconocido" else "2-5 MB"
            })
            
            return {
                'success': True,
                'title': info.get('title', 'Video'),
                'thumbnail': info.get('thumbnail', ''),
                'uploader': info.get('uploader') or info.get('channel', 'Desconocido'),
                'duration': duration,
                'options': available_options,
                'original_url': url
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al obtener información: {str(e)}'
            }

def download_media(url, option_id):
    output_dir = os.path.join(os.path.dirname(__file__), 'downloads')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Clean up files older than 10 minutes (600 seconds)
    now = time.time()
    for f in os.listdir(output_dir):
        fpath = os.path.join(output_dir, f)
        if os.path.isfile(fpath):
            if now - os.path.getmtime(fpath) > 600:
                try:
                    os.remove(fpath)
                except Exception as e:
                    print(f"Error removing old file {fpath}: {e}")
    
    unique_suffix = int(time.time())
    
    # Check option and configure format downloads
    if option_id.startswith('convert_'):
        # Parse custom conversion: convert_video_webm_1080 or convert_audio_flac_320
        parts = option_id.split('_')
        media_type = parts[1]      # 'video' or 'audio'
        target_ext = parts[2]      # 'mp4', 'webm', 'mkv', 'avi', 'mp3', 'wav', 'flac', 'aac', 'ogg'
        quality = parts[3]         # '1080', '720', '320', etc.
        
        if media_type == 'video':
            ydl_opts = {
                'format': f'bestvideo[height<={quality}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={quality}]+bestaudio/best[height<={quality}]/best',
                'outtmpl': os.path.join(output_dir, f'%(title)s_{unique_suffix}.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': target_ext,
                }],
                'quiet': True,
                'no_warnings': True,
            }
        else:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': os.path.join(output_dir, f'%(title)s_{unique_suffix}.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': target_ext,
                    'preferredquality': quality,
                }],
                'quiet': True,
                'no_warnings': True,
            }
    elif option_id.startswith('video_'):
        res = option_id.split('_')[1]
        if res == 'best':
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': os.path.join(output_dir, f'%(title)s_{unique_suffix}.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
        else:
            ydl_opts = {
                'format': f'bestvideo[height<={res}][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height<={res}]+bestaudio/best[height<={res}]/best',
                'outtmpl': os.path.join(output_dir, f'%(title)s_{unique_suffix}.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }
    elif option_id == 'audio_mp3_320':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, f'%(title)s_{unique_suffix}.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'quiet': True,
            'no_warnings': True,
        }
    elif option_id == 'audio_mp3_192':
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_dir, f'%(title)s_{unique_suffix}.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
        }
    elif option_id == 'audio_m4a':
        ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': os.path.join(output_dir, f'%(title)s_{unique_suffix}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': os.path.join(r'C:\Program Files\ffmpeg\bin', 'ffmpeg.exe'),
        }
    else: # Default
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
            'outtmpl': os.path.join(output_dir, f'%(title)s_{unique_suffix}.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'ffmpeg_location': os.path.join(r'C:\Program Files\ffmpeg\bin', 'ffmpeg.exe'),
        }
        
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=True)
            downloaded_file = None
            for f in os.listdir(output_dir):
                if f"_{unique_suffix}." in f:
                    downloaded_file = os.path.join(output_dir, f)
                    break
            
            if downloaded_file and os.path.exists(downloaded_file):
                return {
                    'success': True,
                    'file_path': downloaded_file,
                    'filename': os.path.basename(downloaded_file),
                    'title': info.get('title', 'video')
                }
            else:
                return {
                    'success': False,
                    'message': 'No se pudo encontrar el archivo descargado'
                }
        except Exception as e:
            # Fallback for audio conversions if ffmpeg is missing
            if 'audio_mp3_' in option_id:
                try:
                    ydl_opts_fallback = {
                        'format': 'bestaudio/best',
                        'outtmpl': os.path.join(output_dir, f'%(title)s_{unique_suffix}.%(ext)s'),
                        'quiet': True,
                        'no_warnings': True,
                        'ffmpeg_location': os.path.join(r'C:\Program Files\ffmpeg\bin', 'ffmpeg.exe'),
                    }
                    with yt_dlp.YoutubeDL(ydl_opts_fallback) as ydl_fb:
                        info = ydl_fb.extract_info(url, download=True)
                        downloaded_file = None
                        for f in os.listdir(output_dir):
                            if f"_{unique_suffix}." in f:
                                downloaded_file = os.path.join(output_dir, f)
                                break
                        if downloaded_file and os.path.exists(downloaded_file):
                            return {
                                'success': True,
                                'file_path': downloaded_file,
                                'filename': os.path.basename(downloaded_file),
                                'title': info.get('title', 'audio')
                            }
                except Exception as fallback_err:
                    return {
                        'success': False,
                        'message': f'Error en descarga y fallback de audio: {str(fallback_err)}'
                    }
            return {
                'success': False,
                'message': f'Error al descargar: {str(e)}'
            }

@app.route('/')
def home():
    return send_file(os.path.join(os.path.dirname(__file__), 'templates', 'index.html'))

@app.route('/converter')
def converter():
    return send_file(os.path.join(os.path.dirname(__file__), 'templates', 'converter.html'))

@app.route('/get_info', methods=['POST'])
def get_info():
    data = request.get_json() or {}
    url = data.get('url')
    if not url or not is_valid_url(url):
        return jsonify({'success': False, 'message': 'Por favor, ingresa una URL válida'}), 400
    
    result = get_video_info(url)
    if not result['success']:
        return jsonify(result), 400
    return jsonify(result)

@app.route('/download', methods=['POST'])
def download():
    data = request.get_json() or {}
    url = data.get('url')
    option_id = data.get('option_id', 'video_best')
    
    if not url or not is_valid_url(url):
        return jsonify({'success': False, 'message': 'Por favor, ingresa una URL válida'}), 400
    
    result = download_media(url, option_id)
    if not result['success']:
        return jsonify(result), 400
    return jsonify(result)

@app.route('/serve_file/<filename>')
def serve_file(filename):
    filename = os.path.basename(filename)
    output_dir = os.path.join(os.path.dirname(__file__), 'downloads')
    file_path = os.path.join(output_dir, filename)
    
    if not os.path.exists(file_path):
        return "El archivo no existe o ya ha expirado.", 404
        
    name, ext = os.path.splitext(filename)
    if '_' in name:
        parts = name.split('_')
        if parts[-1].isdigit():
            original_name = '_'.join(parts[:-1]) + ext
        else:
            original_name = filename
    else:
        original_name = filename
    
    # Sanitizar el nombre del archivo de salida para evitar problemas con cabeceras HTTP
    original_name = re.sub(r'[^\w\-\.\(\)\s]', '', original_name)
    if not original_name:
        original_name = f"download{ext}"
        
    return send_file(file_path, as_attachment=True, download_name=original_name)

if __name__ == '__main__':
    app.run(debug=True)