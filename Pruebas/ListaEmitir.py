import pychromecast
from PyQt6.sip import array


def listar_chromecasts():
    # Intentar descubrir los dispositivos Chromecast en la red
    chromecasts, browser = pychromecast.get_chromecasts()

    if chromecasts:
        print("Dispositivos Chromecast disponibles:")
        array=[]
        for idx, cast in enumerate(chromecasts):
            print(f"{idx + 1}. {cast.name}" )
            array.append(cast.name)
        return array
    else:
        print("No se encontraron dispositivos Chromecast en la red.")

if __name__ == "__main__":
    listar_chromecasts()
