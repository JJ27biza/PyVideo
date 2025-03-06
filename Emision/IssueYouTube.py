import time
import pychromecast
from pychromecast.controllers.youtube import YouTubeController

#Este método permite la emisión de del video de youtube por url y por nombre de chromecast
def emit_in_yt(video_url,nombre_chromecast):
    try:
        chromecasts, browser = pychromecast.get_chromecasts()

        if not chromecasts:
            print("No se encontraron dispositivos Chromecast.")
            exit()

        chromecast = None
        for cast in chromecasts:
            if cast.name == nombre_chromecast:
                chromecast = cast
                break

        if chromecast is None:
            print(f"No se encontró un dispositivo Chromecast con el nombre: {nombre_chromecast}")
            exit()

        chromecast.wait()

        yt_controller = YouTubeController()

        chromecast.register_handler(yt_controller)

        yt_controller.play_video(video_url)


    except Exception as error:
        print(error)




