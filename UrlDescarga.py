import requests
import os


#Metodo que descarga el video que se para por url y se almacena en Desktop
def descargar_archivo(url):
    try:
        ruta_guardado = os.path.expanduser('~\Desktop\descargado.mp4')
        response = requests.get(url)

        if response.status_code == 200:
            with open(ruta_guardado, 'wb') as file:
                file.write(response.content)
        else:
            print(f"Error al descargar el archivo. Código de estado: {response.status_code}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")




