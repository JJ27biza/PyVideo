import time  # Asegúrate de importar la librería 'time'
from zeroconf import Zeroconf, ServiceBrowser

class ChromecastListener:
    def __init__(self):
        self.discovered_devices = []

    def add_service(self, zeroconf, type, name):
        if "_googlecast._tcp.local." in type:
            print(f"Chromecast encontrado: {name}")
            self.discovered_devices.append(name)

    def remove_service(self, zeroconf, type, name):
        print(f"Se eliminó el servicio: {name}")
        self.discovered_devices.remove(name)

    # Agregar el método vacío 'update_service' para evitar la advertencia
    def update_service(self, zeroconf, type, name):
        pass  # Este método se deja vacío si no necesitas manejar las actualizaciones de servicios

def listar_chromecasts():
    zeroconf_instance = Zeroconf()
    listener = ChromecastListener()

    browser = ServiceBrowser(zeroconf_instance, "_googlecast._tcp.local.", listener)

    # Buscar dispositivos durante 30 segundos
    print("Buscando dispositivos Chromecast...")
    try:
        # Usamos un tiempo de espera para permitir la detección
        time.sleep(30)
    except KeyboardInterrupt:
        pass
    finally:
        zeroconf_instance.close()

    if listener.discovered_devices:
        print("Dispositivos Chromecast encontrados:")
        for device in listener.discovered_devices:
            print(device)
    else:
        print("No se encontraron dispositivos Chromecast.")

if __name__ == "__main__":
    listar_chromecasts()
