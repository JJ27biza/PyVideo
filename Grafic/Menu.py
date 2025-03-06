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
import Emision.ListIssue as lista
import Emision.IssueLocal as emitirLocal
import Emision.IssueYouTube as emitiryt
import Emision.DisconnectLocal as desconexion
import cv2
import numpy as np
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import pygame
import AudioExtraction as audio
import serverFake as sf
import UrlDescarga as ud
from threading import Thread, Event
import time
import pychromecast





class Menu(App):
    #Construccion gráfica de la aplicación
    def build(self):
        #Varibale "globales"
        self.capture = None
        self.pauseAction = False
        self.buttonPlay = None
        self.audio_started = False
        self.url_yt_pop=None
        self.listSubtitules=[]
        self.video_path = '../Image/pause.png'
        self.sound_path=None
        self.buttonPlay = None
        self.video_time = 0
        self.paused_frame = None
        self.error_Borrado=False
        self.hilo_server=None
        self.arrayListar=lista.listar_chromecasts()
        self.ip=None
        self.actionSubtitules = True
        self.nombreSubtitulos = None
        self.last_audio_time = 0
        self.last_sync_time = time.time()
        self.sync_threshold = 0.1
        self.sync_interval = 0.5
        self.last_audio_adjustment = time.time()
        self.emision_activa = False

        pygame.mixer.init()
        Window.maximize()
        Window.clearcolor = (0.2, 0.3, 0.4, 1)
        Window.bind(on_request_close=self.on_cerrar)
        self.title = 'PyVideo'

        self.layout = BoxLayout(orientation='vertical')

        self.boxNav = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        self.boxBack = BoxLayout(orientation='horizontal', size_hint=(0.5, 0.1))
        self.boxBack.pos_hint={'center_x': 0.5, 'center_y': 0.5}
        self.box = BoxLayout(orientation='horizontal', size_hint=(1, 0.8))
        ############################Botones y video###################################
        # Botón Añadir
        self.buttonAñadir = Button(text="Añadir", size_hint=(0.1, 1))
        self.buttonAñadir.bind(on_press=self.on_press_Añadir)
        self.boxNav.add_widget(self.buttonAñadir)
        # Botón Enviar Video
        self.buttonEnviar=Button(text="Enviar Video",size_hint=(0.1,1))

        self.buttonEnviar.bind(on_press=self.open_popup_Server_Output)

        self.boxNav.add_widget(self.buttonEnviar)

        self.buttonRecibir = Button(text="Recibir Video", size_hint=(0.1, 1))
        self.buttonRecibir.bind(on_press=self.open_popup_Server_Inputput)
        self.boxNav.add_widget(self.buttonRecibir)
        #Dropdown para ver los dispositivos disponibles para conectarse con Chromecast
        self.dropdown = DropDown()
        if self.arrayListar==None or self.arrayListar==0:
            self.arrayListar=''
        for index in enumerate(self.arrayListar):
            self.btn = Button(text=str(index[1]), size_hint_y=None, height=44)
            self.btn.bind(on_release=lambda btn=self.btn: self.dropdown.select(btn.text))
            self.dropdown.add_widget(self.btn)
        self.dropdown.bind(on_select=lambda instance, x: self.emision_local(x))
        #Segundo Dropdown para los dispositivos para la emision YouTube
        self.dropdownyt = DropDown()
        if self.arrayListar==None or self.arrayListar==0:
            self.arrayListar=''
        for index in enumerate(self.arrayListar):
            self.btn = Button(text=str(index[1]), size_hint_y=None, height=44)
            self.btn.bind(on_release=lambda btn=self.btn: self.dropdownyt.select(btn.text))
            self.dropdownyt.add_widget(self.btn)
        self.dropdownyt.bind(on_select=lambda instance, x:self.open_popup_YT(x) )



        # Botón EmitirLocal
        self.buttonEmitirLocal=Button(text="Emitir Local",size_hint=(0.1,1))
        self.buttonEmitirLocal.bind(on_release=self.dropdown.open)
        self.boxNav.add_widget(self.buttonEmitirLocal)
        # Botón Emitir YouTube
        self.buttonEmitirYouTube=Button(text="Emitir YouTube",size_hint=(0.1,1))
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
        # Button Maximize
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
        # Botón Play
        self.buttonPlay = Button(text="Play", size_hint=(0.5, 1))
        self.buttonPlay.bind(on_press=self.on_button_press)
        self.buttonPlay.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.boxBack.add_widget(self.buttonPlay)
        #Botón Subtitulos
        self.buttonSubtitle = Button(text="Subtitulos", size_hint=(0.5, 1))
        self.buttonSubtitle.bind(on_press=self.load_Subtitules)
        self.buttonSubtitle.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
        self.boxBack.add_widget(self.buttonSubtitle)
        #SeekBar Volumen
        self.slider = Slider(min=0, max=100,value=15,step=1)
        self.slider.bind(on_touch_up=self.return_sound)
        self.boxBack.add_widget(self.slider)
        # Añadir los BoxLayouts al layout principal
        self.layout.add_widget(self.boxNav)
        self.layout.add_widget(self.box)
        self.layout.add_widget(self.boxBack)
        return self.layout
    #Este método permite volver atras para ver el video con una lista de videos
    # moviendo las posiciones de los videos y de los audios correspondientes con el video
    def on_button_atras(self,instance):
        global numero
        try:
            if numero < len(listVideo) + 1:
                numero -= 1
                self.video_path = '../VideoStore/' + listVideo[numero]
                self.sound_path='../SoundStore/'+listVideo[numero]+'_audio.mp3'
                pygame.mixer.music.load('../SoundStore/' + listVideo[numero] + '_audio.mp3')
                self.capture = cv2.VideoCapture(self.video_path)
            else:
                print('No existen más videos')
        except Exception as error:
            print('Error al adelantar el video', error)

    # Este método permite ir hacia delante para ver el video con una lista de videos
    # moviendo las posiciones de los videos y de los audios correspondientes con el video
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
            else:
                print('No existen más videos')
        except Exception as error:
            print('Error al adelantar el video', error)

    #Control del botón de pausa o play para detener o reanudar tanto audio como video sincronizando sus posiciones
    def on_button_press(self, instance):
        if self.capture is None or not self.capture.isOpened():
            if len(listVideo) != 0:
                if self.video_path == '../Image/pause.png':

                    self.video_path = '../VideoStore/' + listVideo[numero]
                    self.capture = cv2.VideoCapture(self.video_path)

                    self.sound_path= '../SoundStore/' + listVideo[numero] + '_audio.mp3'
                    pygame.mixer.music.load(self.sound_path)

                    pygame.mixer.music.play(loops=0, start=0.0)

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
                pygame.mixer.music.pause()
                self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.video_time * 30)

            self.pauseAction = not self.pauseAction
            self.buttonPlay.text = 'Play' if self.pauseAction else 'Pause'

    #Añadir videos al directorio de correspodiente y el audio de ese video
    #Despues de utilizar ese metodo se cierra la aplicacion
    def on_press_Añadir(self,instance):
        global listVideo
        try:
            print("La aplicación se cerrará.")
            self.capture=cv2.VideoCapture(0)
            if self.capture is not None:
                self.capture.release()
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

    #Método modificar el audio del dispositivo con el slider
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

            self.img.pos_hint = {'center_x': 0.5, 'center_y': 0.5}
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
    #Método para la actualización de los frames del video para que se reproduzca y sincronizandolo con el audio
    def update(self, dt):
        if self.capture is None or not self.capture.isOpened():
            return

        if self.pauseAction:
            if self.paused_frame is not None:
                frame = self.paused_frame
                frame = cv2.flip(frame, 0)

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

                self.img.texture = texture
            return

        ret, frame = self.capture.read()

        if ret:
            self.paused_frame = frame

            frame = cv2.flip(frame, 0)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            self.img.texture = texture

            self.video_time = self.capture.get(cv2.CAP_PROP_POS_MSEC) / 1000

            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=0, start=self.video_time)

            current_time = time.time()

            if abs(self.video_time - self.last_audio_time) > self.sync_threshold:
                if current_time - self.last_audio_adjustment > self.sync_interval:
                    pygame.mixer.music.set_pos(self.video_time)
                    self.last_audio_time = self.video_time
                    self.last_audio_adjustment = current_time

        else:
            self.show_end_image()
            pygame.mixer.music.stop()

    #Método para que al finalizar el video mostrar la imagen de pausa
    def show_end_image(self):
        end_image_path = '../Image/pause.png'
        end_image = cv2.imread(end_image_path)
        if end_image is None:
            print("Error: No se pudo leer el frame del video")
            self.error_Borrado=True
        else:
            end_image = cv2.cvtColor(end_image, cv2.COLOR_BGR2RGB)
        texture = Texture.create(size=(end_image.shape[1], end_image.shape[0]), colorfmt='rgb')
        texture.blit_buffer(end_image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

        self.img.texture = texture
        pygame.mixer.music.stop()
        self.capture.release()

    #Metódo para adelantar el video y audio 30 segundos sincronizandolos
    def adelantar_30s(self, instance):
        if self.capture is not None and self.capture.isOpened():
            current_time_ms = self.capture.get(cv2.CAP_PROP_POS_MSEC)
            new_time_ms = current_time_ms + 30000
            self.capture.set(cv2.CAP_PROP_POS_MSEC, new_time_ms)
            new_time_seconds = new_time_ms / 1000
            pygame.mixer.music.set_pos(new_time_seconds)

    #Metódo para atrasar el video y audio 30 segundos sincronizandolos
    def atrasar_30s(self, instance):
        if self.capture is not None and self.capture.isOpened():
            current_time_ms = self.capture.get(cv2.CAP_PROP_POS_MSEC)
            new_time_ms = current_time_ms - 30000
            new_time_ms = max(new_time_ms, 0)
            self.capture.set(cv2.CAP_PROP_POS_MSEC, new_time_ms)
            new_time_seconds = new_time_ms / 1000
            pygame.mixer.music.set_pos(new_time_seconds)

    #Metodo que libera la captura de video al acabar
    def on_stop(self):
        self.capture.release()

    #Método para reanudar el video y audio desde el tiempo guardado
    def resume_video(self):
        pygame.mixer.music.unpause()
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.video_time * 30)
        Clock.schedule_interval(self.update, 1.0 / 30.0)


    #Método para abrir una ventana para la emisión de YouTube
    def open_popup_YT(self, x):
        self.popup_content = BoxLayout(orientation='vertical')

        self.label = Label(text='Añada la url del video de YouTube que desea visualizar')
        self.textinput = TextInput()
        self.close_button = Button(text="Ok")
        self.close_button.bind(on_release=lambda instance: self.close_popup_YT(instance, x))

        self.popup_content.add_widget(self.label)
        self.popup_content.add_widget(self.textinput)
        self.popup_content.add_widget(self.close_button)

        self.popup = Popup(title="Ventana Emergente", content=self.popup_content,
                           size_hint=(None, None), size=(400, 300))
        self.popup.open()

    #Metódo para cerrar la ventana de la emisión de Youtube y emite el video de youtube eliminando la parte de la url no necesaria
    def close_popup_YT(self, instance, x):
        self.popup.dismiss()
        self.url_yt_pop = self.textinput.text
        if self.textinput.text != '':
            delete = "https://www.youtube.com/watch?v="
            self.url_yt_pop = self.url_yt_pop.replace(delete, "")
            emitiryt.emit_in_yt(self.url_yt_pop, x)

    #Método para abrir la ventana del funcinamiento del servidor para poder enviar videos
    def open_popup_Server_Output(self, instance):
        self.popup_content = BoxLayout(orientation='vertical')
        mi_ip = socket.gethostbyname(socket.gethostname())
        if self.video_path != '../Image/pause.png':
            self.label = Label(text='Server ya funcionando durante 1 minuto')
            self.label2 = Label(text='http://' + mi_ip + ':5000/descarga')
            self.close_button = Button(text="Close")
            self.close_button.bind(on_release=lambda instance: self.close_popup_Server(instance))
            self.popup_content.add_widget(self.label)
            self.popup_content.add_widget(self.label2)
            self.popup_content.add_widget(self.close_button)
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
            self.popup = Popup(title="Ventana Server", content=self.popup_content,
                               size_hint=(None, None), size=(400, 300))
            self.popup.open()

    #Método para cerrar la ventana del funcionamiento servidor
    def close_popup_Server(self, instance):
        self.popup.dismiss()  # Cerrar el popup correctamente

    #Metódo para abrir la vetana para introducir la url para descargar el video
    def open_popup_Server_Inputput(self, instance):
        self.popup_content2 = BoxLayout(orientation='vertical')
        self.label = Label(text='Descargar de video indica solo su ip. Ejemplo: 192.168.x.x')
        self.textinput = TextInput()
        self.close_button = Button(text="Ok")

        self.close_button.bind(on_release=lambda instance: self.close_popup_Input(instance))

        self.popup_content2.add_widget(self.label)
        self.popup_content2.add_widget(self.textinput)
        self.popup_content2.add_widget(self.close_button)
        self.popup = Popup(title="Ventana Entrada", content=self.popup_content2,
                           size_hint=(None, None), size=(400, 300))
        self.popup.open()



    #Metódo para cerrar la ventana de la descarga del video y ejecutar la descarga
    def close_popup_Input(self, instance):
        self.popup.dismiss()
        if self.textinput.text != '':
            self.ip=self.textinput.text
            url='http://'+self.ip+':5000/descarga'
            ud.descargar_archivo(url)

    #Este método comprueba si el video ya tiene ese video con subtitulos si no pues se ejecuta el proceso en un hilo para obtener el video con subtitulos
    def load_Subtitules(self, instance):
        global listVideo, numero
        try:

            self.listSubtitules = actionVideo.listVideoSubtitulos()
            nombre = listVideo[numero]
            numero = 0
            self.capture.release()
            pygame.mixer.music.unload()
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            pygame.mixer.init()
            Clock.schedule_once(lambda dt: self.update_image_source('../Image/cargando.png'), 0)

            def process_subtitles_and_video():

                for i in self.listSubtitules:
                    if i == nombre + 'with_subtitles.mp4':
                        self.actionSubtitules = False
                        self.nombreSubtitulos = i
                if self.actionSubtitules:
                    VideoSubtitles.str_Subtitules(nombre)
                    strVideo.srt_To_Video(nombre)

                    deleteVideo.functionDeleteArchive('temp_audio.mp3')
                    deleteVideo.functionDeleteArchive(nombre + '_subtitles.srt')
                    self.video_path = '../Image/pause.png'

                    Clock.schedule_once(lambda dt: self.update_image_source('../Image/pause.png'), 0)

                    self.show_image = False
                else:
                    self.video_path = '../VideoStoreSubtitles/' + self.nombreSubtitulos
                    self.sound_path = '../SoundStore/' + nombre + '_audio.mp3'
                    pygame.mixer.music.load(self.sound_path)
                    self.capture = cv2.VideoCapture(self.video_path)

            processing_thread = Thread(target=process_subtitles_and_video)
            processing_thread.start()

        except Exception as error:
            print('Error en la carga de Subtitulos', error)
    #Metodo para detener la emision en local
    def detener_emision(self, instance, x):
        self.emision_activa=True
        desconexion.desconexion_total(x)
        Clock.schedule_once(lambda dt: self.update_image_source('../Image/pause.png'), 0)
        self.video_path = '../Image/pause.png'
        Clock.schedule_once(lambda dt: self.remove_detener_button(), 0)
