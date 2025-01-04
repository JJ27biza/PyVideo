import os
class ActionVideo():
    def listVideo(self):
        try:
            project_dir = os.path.dirname(os.path.abspath(__file__))
            video_directory = os.path.join(project_dir, 'VideoStore')
            contenido = os.listdir(video_directory)
            return contenido
        except Exception as error:
<<<<<<< HEAD
            print('Error al hacer la lista de videos',error)
=======
            print('Error al hacer la lista de videos',error)
>>>>>>> master
