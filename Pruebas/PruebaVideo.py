import cv2
import numpy as np
import time

# Ruta del archivo de video
video_path = '../VideoStore/LockBoxPC.mp4'

# Crear el objeto VideoCapture
capture = cv2.VideoCapture(video_path)

# Verificar si el video se abrió correctamente
if not capture.isOpened():
    print("Error: No se puede abrir el video.")
    exit()

# Variables para controlar la pausa
is_paused = False
paused_frame = None

while True:
    # Esperar a que el usuario presione una tecla para pausar o reanudar el video
    key = cv2.waitKey(1) & 0xFF

    if key == ord('p'):  # Presionar 'p' para pausar/reanudar
        is_paused = not is_paused
        print("Pausado" if is_paused else "Reanudado")

    if is_paused:
        # Si está pausado, no leer el siguiente frame, simplemente mostrar el frame actual
        if paused_frame is not None:
            cv2.imshow('Video', paused_frame)
        continue

    # Leer el siguiente frame
    ret, frame = capture.read()

    if not ret:
        print("Fin del video.")
        break

    # Mostrar el frame
    cv2.imshow('Video', frame)

    # Guardar el frame para mostrarlo cuando se pause
    paused_frame = frame

    # Salir si el usuario presiona 'q'
    if key == ord('q'):
        break

# Liberar recursos
capture.release()
cv2.destroyAllWindows()
