import time
import pychromecast

#Método que se conecta al chromecast por el nombre
def conectar_chromecast(nombre_dispositivo):
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[nombre_dispositivo])

    if chromecasts:
        cast = chromecasts[0]
        cast.wait()
        print(f"Conectado a {nombre_dispositivo}")
        return cast
    else:
        print(f"No se encontró un dispositivo con el nombre {nombre_dispositivo}")
        return None

#Método que se desconecta del chromecast
def desconectar_chromecast(cast):
    if cast:
        cast.quit_app()
        print(f"Desconectado de {cast.name}")

#Método que se conecta por el nombre espera 5 segundos y se desconecta
def desconexion_total(nombre_dispositivo):

    cast = conectar_chromecast(nombre_dispositivo)

    time.sleep(5)

    desconectar_chromecast(cast)
