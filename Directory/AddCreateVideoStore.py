import os

class AddCreateVideoStore():

    def functionCreateVideoStore(self,name):
        try:
            if not os.path.exists('../'+name):
                os.mkdir('../'+name)
                return True
        except Exception as error:
            print('Error al crear VideoStore',error)