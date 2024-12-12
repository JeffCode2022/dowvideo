# app.py
from flask import Flask, render_template, request, send_file
import yt_dlp
import os
from urllib.parse import urlparse
import time
import shutil


app = Flask(__name__)

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False

def download_video(url, output_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'extract_flat': False,
        'quiet': True,
        'no_warnings': True,
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Obtener información del video primero
            info = ydl.extract_info(url, download=False)
            # Descargar el video
            ydl.download([url])
            
            # Una vez descargado, movemos el archivo a un lugar accesible
            video_filename = os.path.join(output_path, f"{info['title']}.{info['ext']}")
            
            # Asegurarse de que el archivo existe
            if os.path.exists(video_filename):
                return {
                    'success': True,
                    'video_file': video_filename,  # Retornar la ruta del video
                    'message': 'Video descargado exitosamente'
                }
            else:
                return {
                    'success': False,
                    'message': 'No se pudo encontrar el archivo descargado.'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error al descargar el video: {str(e)}'
            }

@app.route('/', methods=['GET', 'POST'])
def home():
    message = ""
    status = ""
    if request.method == 'POST':
        link = request.form['link']
        
        if not is_valid_url(link):
            message = "Por favor, ingresa una URL válida"
            status = "error"
        else:
            output_path = "downloads"
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            
            result = download_video(link, output_path)
            message = result['message']
            status = 'success' if result['success'] else 'error'
    
    return render_template('index.html', message=message, status=status)

if __name__ == '__main__':
    app.run(debug=True)