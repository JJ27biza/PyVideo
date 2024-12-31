class ModificText():
    def functionDeleteText(self, text):
        try:
            if text:
                texto = text.replace("Archivo seleccionado: ", "")
                return texto
            else:
                print("El texto proporcionado está vacío.")
                return text
        except Exception as error:
            print(f"Error al borrar texto: {error}")
            return ''
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