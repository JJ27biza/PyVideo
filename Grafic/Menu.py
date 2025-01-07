import os.path

from kivy.app import App
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.uix.video import Video
from kivy.core.window import Window
from Directory.DeleteArchiveDirectory import DeleteArchiveDirectory
from Directory.OpenDirectory import OpenDirectory
from Directory.AddCreateVideoStore import AddCreateVideoStore
import Directory.DeleteArchiveDirectory as deleteVideo
from ModificText import ModificText
from Directory.AddArchiveDirectory import AddArchiveDirectory
from ActionVideo import ActionVideo
from ControlSound.ActionSound import ActionSound

class Menu(App):
    def build(self):
        Window.maximize()
        Window.clearcolor = (0.2, 0.3, 0.4, 1)
        self.title = 'PyVideo'
        # Layout principal (vertical)
        self.layout = BoxLayout(orientation='vertical')
        # Crear BoxLayouts con diferentes tamaños (size_hint)
        self.boxNav = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))# BoxNav ocupa solo 10% de la altura
        self.boxBack = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))
        self.boxBack.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.box = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))  # Box ocupa el 80% de la altura
        ############################Botones y video###################################
        # Botón Añadir
        self.buttonAñadir = Button(text="Añadir", size_hint=(0.1, 1))
        self.buttonAñadir.bind(on_press=self.on_press_Añadir)
        self.boxNav.add_widget(self.buttonAñadir)
        # Botón Añadir Bluethoot
        self.buttonBluethoot=Button(text="Añadir Bluetooth",size_hint=(0.1,1))
        self.boxNav.add_widget(self.buttonBluethoot)
        # Botón Enviar Bluetooth
        self.buttonEnviarVideo=Button(text="Enviar Blutooth",size_hint=(0.1,1))
        self.boxNav.add_widget(self.buttonEnviarVideo)
        # Botón Descargar Video
        self.buttonDescargar=Button(text="Descargar Video",size_hint=(0.1,1))
        self.boxNav.add_widget(self.buttonDescargar)
        # Botón Borrar Video
        self.buttonBorrarVideo=Button(text="Borrar",size_hint=(0.1,1))
        self.buttonBorrarVideo.bind(on_press=self.on_press_Borrar)

        self.boxNav.add_widget(self.buttonBorrarVideo)
        # Botón Atras
        self.buttonAtras = Button(text="Atras", size_hint=(0.1, 0.2))
        self.buttonAtras.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.buttonAtras.bind(on_press=self.on_button_atras)

        self.box.add_widget(self.buttonAtras)
        # Video

        self.video = Video(source= '../Image/pause.png',state="pause",size_hint=(1, 1),pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.box.add_widget(self.video)
        # Botón Delante
        self.buttonDelante = Button(text="Delante", size_hint=(0.1, 0.2))
        self.buttonDelante.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.buttonDelante.bind(on_press=self.on_button_adelante)
        self.box.add_widget(self.buttonDelante)
        # Button Maximice
        self.buttonMax = Button(text="Maximize", size_hint=(0.5, 1))
        # self.buttonMax.bind(on_press=self.on_button_press)
        self.buttonMax.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.boxBack.add_widget(self.buttonMax)

        # Botón Play (en BoxBack)
        self.buttonPlay = Button(text="Play", size_hint=(0.5, 1))
        self.buttonPlay.bind(on_press=self.on_button_press)
        self.buttonPlay.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.boxBack.add_widget(self.buttonPlay)

        #Progress bar volumen
        #self.pbVolumen = ProgressBar(value=50, max=100,size_hint=(0.5, 1))
        #self.pbVolumen.value_normalized
        #self.pbVolumen.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        #self.boxBack.add_widget(self.pbVolumen)
        #Imagen Volumen
        self.vimg = Image(source="../Picture/alto_volumen.png",size_hint=(None, 1))
        self.vimg.padding = (0, 0)  # Aseguramos que la imagen no tenga relleno
        self.boxBack.add_widget(self.vimg)
        #SeekBar Volumen
        self.slider = Slider(min=0, max=100,step=1)
        self.slider.bind(on_touch_up=self.return_sound)
        self.boxBack.add_widget(self.slider)
        # Añadir los BoxLayouts al layout principal
        self.layout.add_widget(self.boxNav)
        self.layout.add_widget(self.box)
        self.layout.add_widget(self.boxBack)
        return self.layout
    def on_button_atras(self,instance):
        global numero
        try:
            if 0 < numero:
                 numero-=1
                 self.video.source='../VideoStore/'+listVideo[numero]
                 self.video.state = 'stop'
                 self.video.state = 'play'
                 print(f"Reproduciendo: {listVideo[numero]}",'Numero: ',numero)
                 print('Atras', numero)
            else:
                print('No existen más videos')
        except Exception as error:
            print('Error al siguiente video',error)
    def on_button_adelante(self,instance):
        global numero

        try:
            if (len(listVideo)-1)>numero:
                numero += 1
                self.video.source = '../VideoStore/'+listVideo[numero]
                self.video.state = 'stop'
                self.video.state = 'play'
                print(f"Reproduciendo: {listVideo[numero]}",'Numero: ',numero)
                print('Adelante',numero)
            else:

                print('No existen más videos')

        except Exception as error:
            print('Error al siguiente video',error)

    def on_button_press(self, instance):
        if self.video.source == '../Image/pause.png' or not os.path.isdir('../VideoStore'):
            if len(listVideo) != 0:
                self.video.source = '../VideoStore/' + listVideo[numero]
                self.video.state = 'play'
                self.buttonPlay.text = "Pause"
            else:
                print('Nose encuentra directorio')
        elif self.video.state == 'play':
            self.video.state = 'pause'
            self.buttonPlay.text = "Play"
        else:
            self.video.state = 'play'
            self.buttonPlay.text = "Pause"
    def on_press_Añadir(self,instance):

        global listVideo
        try:
            self.stop()
            op.run()
            url_video = delete.functionDeleteText(op.label.text)
            url_correcta = delete.functionValidationUrl(url_video)
            addD.functionAddArchiveDirectory(url_correcta, "../VideoStore")
        except Exception as error:
            print('Error al añadir', error)
    def on_press_Borrar(self,instance):
        try:
            video_path = self.video.source

            deleteVideo.functionDeleteArchive(video_path)
        except Exception as error:
            print('Error al borrar',error)

    def return_sound(self,instance,touch):

        try:
            if instance.collide_point(*touch.pos):
                value = instance.value
            actionSound.functionControlSound(value)
            print(value)
        except Exception as error:
            print('Error al mover el sonido',error)
if __name__ == "__main__":
    op = OpenDirectory()
    delete=ModificText()
    numero=0
    addD=AddArchiveDirectory()
    deleteVideo=DeleteArchiveDirectory()
    actionVideo=ActionVideo()
    actionVideoStore=AddCreateVideoStore()
    listVideo=actionVideo.listVideo()
    actionVideoStore.functionCreateVideoStore()
    actionSound=ActionSound()
    Menu().run()