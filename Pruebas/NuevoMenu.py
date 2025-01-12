from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.video import Video
from kivy.uix.videoplayer import VideoPlayer
from kivy.uix.button import Button
from kivy.clock import Clock

class VideoApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        # Crear un VideoPlayer inicial
        self.video_player = VideoPlayer(source='../VideoStore/profe.mkv', state='play')
        self.layout.add_widget(self.video_player)

        # Crear un botón para cambiar el video
        self.change_button = Button(text="Cambiar a Video")
        self.change_button.bind(on_press=self.change_to_video)
        self.layout.add_widget(self.change_button)

        return self.layout

    def change_to_video(self, instance):
        # Guardar la posición actual del video
        current_position = self.video_player.position

        # Detener el VideoPlayer
        self.video_player.state = 'stop'

        # Remover el VideoPlayer del layout
        self.layout.remove_widget(self.video_player)

        # Crear un nuevo widget Video y configurar su fuente
        self.video = Video(source='../VideoStore/profe.mkv', state='play', allow_stretch=True, keep_ratio=False)

        # Crear un temporizador para que el Video esté cargado antes de hacer el seek
        Clock.schedule_once(lambda dt: self.resume_video(current_position), 0.1)

        # Añadir el nuevo Video al layout
        self.layout.add_widget(self.video)

    def resume_video(self, current_position):
        # Ahora que el video está cargado, reanudar la reproducción desde la posición anterior
        self.video.seek(current_position)
        self.video.state = 'play'

if __name__ == "__main__":
    VideoApp().run()
