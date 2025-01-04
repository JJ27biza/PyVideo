import os

class AddCreateVideoStore():

    def functionCreateVideoStore(self):
        try:
            if not os.path.exists('../VideoStore'):
                os.mkdir('../VideoStore')
                return True
        except Exception as error:
            print('Error al crear VideoStore',error)