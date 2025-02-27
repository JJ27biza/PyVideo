import os.path
from operator import truediv

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
import sys
import socket
import threading


from numpy.lib.utils import source

sys.path.append('C:/Users/micro/PycharmProjects/PyVideo/')
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.slider import Slider
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from Directory.DeleteArchiveDirectory import DeleteArchiveDirectory
from Directory.OpenDirectory import OpenDirectory
from Directory.AddCreateVideoStore import AddCreateVideoStore
from ffpyplayer.player import MediaPlayer
import Directory.DeleteArchiveDirectory as deleteVideo
import Subtitules.strToVideo as strVideo
import Subtitules.Subtitules as VideoSubtitles
from ModificText import ModificText
from Directory.AddArchiveDirectory import AddArchiveDirectory
from ActionVideo import ActionVideo
from ffpyplayer.player import MediaPlayer
from ControlSound.ActionSound import ActionSound
from kivy.uix.dropdown import DropDown
import Emision.ListaEmitir as lista
import Emision.EmitirLocal as emitirLocal
import Emision.EmitirYouTube as emitiryt
import cv2
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import pygame
import AudioExtraction as audio
import serverFake as sf
import UrlDescarga as ud
from threading import Thread
import time





class Menu(App):
    def build(self):
        self.capture = None
        self.pauseAction = False
        self.buttonPlay = None
        self.audio_started = False
        self.url_yt_pop=None
        self.listSubtitules=[]
        self.video_path = '../Image/pause.png'
        self.sound_path=None
        self.buttonPlay = None  # Este debería ser un botón en tu interfaz Kivy
        self.video_time = 0  # Mantener la posición del video
        self.paused_frame = None
        self.error_Borrado=False
        self.hilo_server=None
        self.arrayListar=lista.listar_chromecasts()
        self.ip=None
        self.actionSubtitules = True
        self.nombreSubtitulos = None
        self.last_audio_time = 0  # Para sincronizar audio
        self.last_sync_time = time.time()  # Para medir cuando hacer la sincronización
        self.sync_threshold = 0.1  # Umbral de sincronización en segundos
        self.sync_interval = 0.5  # Intervalo de sincronización (en segundos)
        self.last_audio_adjustment = time.time()

        pygame.mixer.init()
        Window.maximize()
        Window.clearcolor = (0.2, 0.3, 0.4, 1)
        Window.bind(on_request_close=self.on_cerrar)
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

        self.buttonEnviar.bind(on_press=self.open_popup_Server_Output)

        self.boxNav.add_widget(self.buttonEnviar)

        self.buttonRecibir = Button(text="Recibir Video", size_hint=(0.1, 1))
        self.buttonRecibir.bind(on_press=self.open_popup_Server_Inputput)
        self.boxNav.add_widget(self.buttonRecibir)
        # create a dropdown with 10 buttons
        self.dropdown = DropDown()
        if self.arrayListar==None or self.arrayListar==0:
            self.arrayListar=''
        for index in enumerate(self.arrayListar):
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            # Crea el botón
            self.btn = Button(text=str(index[1]), size_hint_y=None, height=44)

            # Usar una lambda para asegurarse de que el texto del botón se pase correctamente
            self.btn.bind(on_release=lambda btn=self.btn: self.dropdown.select(btn.text))

            # Añadir el botón al dropdown
            self.dropdown.add_widget(self.btn)

        if self.video_path !='../Image/pause.png':
            self.dropdown.bind(on_select=lambda instance, x: emitirLocal.emit_in_local(self.video_path, x))

        self.dropdownyt = DropDown()
        if self.arrayListar==None or self.arrayListar==0:
            self.arrayListar=''
        for index in enumerate(self.arrayListar):
            # When adding widgets, we need to specify the height manually
            # (disabling the size_hint_y) so the dropdown can calculate
            # the area it needs.

            # Crea el botón
            self.btn = Button(text=str(index[1]), size_hint_y=None, height=44)

            # Usar una lambda para asegurarse de que el texto del botón se pase correctamente
            self.btn.bind(on_release=lambda btn=self.btn: self.dropdownyt.select(btn.text))

            # Añadir el botón al dropdown
            self.dropdownyt.add_widget(self.btn)

        # Bind del dropdown
        self.dropdownyt.bind(on_select=lambda instance, x:self.open_popup_YT(x) )



        # Botón Enviar Bluetooth
        self.buttonEmitirLocal=Button(text="Emitir Local",size_hint=(0.1,1))
        self.buttonEmitirLocal.bind(on_release=self.dropdown.open)
        #self.dropdown.bind(on_select=lambda instance, x: setattr(self.buttonEmitirLocal, 'text', x))
        self.boxNav.add_widget(self.buttonEmitirLocal)
        # Botón Descargar Video
        self.buttonEmitirYouTube=Button(text="Emitir YouTube",size_hint=(0.1,1))
        #
        self.buttonEmitirYouTube.bind(on_release=self.dropdownyt.open)

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
        self.buttonSubtitle = Button(text="Subtitulos", size_hint=(0.5, 1))
        self.buttonSubtitle.bind(on_press=self.load_Subtitules)
        self.buttonSubtitle.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.boxBack.add_widget(self.buttonSubtitle)

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
    #Este método permite volver atras para ver el video
    def on_button_atras(self,instance):
        global numero
        try:
            # Comprobar si el índice 'numero' es menor que el tamaño de la lista - 1
            if numero < len(listVideo) + 1:
                numero -= 1  # Avanzar al siguiente video
                self.video_path = '../VideoStore/' + listVideo[numero]
                self.sound_path='../SoundStore/'+listVideo[numero]+'_audio.mp3'
                pygame.mixer.music.load('../SoundStore/' + listVideo[numero] + '_audio.mp3')
                self.capture = cv2.VideoCapture(self.video_path)  # Cargar el siguiente video
                print(f"Reproduciendo: {listVideo[numero]}", 'Numero: ', numero)
            else:
                print('No existen más videos')
        except Exception as error:
            print('Error al adelantar el video', error)

    # Este método permite ir hacia delante para ver el video
    def on_button_adelante(self, instance):
        global numero
        try:
            # Comprobar si el índice 'numero' es menor que el tamaño de la lista - 1
            if numero < len(listVideo) -1:
                numero += 1  # Avanzar al siguiente video
                self.video_path= '../VideoStore/' + listVideo[numero]
                self.sound_path='../SoundStore/' + listVideo[numero] + '_audio.mp3'
                pygame.mixer.music.load('../SoundStore/' + listVideo[numero] + '_audio.mp3')
                self.capture = cv2.VideoCapture(self.video_path)  # Cargar el siguiente video
                print(f"Reproduciendo: {listVideo[numero]}", 'Numero: ', numero)
            else:
                print('No existen más videos')
        except Exception as error:
            print('Error al adelantar el video', error)

    #Control del botón de pausa o play para detener o reanudar tanto audio como video
    def on_button_press(self, instance):
        # Comprobar si ya se ha cargado el video
        if self.capture is None or not self.capture.isOpened():
            if len(listVideo) != 0:
                if self.video_path == '../Image/pause.png':
                    print('Cargar video y audio')

                    # Cargar el archivo de video
                    self.video_path = '../VideoStore/' + listVideo[numero]
                    self.capture = cv2.VideoCapture(self.video_path)

                    # Cargar y reproducir el audio
                    self.sound_path= '../SoundStore/' + listVideo[numero] + '_audio.mp3'
                    pygame.mixer.music.load(self.sound_path)

                    # Reproducir el audio desde el inicio y sincronizar con el video
                    pygame.mixer.music.play(loops=0, start=0.0)

                    # Comenzar la actualización del video
                    Clock.unschedule(self.update)
                    Clock.schedule_interval(self.update, 1.0 / 30.0)

                else:

                    if self.error_Borrado==False:
                        pygame.mixer.music.play(loops=0,
                                            start=self.video_time)  # Comienza el audio desde el tiempo actual del video
                    else:
                        print('Error en el borrado')
                        self.video_path=='../Image/pause.png'
                        self.error_Borrado=True

            else:
                print('No se encuentra el directorio')

        else:
            if self.video_path != '../Image/pause.png':
                # Pausar el video y el audio simultáneamente
                pygame.mixer.music.pause()
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.video_time * 30)  # Guardar la posición en segundos

            # Alternar entre pausa y play
            self.pauseAction = not self.pauseAction
            self.buttonPlay.text = 'Play' if self.pauseAction else 'Pause'

    #Añadir vide al directorio de VideoStore y el audio de ese video
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
            url_audio= audio.extraction_Audio(url_correcta)
            addD.functionAddArchiveDirectory(url_correcta, "../VideoStore")
            addD.functionAddArchiveDirectory(url_audio, "../SoundStore")
        except Exception as error:
            print('Error al añadir', error)
    #Método que borra el video del directorio y el audio
    def on_press_Borrar(self,instance):
        global numero,listVideo
        try:
            if self.video_path!='../Image/pause.png':
                numero=0
                self.capture.release()
                self.img.source='../Image/pause.png'
                self.img.reload()
                pygame.mixer.music.unload()
                pygame.mixer.music.stop()
                deleteVideo.functionDeleteArchive(self.video_path)
                pygame.mixer.quit()
                deleteVideo.functionDeleteArchive(self.sound_path)
                pygame.mixer.init()
                self.video_path='../Image/pause.png'
                self.sound_path=None
                listVideo.clear()
                listVideo = actionVideo.listVideo()
        except Exception as error:
            print('Error al borrar',error)
    #Método para volver a ejecutar el audio
    def return_sound(self,instance,touch):
        try:
            if instance.collide_point(*touch.pos):
             actionSound.functionControlSound(instance.value)
        except Exception as error:
            print('Error al mover el sonido',error)
    #Metódo para maximizar el video
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

    #Método para que al hacer click en la ventana se vuelva al formato original, solo funciona si esta maximizado anteriormente
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
    #Actualización de los frames del video para que se reproduzca
    import pygame

    import pygame

    def update(self, dt):
        # Asegurarse de que el video esté cargado
        if self.capture is None or not self.capture.isOpened():
            return  # Si no se ha abierto el video, no hacer nada

        if self.pauseAction:
            # Si está pausado, no leer un nuevo frame y mostrar el último frame pausado
            if self.paused_frame is not None:
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

            # Mantener el tiempo actual del video (en segundos)
            self.video_time = self.capture.get(cv2.CAP_PROP_POS_MSEC) / 1000

            # **Sincronización al inicio**: Comenzar solo si no está en reproducción
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=0, start=self.video_time)

            # **Ajuste suave de audio**: Realizar ajustes solo si la diferencia es mayor que el umbral
            current_time = time.time()

            # Si el tiempo desde el último ajuste de audio es mayor que el intervalo deseado
            if abs(self.video_time - self.last_audio_time) > self.sync_threshold:
                # Ajuste suave: Solo sincronizar cuando haya un desfase significativo
                if current_time - self.last_audio_adjustment > self.sync_interval:
                    pygame.mixer.music.set_pos(self.video_time)
                    self.last_audio_time = self.video_time
                    self.last_audio_adjustment = current_time

        else:
            # Si el video ha terminado (ret es False), mostrar la imagen final y detener el audio
            self.show_end_image()
            pygame.mixer.music.stop()  # Detener el audio cuando el video termine

    #Al finalizar el video mostrar la imagen de pausa
    def show_end_image(self):
        # Cargar la imagen que quieres mostrar al final del video
        end_image_path = '../Image/pause.png'  # Cambia la ruta a la imagen que deseas mostrar
        end_image = cv2.imread(end_image_path)
        if end_image is None:
            print("Error: No se pudo leer el frame del video")
            self.error_Borrado=True
        else:
            end_image = cv2.cvtColor(end_image, cv2.COLOR_BGR2RGB)

        # Convertir la imagen a formato adecuado para Kivy (de BGR a RGB)


        # Crear la textura para la imagen final
        texture = Texture.create(size=(end_image.shape[1], end_image.shape[0]), colorfmt='rgb')
        texture.blit_buffer(end_image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

        # Mostrar la textura en el widget de imagen
        self.img.texture = texture
        pygame.mixer.music.stop()  # Detener el audio cuando termina el video
        self.capture.release()

    #Metódo para adelantar el video y audio 30 segundos sincronizandolos
    def adelantar_30s(self, instance):
        # Asegúrate de que el video está abierto
        if self.capture is not None and self.capture.isOpened():
            # Obtener la posición actual en milisegundos (para el video)
            current_time_ms = self.capture.get(cv2.CAP_PROP_POS_MSEC)

            # Adelantar 30 segundos (30000 milisegundos)
            new_time_ms = current_time_ms + 30000  # 30 segundos en milisegundos

            # Establecer la nueva posición en milisegundos para el video
            self.capture.set(cv2.CAP_PROP_POS_MSEC, new_time_ms)

            # Sincronizar el audio
            new_time_seconds = new_time_ms / 1000  # Convertir a segundos
            pygame.mixer.music.set_pos(new_time_seconds)  # Establecer la posición en el audio

            print(f"Adelantando 30 segundos: del tiempo {current_time_ms}ms al tiempo {new_time_ms}ms")
    #Metódo para retrasar el video y audio 30 segundos sincronizandolos

    def atrasar_30s(self, instance):
        # Asegúrate de que el video está abierto
        if self.capture is not None and self.capture.isOpened():
            # Obtener la posición actual en milisegundos (para el video)
            current_time_ms = self.capture.get(cv2.CAP_PROP_POS_MSEC)

            # Atrasar 30 segundos (30000 milisegundos)
            new_time_ms = current_time_ms - 30000  # 30 segundos en milisegundos

            # Asegurarse de no atrasar más allá del inicio del video
            new_time_ms = max(new_time_ms, 0)

            # Establecer la nueva posición en milisegundos para el video
            self.capture.set(cv2.CAP_PROP_POS_MSEC, new_time_ms)

            # Sincronizar el audio
            new_time_seconds = new_time_ms / 1000  # Convertir a segundos
            pygame.mixer.music.set_pos(new_time_seconds)  # Establecer la posición en el audio

            print(f"Atrasando 30 segundos: del tiempo {current_time_ms}ms al tiempo {new_time_ms}ms")
    #Metodo que libera la ejecucción del video
    def on_stop(self):
        # Liberar la captura de video cuando se cierre la aplicación
        self.capture.release()
    #Método para reanudar el video y audio desde el tiempo guardado
    def resume_video(self):
        # Reanudar el video y el audio desde el tiempo guardado
        pygame.mixer.music.unpause()  # Reanudar el audio
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.video_time * 30)  # Reanudar el video en la posición correcta
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Reanudar la actualización del video

    #Método para abrir una vetana para la emisión de YouTube
    def open_popup_YT(self, x):
        # Crear el contenido para la ventana emergente (popup)
        self.popup_content = BoxLayout(orientation='vertical')

        self.label = Label(text='Añada la url del video de YouTube que desea visualizar')
        self.textinput = TextInput()
        self.close_button = Button(text="Ok")

        # Usar una lambda para pasar el argumento 'x' al método close_popup
        self.close_button.bind(on_release=lambda instance: self.close_popup_YT(instance, x))

        # Añadir los widgets al contenido del popup
        self.popup_content.add_widget(self.label)
        self.popup_content.add_widget(self.textinput)
        self.popup_content.add_widget(self.close_button)

        # Crear el Popup y mostrarlo
        self.popup = Popup(title="Ventana Emergente", content=self.popup_content,
                           size_hint=(None, None), size=(400, 300))
        self.popup.open()

    #Metódo para cerrar la ventana de la emisión de Youtube
    def close_popup_YT(self, instance, x):
        # Cerrar el popup cuando se presione el botón de cerrar
        self.popup.dismiss()

        # Obtener el texto del TextInput
        self.url_yt_pop = self.textinput.text
        if self.textinput.text != '':
            # Eliminar la parte de la URL de YouTube
            delete = "https://www.youtube.com/watch?v="
            self.url_yt_pop = self.url_yt_pop.replace(delete, "")
            print(self.url_yt_pop)
            # Llamar a la función emitiryt con el valor procesado
            emitiryt.emit_in_yt(self.url_yt_pop, x)
    #Método para abrir la ventana del funcinamiento del servidor
    def open_popup_Server_Output(self, instance):
        # Crear el contenido para la ventana emergente (popup)
        self.popup_content = BoxLayout(orientation='vertical')
        mi_ip = socket.gethostbyname(socket.gethostname())
        if self.video_path != '../Image/pause.png':

            self.label = Label(text='Server ya funcionando durante 1 minuto')
            self.label2 = Label(text='http://' + mi_ip + ':5000/descarga')
            self.close_button = Button(text="Close")

            # Usar una lambda para pasar el argumento 'x' al método close_popup_Server
            self.close_button.bind(on_release=lambda instance: self.close_popup_Server(instance))

            # Añadir los widgets al contenido del popup
            self.popup_content.add_widget(self.label)
            self.popup_content.add_widget(self.label2)
            self.popup_content.add_widget(self.close_button)

            # Crear el Popup y mostrarlo
            self.popup = Popup(title="Ventana Server", content=self.popup_content,
                               size_hint=(None, None), size=(400, 300))
            self.popup.open()

            delete = "../VideoStore/"
            url_video = self.video_path.replace(delete, "")



            self.hilo_server=threading.Thread(target=sf.enviarVideo, args=(url_video,))
            self.hilo_server.start()
        else:
            self.label = Label(text='No estas enviando video')
            self.close_button = Button(text="Close")
            self.popup_content.add_widget(self.label)
            self.popup_content.add_widget(self.close_button)
            self.close_button.bind(on_release=lambda instance: self.close_popup_Server(instance))
            # Crear el Popup y mostrarlo
            self.popup = Popup(title="Ventana Server", content=self.popup_content,
                               size_hint=(None, None), size=(400, 300))
            self.popup.open()

    #Método para cerrar la ventana del funcionamiento servidor
    def close_popup_Server(self, instance):
        # Cerrar el popup cuando se presione el botón de cerrar
        self.popup.dismiss()  # Cerrar el popup correctamente
    #Metódo para abrir la vetana para introducir la url para descargar el video
    def open_popup_Server_Inputput(self, instance):
        # Crear el contenido para la ventana emergente (popup)
        self.popup_content2 = BoxLayout(orientation='vertical')
        mi_ip = socket.gethostbyname(socket.gethostname())
        self.label = Label(text='Descargar de video indica solo su ip. Ejemplo: 192.168.x.x')
        self.textinput = TextInput()
        self.close_button = Button(text="Ok")

        # Usar una lambda para pasar el argumento 'x' al método close_popup_Server
        self.close_button.bind(on_release=lambda instance: self.close_popup_Input(instance))

        # Añadir los widgets al contenido del popup
        self.popup_content2.add_widget(self.label)
        self.popup_content2.add_widget(self.textinput)
        self.popup_content2.add_widget(self.close_button)

        # Crear el Popup y mostrarlo
        self.popup = Popup(title="Ventana Entrada", content=self.popup_content2,
                           size_hint=(None, None), size=(400, 300))
        self.popup.open()



    #Metódo para cerrar la ventana de la descarga del video
    def close_popup_Input(self, instance):
        # Cerrar el popup cuando se presione el botón de cerrar
        self.popup.dismiss()
        if self.textinput.text != '':
            self.ip=self.textinput.text
            url='http://'+self.ip+':5000/descarga'
            ud.descargar_archivo(url)
    def add_url_yt(self,instance):
        self.open_popup_YT()
    def standBy_Video(self):
        try:
           self.capture.release()



        except Exception as error:
            print('Error en standBy',error)

    def load_Subtitules(self, instance):
        global listVideo, numero
        try:

            self.listSubtitules = actionVideo.listVideoSubtitulos()
            nombre = listVideo[numero]
            print('Nombre ', nombre)
            numero = 0
            self.capture.release()
            pygame.mixer.music.unload()
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            pygame.mixer.init()

            # Cambiar imagen a "cargando.png"
            Clock.schedule_once(lambda dt: self.update_image_source('../Image/cargando.png'), 0)

            # Procesar los subtítulos y el video en un hilo separado
            def process_subtitles_and_video():

                for i in self.listSubtitules:
                    if i == nombre + 'with_subtitles.mp4':
                        self.actionSubtitules = False
                        self.nombreSubtitulos = i
                if self.actionSubtitules:
                    VideoSubtitles.str_Subtitules(nombre)
                    strVideo.srt_To_Video(nombre)

                    # Borrar archivos temporales
                    deleteVideo.functionDeleteArchive('temp_audio.mp3')
                    deleteVideo.functionDeleteArchive(nombre + '_subtitles.srt')
                    self.video_path = '../Image/pause.png'

                    # Cambiar la imagen a mostrar
                    Clock.schedule_once(lambda dt: self.update_image_source('../Image/pause.png'), 0)

                    self.show_image = False
                else:
                    self.video_path = '../VideoStoreSubtitles/' + self.nombreSubtitulos
                    self.sound_path = '../SoundStore/' + nombre + '_audio.mp3'
                    pygame.mixer.music.load(self.sound_path)
                    self.capture = cv2.VideoCapture(self.video_path)

            # Crear un hilo para el procesamiento
            processing_thread = Thread(target=process_subtitles_and_video)
            processing_thread.start()

        except Exception as error:
            print('Error en la carga de Subtitulos', error)

    def update_image_source(self, image_path):
        self.img.source = image_path
        self.img.reload()

    def on_cerrar(self, instance):

        if self.hilo_server.is_alive():
            print('Espere a que el hilo finalice')
            return True


if __name__ == "__main__":
    op = OpenDirectory()
    delete=ModificText()
    numero=0
    addD=AddArchiveDirectory()
    deleteVideo=DeleteArchiveDirectory()
    actionVideo=ActionVideo()
    actionVideoStore=AddCreateVideoStore()
    listVideo=actionVideo.listVideo()
    actionVideoStore.functionCreateVideoStore('VideoStore')
    actionVideoStore.functionCreateVideoStore('SoundStore')
    actionVideoStore.functionCreateVideoStore('VideoStoreSubtitles')
    actionSound=ActionSound()
    Menu().run()
