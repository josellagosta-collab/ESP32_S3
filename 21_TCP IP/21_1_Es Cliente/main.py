import network
import socket
import time

# Ajusta estos valores según tu red y servidor
SSID = "TU_SSID"
PASSWORD = "TU_PASSWORD"
HOST = "192.168.1.100"
PORT = 5000
MESSAGE = "Hola servidor"


def connect_wifi(ssid, password, timeout=20):
    wlan = network.WLAN(network.STA_IF)
    if not wlan.active():
        wlan.active(True)

    if not wlan.isconnected():
        print("Conectando a WiFi...", ssid)
        wlan.connect(ssid, password)

        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > timeout:
                raise OSError("No se pudo conectar a la red WiFi")
            time.sleep(1)

    print("WiFi conectado")
    print("Dirección IP:", wlan.ifconfig()[0])
    return wlan


def tcp_client(host, port, message):
    print("Creando socket TCP...")
    addr_info = socket.getaddrinfo(host, port)
    if not addr_info:
        raise OSError("No se pudo resolver la dirección del servidor")

    addr = addr_info[0][-1]
    client = socket.socket()
    client.settimeout(10)

    try:
        print("Conectando al servidor {}:{}...".format(host, port))
        client.connect(addr)
        print("Conectado al servidor")

        payload = message.encode("utf-8")
        print("Enviando texto:", message)
        client.send(payload)

        print("Esperando respuesta...")
        data = client.recv(1024)
        if data:
            print("Respuesta recibida:", data.decode("utf-8", "replace"))
        else:
            print("No se recibió respuesta del servidor")

    finally:
        client.close()
        print("Socket cerrado")


if __name__ == "__main__":
    try:
        connect_wifi(SSID, PASSWORD)
        tcp_client(HOST, PORT, MESSAGE)
    except OSError as error:
        print("Error de red:", error)
    except Exception as error:
        print("Error inesperado:", error)
    finally:
        print("Programa finalizado")
