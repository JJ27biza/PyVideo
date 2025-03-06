import pyvolume


class ActionSound:
    #Este método cambia el volumen del dispositivo
    def functionControlSound(self,value):
        try:
            pyvolume.custom(percent=int(value))
        except Exception as error:
            print('Error al cambiar el volumen',error)