import pyvolume


class ActionSound:
    def functionControlSound(self,value):
        try:
            pyvolume.custom(percent=int(value))
        except Exception as error:
            print('Error al cambiar el volumen',error)