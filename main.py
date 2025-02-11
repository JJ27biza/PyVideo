from Directory.DeleteArchiveDirectory import DeleteArchiveDirectory
from ModificText import ModificText
from Directory.AddArchiveDirectory import AddArchiveDirectory
from Directory.OpenDirectory import OpenDirectory
import ModificText as delete
import Directory.AddArchiveDirectory as addDirectory
import VideoReproduce as video
from VideoReproduce import VideoReproduce
import Directory.DeleteArchiveDirectory as deleteVideo
import pyvolume
import serverFake as es

def añadirVideo():
    o.run()
    url_video=delete.functionDeleteText(o.label.text)
    url_correcta=delete.functionValidationUrl(url_video)
    addD.functionAddArchiveDirectory(url_correcta,"../VideoStore")
def verVideo():
    video.capturaVideo('VideoStore/LockBoxAndroid.mp4')
def borrarVideo():
    deleteVideo.functionDeleteArchive('VideoStore/LockBoxAndroid.mp4')
if __name__ == '__main__':
   es.apagarServidor()  # Puedes descomentar esta línea para apagar el servidor después de un tiempo



    #verVideo()


