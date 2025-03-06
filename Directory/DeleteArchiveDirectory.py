import os
class DeleteArchiveDirectory():
    #Este método permite borrar el archivo en la ruta indicada
    def functionDeleteArchive(self,ruta):
        try:
            if os.path.exists(ruta):
                os.remove(ruta)
            else:
                print("El archivo no existe")


        except Exception as error:
            print('Error al borrar el archivo',error)