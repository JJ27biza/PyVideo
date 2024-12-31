import cv2

class VideoReproduce():

    def capturaVideo(self,fichero):

        captura = cv2.VideoCapture(fichero)

        if not captura.isOpened():
            print("Error al abrir el video.")
            return

        cv2.namedWindow('Video', cv2.WINDOW_FULLSCREEN)

        while True:
            ret, imagen = captura.read()

            if not ret:
                print("Se ha alcanzado el final del video o ocurrió un error.")
                break
            cv2.imshow('Video', imagen)

            key = cv2.waitKey(30) & 0xFF

            if key == 27:
                break
            if cv2.getWindowProperty('Video', cv2.WND_PROP_VISIBLE) < 1:
                break

        captura.release()
        cv2.destroyAllWindows()