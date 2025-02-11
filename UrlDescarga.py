import requests
import os



def descargar_archivo(url):
    try:
        ruta_guardado = os.path.expanduser('~\Desktop\descargado.mp4')
        # Realizar la solicitud HTTP GET para obtener el archivo
        response = requests.get(url)

        # Verificar que la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            # Abrir un archivo en modo de escritura binaria y guardar el contenido
            with open(ruta_guardado, 'wb') as file:
                file.write(response.content)
            print(f"Archivo descargado y guardado como: {ruta_guardado}")
        else:
            print(f"Error al descargar el archivo. Código de estado: {response.status_code}")

    except Exception as e:
        print(f"Ocurrió un error: {e}")