#Este metodo borrar el bton de cerrar la emision local
    def remove_detener_button(self):
        self.boxNav.remove_widget(self.buttonDetenerLocal)

    #Este método permite realizar la emisión local del video atraves de un hilo
    def emision_local(self, x):
        global numero
        try:
            numero = 0
            self.capture.release()
            pygame.mixer.music.unload()
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            pygame.mixer.init()
            Clock.schedule_once(lambda dt: self.update_image_source('../Image/cargando.png'), 0)

            def process_emision():
                emitirLocal.emit_in_local(self.video_path, x)

                while not self.emision_activa:
                    pass
                print("Proceso detenido.")


            processing_thread = Thread(target=process_emision)
            processing_thread.start()

            self.buttonDetenerLocal = Button(text="Detener Local", size_hint=(0.1, 1))
            self.buttonDetenerLocal.bind(on_release=lambda instance: self.detener_emision(instance, x))
            self.boxNav.add_widget(self.buttonDetenerLocal)
            self.layout.add_widget(self.boxNav)

        except Exception as error:
            print('Error en la carga de Subtitulos', error)

    #Permite realizar el cambio de imagen para saber como va el proceso
    def update_image_source(self, image_path):
        self.img.source = image_path
        self.img.reload()
    #Método que evita cerrar la ventan si el hilo esta vivo
    def on_cerrar(self, instance):
        if self.hilo_server!=None:
            if self.hilo_server.is_alive():
                return True
        else:
            return False


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
