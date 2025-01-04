import bluetooth

class BluetoothServer():

    def enviar_video(self,archivo, mac_destino):
        socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        socket.connect((mac_destino, 1))

        with open(archivo, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                socket.send(data)

        print("Video enviado con éxito.")
        socket.close()


