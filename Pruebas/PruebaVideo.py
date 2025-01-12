import cv2
from kivy.app import App
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from kivy.clock import Clock
from Directory.DeleteArchiveDirectory import DeleteArchiveDirectory
from Directory.OpenDirectory import OpenDirectory
from Directory.AddCreateVideoStore import AddCreateVideoStore
import Directory.DeleteArchiveDirectory as deleteVideo
from ModificText import ModificText
from Directory.AddArchiveDirectory import AddArchiveDirectory
from ActionVideo import ActionVideo
from ControlSound.ActionSound import ActionSound

class VideoApp(App):
    def build(self):
        # Creamos un widget de imagen que se usará para mostrar el video
        self.img = Image()
        # Abrimos la cámara o el archivo de video (0 es la cámara predeterminada)
        self.capture = cv2.VideoCapture('../VideoStore/SuperSalto.mkv')

        # Verificamos si la cámara o el archivo se abrió correctamente
        if not self.capture.isOpened():
            print("Error al abrir la cámara o el archivo de video.")
            return

        # Iniciamos el reloj de Kivy para actualizar la imagen
        Clock.schedule_interval(self.update_frame, 1.0 / 30.0)  # 30 FPS

        return self.img

    def update_frame(self, dt):
        # Leemos el siguiente cuadro del video
        ret, frame = self.capture.read()

        if ret:
            # Convertimos el cuadro de BGR (OpenCV) a RGB (Kivy)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.flip(frame, 0)

            # Creamos una textura a partir del cuadro y la asignamos al widget Image
            texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
            texture.blit_buffer(frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            # Asignamos la textura a la imagen
            self.img.texture = texture

    def on_stop(self):
        # Cerramos el video cuando la aplicación se detiene
        if self.capture.isOpened():
            self.capture.release()

if __name__ == "__main__":
    VideoApp().run()
