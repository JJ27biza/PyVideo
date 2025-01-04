from Bluetooth.BluetoothClient import BluetoothClient
from Bluetooth.BluetoothServer import BluetoothServer

if __name__ == '__main__':
  mac_destino = "00:1A:7D:DA:71:13"
  archivo_video = "../VideoStore/SuperSalto.mkv"
  client= BluetoothClient()
  server = BluetoothServer()

