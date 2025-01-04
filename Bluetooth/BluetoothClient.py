import bluetooth


class BluetoothClient():

    def recibir_video(self,archivo_destino):
        server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        server_socket.bind(("", bluetooth.PORT_ANY))
        server_socket.listen(1)

        print("Esperando conexión de un dispositivo...")

        client_socket, client_info = server_socket.accept()
        print(f"Conexión aceptada desde {client_info}")

        with open(archivo_destino, 'wb') as f:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    break
                f.write(data)

        print("Video recibido con éxito.")
        client_socket.close()
        server_socket.close()
