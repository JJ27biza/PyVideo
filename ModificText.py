class ModificText():
    #Metodo para borrar el texto en la seleccion del video en el directorio
    def functionDeleteText(self, text):
        try:
            if text:
                texto = text.replace("Archivo seleccionado: ", "")
                return texto
            else:
                return text
        except Exception as error:
            print(f"Error al borrar texto: {error}")
            return ''
        #Metodo para validar la url
    def functionValidationUrl(self,text):
        try:
            if text:
                texto = text.replace('\\', "/")
                return texto
            else:
                print("El texto proporcionado está vacío.")
                return text
        except Exception as error:
            print(f"Error al replazar texto: {error}")
            return ''