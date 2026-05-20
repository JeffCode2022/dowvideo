import requests
import json
import sys

def test_server():
    base_url = "http://127.0.0.1:5000"
    
    # Test homepage
    print("Probando GET / ...")
    try:
        r = requests.get(base_url)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Página principal cargada exitosamente!")
            print(f"Longitud del HTML: {len(r.text)} bytes")
        else:
            print(f"Error cargando la página principal: {r.text[:200]}")
            sys.exit(1)
    except Exception as e:
        print(f"No se pudo conectar al servidor: {e}")
        sys.exit(1)

    # Test /get_info with a sample video URL
    test_video_url = "https://www.youtube.com/watch?v=aqz-KE-bpKQ" # Un video corto/estándar de ejemplo
    print(f"\nProbando POST /get_info con {test_video_url} ...")
    try:
        r = requests.post(f"{base_url}/get_info", json={"url": test_video_url})
        print(f"Status: {r.status_code}")
        data = r.json()
        if data.get('success'):
            print("Información del video extraída exitosamente!")
            print(f"Título: {data.get('title')}")
            print(f"Creador: {data.get('uploader')}")
            print(f"Duración: {data.get('duration')}")
            print("Formatos disponibles:")
            for opt in data.get('options', []):
                print(f" - [{opt['id']}] {opt['label']} (Peso: {opt['size']})")
            
            # Test /download with the first audio option
            audio_option = next((opt for opt in data.get('options', []) if opt['type'] == 'audio'), None)
            if audio_option:
                print(f"\nProbando POST /download con opción {audio_option['id']} ...")
                r_dl = requests.post(f"{base_url}/download", json={"url": test_video_url, "option_id": audio_option['id']})
                print(f"Status: {r_dl.status_code}")
                dl_data = r_dl.json()
                if dl_data.get('success'):
                    print("Descarga/Conversión completada exitosamente en el servidor!")
                    print(f"Archivo generado: {dl_data.get('filename')}")
                    
                    # Test downloading the file
                    serve_url = f"{base_url}/serve_file/{dl_data.get('filename')}"
                    print(f"Probando descargar el archivo desde {serve_url} ...")
                    r_file = requests.get(serve_url)
                    print(f"Status: {r_file.status_code}")
                    if r_file.status_code == 200:
                        print(f"Archivo descargado exitosamente! Tamaño: {len(r_file.content)} bytes")
                    else:
                        print("Error al descargar el archivo físico.")
                else:
                    print(f"Error al descargar: {dl_data.get('message')}")
            else:
                print("No se encontraron opciones de audio para probar la descarga.")
        else:
            print(f"Error al obtener información: {data.get('message')}")
    except Exception as e:
        print(f"Error durante las pruebas de la API: {e}")

if __name__ == "__main__":
    test_server()
