import os
class DeleteArchiveDirectory():
    def functionDeleteArchive(self,ruta):
        try:
            if os.path.exists(ruta):
                os.remove(ruta)
                print("El archivo ha sido eliminado")
            else:
                print("El archivo no existe")


        except Exception as error:
            print('Error al borrar el archivo',error)