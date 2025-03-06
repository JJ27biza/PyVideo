import os

class AddCreateVideoStore():
    #Este metodo permite crear directorios en la aplicacion
    def functionCreateVideoStore(self,name):
        try:
            if not os.path.exists('../'+name):
                os.mkdir('../'+name)
                return True
        except Exception as error:
            print('Error al crear VideoStore',error)