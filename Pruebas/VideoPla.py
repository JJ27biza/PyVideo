import pygame
import cv2
from kivy.graphics.texture import Texture
from kivy.clock import Clock

class VideoPlayer:
    def __init__(self):
        self.capture = None
        self.video_path = ''
        self.pauseAction = False
        self.buttonPlay = None  # Este debería ser un botón en tu interfaz Kivy
        self.video_time = 0  # Mantener la posición del video
        self.paused_frame = None  # Para mantener el último frame pausado
        pygame.mixer.init()

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

            # Mantener el tiempo actual del video (en segundos)
            self.video_time = self.capture.get(cv2.CAP_PROP_POS_MSEC) / 1000

            # Reproducir el audio solo una vez al principio (si no está en reproducción)
            if not pygame.mixer.music.get_busy():
                pygame.mixer.music.play(loops=0, start=self.video_time)

        else:
            # Si el video ha terminado (ret es False), mostrar la imagen final y detener el audio
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
        pygame.mixer.music.stop()  # Detener el audio cuando termina el video
        self.capture.release()

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
                    audio_path = '../SoundStore/' + listVideo[numero] + '_audio.mp3'
                    pygame.mixer.music.load(audio_path)

                    # Reproducir el audio desde el inicio y sincronizar con el video
                    pygame.mixer.music.play(loops=0, start=0.0)

                    # Comenzar la actualización del video
                    Clock.schedule_interval(self.update, 1.0 / 30.0)

                else:
                    print('Reproducir solo el audio')
                    pygame.mixer.music.play(loops=0, start=self.video_time)  # Comienza el audio desde el tiempo actual del video

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

    def resume_video(self):
        # Reanudar el video y el audio desde el tiempo guardado
        pygame.mixer.music.unpause()  # Reanudar el audio
        self.capture.set(cv2.CAP_PROP_POS_FRAMES, self.video_time * 30)  # Reanudar el video en la posición correcta
        Clock.schedule_interval(self.update, 1.0 / 30.0)  # Reanudar la actualización del video
