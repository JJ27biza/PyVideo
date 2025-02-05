import time
import pychromecast
from pychromecast.controllers.youtube import YouTubeController


def emit_in_yt(video_url,nombre_chromecast):
    try:
        # Descubre los dispositivos Chromecast disponibles en la red
        chromecasts, browser = pychromecast.get_chromecasts()

        # Verifica que se hayan encontrado dispositivos Chromecast
        if not chromecasts:
            print("No se encontraron dispositivos Chromecast.")
            exit()

        # Buscar el Chromecast por nombre
        chromecast = None
        for cast in chromecasts:
            if cast.name == nombre_chromecast:
                chromecast = cast
                break

        if chromecast is None:
            print(f"No se encontró un dispositivo Chromecast con el nombre: {nombre_chromecast}")
            exit()

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



    except Exception as error:
        print(error)




