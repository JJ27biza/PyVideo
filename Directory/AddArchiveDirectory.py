import shutil
import os
class AddArchiveDirectory():
    def functionAddArchiveDirectory(self,url, destination_path):
        try:
            # Verificar si el archivo existe en la ruta de origen
            if not os.path.exists(url):
                print(f"El archivo en {url} no existe.")
                return

            # Copiar el archivo al directorio de destino
            shutil.copy(url, destination_path)
            print(f"Archivo copiado correctamente de {url} a {destination_path}")
        except Exception as error:
            print('Error en el copiado de video ',error)