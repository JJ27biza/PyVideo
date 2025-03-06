import shutil
import os
class AddArchiveDirectory():
    #Este método verifica si existe la ruta y si existe copia el archivo al directorio destino
    def functionAddArchiveDirectory(self,url, destination_path):
        try:
            if not os.path.exists(url):
                print(f"El archivo en {url} no existe.")
                return

            shutil.copy(url, destination_path)
        except Exception as error:
            print('Error en el copiado de video ',error)