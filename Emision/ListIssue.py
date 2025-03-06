import pychromecast
from PyQt6.sip import array

#Método que busca todo los dispositivos chromecast disponibles
def listar_chromecasts():
    chromecasts, browser = pychromecast.get_chromecasts()

    if chromecasts:
        array=[]
        for idx, cast in enumerate(chromecasts):
            print(f"{idx + 1}. {cast.name}" )
            array.append(cast.name)
        return array
    else:
        print("No se encontraron dispositivos Chromecast en la red.")


