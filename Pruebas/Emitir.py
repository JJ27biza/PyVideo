import os
import time
import pychromecast
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer
import threading
import requests  # Para verificar si la URL está accesible


# Iniciar un servidor HTTP simple para servir el video local
def start_http_server(port=8000):
    os.chdir('../VideoStore')  # Cambiar al directorio donde está el video
    handler = SimpleHTTPRequestHandler
    httpd = TCPServer(("", port), handler)
    print(f"Servidor HTTP iniciado en el puerto {port}")
    httpd.serve_forever()


# Verificar si la URL es accesible antes de emitir
def is_url_accessible(url):
    try:
        response = requests.get(url)
        return response.status_code == 200  # Retorna True si la URL es accesible
    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL: {e}")
        return False


# Función para emitir el video a Chromecast (y a dispositivos Android con Google Cast)
def cast_video_to_device(video_url):
    # Verificar si la URL es accesible
    if not is_url_accessible(video_url):
        print(f"La URL {video_url} no es accesible. No se puede emitir el video.")
        return

    # Encuentra los dispositivos Google Cast disponibles (Chromecast y dispositivos Android compatibles)
    chromecasts = pychromecast.get_chromecasts()

    # Si hay dispositivos disponibles, elige el primero de la lista
    if chromecasts:
        cast = chromecasts[0]  # Seleccionamos el primer dispositivo de la lista
        cast.wait()  # Esperamos a que el dispositivo esté listo

        # Obtener el controlador de medios del dispositivo y preparar la transmisión
        mc = cast.media_controller
        mc.play_media(video_url, 'video/mp4')
        mc.block_until_active()

        # Reproducir el video
        print("Reproduciendo video en el dispositivo...")
        mc.play()
    else:
        print("No se encontraron dispositivos Google Cast disponibles.")


if __name__ == "__main__":
    # Empezar el servidor HTTP en un hilo para poder servir el video
    video_filename = 'LockBoxAndroid.mp4'  # Nombre del archivo de video
    video_url = f'http://localhost:8000/{video_filename}'  # URL para emitir al dispositivo

    # Hacer que el servidor corra en un hilo para no bloquear el proceso
    server_thread = threading.Thread(target=start_http_server)
    server_thread.daemon = True
    server_thread.start()

    # Pausar un momento para que el servidor HTTP se inicie
    time.sleep(2)

    # Emitir el video al dispositivo
    cast_video_to_device(video_url)


