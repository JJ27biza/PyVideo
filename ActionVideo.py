import os
class ActionVideo():
    #Este metodo obtiene una lista de los video que se encuentran en VideoStore
    def listVideo(self):
        try:
            project_dir = os.path.dirname(os.path.abspath(__file__))
            video_directory = os.path.join(project_dir, 'VideoStore')
            contenido = os.listdir(video_directory)
            return contenido
        except Exception as error:
            print('Error al hacer la lista de videos',error)
    #Este metodo obtiene una lista de los video que se encuentran en VideoStoreSubtitles
    def listVideoSubtitulos(self):
        try:
            project_dir = os.path.dirname(os.path.abspath(__file__))
            video_directory = os.path.join(project_dir, 'VideoStoreSubtitles')
            contenido = os.listdir(video_directory)
            return contenido
        except Exception as error:
            print('Error al hacer la lista de videos', error)
