import time
import pychromecast
from pychromecast.controllers.youtube import YouTubeController

# URL del video de YouTube
video_url = 'h5oEPfkcAQg'

# Descubre los dispositivos Chromecast disponibles en la red
chromecasts, browser = pychromecast.get_chromecasts()

# Verifica que se hayan encontrado dispositivos Chromecast
if not chromecasts:
    print("No se encontraron dispositivos Chromecast.")
    exit()

# Conectar al primer Chromecast encontrado
chromecast = chromecasts[0]
print(f"Conectando al dispositivo: {chromecast.name}")
chromecast.wait()

# Obtener el controlador de YouTube
yt_controller = YouTubeController()

# Vincula el controlador de YouTube con el Chromecast
chromecast.register_handler(yt_controller)

# Inicia la reproducción del video de YouTube
print("Reproduciendo el video en YouTube...")
yt_controller.play_video(video_url)

# Espera a que el video esté listo para reproducirse
start_time = time.time()


