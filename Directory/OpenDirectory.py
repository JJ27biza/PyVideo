from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.label import Label
from kivy.core.window import Window



class OpenDirectory(App):
#Este metodo construye la parte gráfica para seleccionar el video que queremos añadir
    def build(self):
        Window.clearcolor = (0.2, 0.3, 0.4, 1)
        self.title = 'PyVideo'
        self.box = BoxLayout(orientation='vertical')
        self.filechooser = FileChooserIconView()
        self.filechooser.bind(selection=self.on_file_select)

        self.label = Label(text="Seleccione un archivo")

        self.box.add_widget(self.filechooser)
        self.box.add_widget(self.label)

        self.filechooser.filters = ['*.mp4', '*.avi', '*.mkv', '*.mp3']

        self.filechooser.show_hidden = True

        return self.box
    #Cambia el texto para saber el video que seleccionamos
    def on_file_select(self, instance, value):
        try:

            if value:
                selected_file = value[0]
                self.label.text = f"Archivo seleccionado: {selected_file}"

        except Exception as error:
            print('Error al seleccionar archivo:', error)
            self.label.text = "Error al seleccionar archivo."


