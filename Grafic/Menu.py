import os.path
from operator import truediv

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
import sys

from numpy.lib.utils import source

sys.path.append('C:/Users/micro/PycharmProjects/PyVideo/')
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.core.window import Window
from Directory.DeleteArchiveDirectory import DeleteArchiveDirectory
from Directory.OpenDirectory import OpenDirectory
from Directory.AddCreateVideoStore import AddCreateVideoStore
from ffpyplayer.player import MediaPlayer
import Directory.DeleteArchiveDirectory as deleteVideo
from ModificText import ModificText
from Directory.AddArchiveDirectory import AddArchiveDirectory
from ActionVideo import ActionVideo
from ffpyplayer.player import MediaPlayer
from ControlSound.ActionSound import ActionSound
import cv2
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture

class Menu(App):
    def build(self):
        self.capture = None
        self.pauseAction = False
        self.buttonPlay = None  # Asumimos que tienes el botón Play/Pause
        self.listVideo = []  # Lista de videos disponibles en el directorio
        self.video_path = '../Image/pause.png'
        Window.maximize()
        Window.clearcolor = (0.2, 0.3, 0.4, 1)
        self.title = 'PyVideo'
        # Layout principal (vertical)
        self.layout = BoxLayout(orientation='vertical')
        # Crear el objeto MediaPlayer de ffpyplayer
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
        self.buttonEnviar=Button(text="Enviar Video",size_hint=(0.1,1))
        self.boxNav.add_widget(self.buttonEnviar)

        self.buttonRecibir = Button(text="Recibir Video", size_hint=(0.1, 1))
        self.boxNav.add_widget(self.buttonRecibir)

        # Botón Enviar Bluetooth
        self.buttonEmitirLocal=Button(text="Emitir Local",size_hint=(0.1,1))
        self.boxNav.add_widget(self.buttonEmitirLocal)
        # Botón Descargar Video
        self.buttonEmitirYouTube=Button(text="Emitir YouTube",size_hint=(0.1,1))
        self.boxNav.add_widget(self.buttonEmitirYouTube)
        # Botón Borrar Video
        self.buttonBorrarVideo=Button(text="Borrar",size_hint=(0.1,1))
        self.buttonBorrarVideo.bind(on_press=self.on_press_Borrar)

        self.boxNav.add_widget(self.buttonBorrarVideo)
        # Botón Atras
        self.buttonAtras = Button(text="Atras", size_hint=(0.1, 0.2))
        self.buttonAtras.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.buttonAtras.bind(on_press=self.on_button_atras)

        self.box.add_widget(self.buttonAtras)

        # Crear el widget de imagen donde se mostrará el video
        self.img = Image(source=self.video_path)

        self.box.add_widget(self.img)
        # Botón Delante
        self.buttonDelante = Button(text="Delante", size_hint=(0.1, 0.2))
        self.buttonDelante.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.buttonDelante.bind(on_press=self.on_button_adelante)
        self.box.add_widget(self.buttonDelante)

        # Button Maximice
        self.buttonMax = Button(text="Maximize")
        self.buttonMax.bind(on_press=self.on_button_maximize)
        self.buttonMax.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.boxBack.add_widget(self.buttonMax)
        #Boton de suma de tiempo
        self.sumarVideo=Button(text="Más 30s", size_hint=(0.5, 1))
        self.sumarVideo.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.sumarVideo.bind(on_press=self.adelantar_30s)
        self.boxBack.add_widget(self.sumarVideo)
        #Botón para reducir tiempo
        self.restarVideo = Button(text="Menos 30s", size_hint=(0.5, 1))
        self.restarVideo.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.restarVideo.bind(on_press=self.atrasar_30s)
        self.boxBack.add_widget(self.restarVideo)
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
        self.slider = Slider(min=0, max=100,value=15,step=1)
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
            # Comprobar si el índice 'numero' es menor que el tamaño de la lista - 1
            if numero < len(listVideo) + 1:
                numero -= 1  # Avanzar al siguiente video
                self.video_path = '../VideoStore/' + listVideo[numero]
                self.capture = cv2.VideoCapture(self.video_path)  # Cargar el siguiente video
                print(f"Reproduciendo: {listVideo[numero]}", 'Numero: ', numero)
            else:
                print('No existen más videos')
        except Exception as error:
            print('Error al adelantar el video', error)


    def on_button_adelante(self, instance):
        global numero
        try:
            # Comprobar si el índice 'numero' es menor que el tamaño de la lista - 1
            if numero < len(listVideo) -1:
                numero += 1  # Avanzar al siguiente video
                self.video_path= '../VideoStore/' + listVideo[numero]
                self.capture = cv2.VideoCapture(self.video_path)  # Cargar el siguiente video
                print(f"Reproduciendo: {listVideo[numero]}", 'Numero: ', numero)
            else:
                print('No existen más videos')
        except Exception as error:
            print('Error al adelantar el video', error)

    def on_button_press(self, instance):
        # Comprobar si ya se ha cargado el video
        if self.capture is None or not self.capture.isOpened():
            if len(listVideo) != 0:
                # Si no se ha cargado el video, cargar el video actual desde la lista
                self.capture = cv2.VideoCapture('../VideoStore/' + listVideo[numero])
                self.video_path='../VideoStore/' + listVideo[numero]
                Clock.schedule_interval(self.update, 1.0 / 30.0)
            else:
                print('No se encuentra el directorio')
        else:
            # Si ya está cargado, solo alternar el estado de pausa
            self.pauseAction = not self.pauseAction
            self.buttonPlay.text = 'Play' if self.pauseAction else 'Pause'

    def on_press_Añadir(self,instance):
        global listVideo
        try:
            # Llamado cuando el botón "Cerrar la ejecución" es presionado
            print("La aplicación se cerrará.")
            self.capture=cv2.VideoCapture(0)
            # Liberar el recurso de captura de OpenCV
            if self.capture is not None:
                self.capture.release()  # Libera el recurso de la cámara

            # Detener la aplicación de Kivy
            self.stop()
            op.run()
            url_video = delete.functionDeleteText(op.label.text)
            url_correcta = delete.functionValidationUrl(url_video)
            addD.functionAddArchiveDirectory(url_correcta, "../VideoStore")
        except Exception as error:
            print('Error al añadir', error)
    def on_press_Borrar(self,instance):
        try:
            if self.video_path!='../Image/pause.png':
                self.capture.release()
                deleteVideo.functionDeleteArchive(self.video_path)
        except Exception as error:
            print('Error al borrar',error)

    def return_sound(self,instance,touch):
        try:
            if instance.collide_point(*touch.pos):
             actionSound.functionControlSound(instance.value)
        except Exception as error:
            print('Error al mover el sonido',error)

    def on_button_maximize(self, instance):
        try:
            self.layout.size_hint = (1, 1)
            self.layout.padding = (0, 0)
            self.layout.spacing = 0

            self.layout.remove_widget(self.boxNav)
            self.layout.remove_widget(self.boxBack)
            self.box.remove_widget(self.buttonAtras)
            self.box.remove_widget(self.buttonDelante)

            self.box.size_hint = (1, 1)
            self.img.size_hint = (1, 1)
            self.img.keep_ratio = False
            self.img.allow_stretch = True

            self.img.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Centra el video en la pantalla


            # Maximiza la ventana
            Window.fullscreen=True

            self.img.size = Window.size

            self.img.bind(on_touch_down=self.on_video_click)

        except Exception as error:
            print('Error al maximizar el video:', error)

    def on_video_click(self,instance,touch):
        try:
            self.box.remove_widget(self.img)
            self.layout.remove_widget(self.box)
            self.boxNav.size_hint=(1, 0.1)
            self.layout.add_widget(self.boxNav)
            self.box.add_widget(self.buttonAtras)
            self.box.add_widget(self.img)
            self.box.add_widget(self.buttonDelante)
            self.box.size_hint = (1, 0.8)
            self.layout.add_widget(self.box)
            self.layout.add_widget(self.boxBack)
            Window.fullscreen=False
            self.img.unbind(on_touch_down=self.on_video_click)

        except Exception as error:
            print('Error al hacer click en el video',error)



    def update(self, dt):
        # Asegurarse de que el video esté cargado
        if self.capture is None or not self.capture.isOpened():
            return  # Si no se ha abierto el video, no hacer nada

        if self.pauseAction:
            # Si está pausado, no leer un nuevo frame y mostrar el último frame pausado
            if self.paused_frame is not None:
                # Solo mostrar el último frame pausado en el widget de Kivy (sin abrir una nueva ventana)

                frame = self.paused_frame
                frame = cv2.flip(frame, 0)

                # Convertir el frame a formato adecuado para Kivy (de BGR a RGB)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Convertir el frame en una textura que pueda ser utilizada por Kivy
                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

                # Mostrar la textura en el widget de imagen
                self.img.texture = texture
            return  # No leer un nuevo frame mientras está pausado

        # Si no está pausado, leer un nuevo frame
        ret, frame = self.capture.read()

        if ret:
            # Guardar el frame actual antes de continuar (para poder pausarlo)
            self.paused_frame = frame

            # Voltear el frame horizontalmente (flip horizontal)
            frame = cv2.flip(frame, 0)

            # Convertir el frame a formato adecuado para Kivy (de BGR a RGB)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convertir el frame en una textura que pueda ser utilizada por Kivy
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            # Mostrar la textura en el widget de imagen
            self.img.texture = texture
        else:
            # Si el video ha terminado (ret es False), mostrar la imagen
            self.show_end_image()

    def show_end_image(self):
        # Cargar la imagen que quieres mostrar al final del video
        end_image_path = '../Image/pause.png'  # Cambia la ruta a la imagen que deseas mostrar
        end_image = cv2.imread(end_image_path)

        # Convertir la imagen a formato adecuado para Kivy (de BGR a RGB)
        end_image = cv2.cvtColor(end_image, cv2.COLOR_BGR2RGB)

        # Crear la textura para la imagen final
        texture = Texture.create(size=(end_image.shape[1], end_image.shape[0]), colorfmt='rgb')
        texture.blit_buffer(end_image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

        # Mostrar la textura en el widget de imagen
        self.img.texture = texture
        self.capture.release()

    def adelantar_30s(self,instance):
        # Asegúrate de que el video está abierto
        if self.capture is not None and self.capture.isOpened():
            # Obtener la posición actual en milisegundos
            current_time_ms = self.capture.get(cv2.CAP_PROP_POS_MSEC)

            # Adelantar 30 segundos (30000 milisegundos)
            new_time_ms = current_time_ms + 30000  # 30 segundos en milisegundos

            # Establecer la nueva posición en milisegundos
            self.capture.set(cv2.CAP_PROP_POS_MSEC, new_time_ms)

            print(f"Adelantando 30 segundos: del tiempo {current_time_ms}ms al tiempo {new_time_ms}ms")
    def atrasar_30s(self,instance):
        # Asegúrate de que el video está abierto
        if self.capture is not None and self.capture.isOpened():
            # Obtener la posición actual en milisegundos
            current_time_ms = self.capture.get(cv2.CAP_PROP_POS_MSEC)

            # Adelantar 30 segundos (30000 milisegundos)
            new_time_ms = current_time_ms - 30000  # 30 segundos en milisegundos

            # Establecer la nueva posición en milisegundos
            self.capture.set(cv2.CAP_PROP_POS_MSEC, new_time_ms)

            print(f"Adelantando 30 segundos: del tiempo {current_time_ms}ms al tiempo {new_time_ms}ms")

    def on_stop(self):
        # Liberar la captura de video cuando se cierre la aplicación
        self.capture.release()


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