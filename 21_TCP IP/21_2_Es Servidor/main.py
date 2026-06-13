import network
import socket
import time

# Ajusta estos valores según tu red WiFi
SSID = "TU_SSID"
PASSWORD = "TU_PASSWORD"
HOST = ""
PORT = 5000
RESPONSE = "Mensaje recibido"


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


def start_tcp_server(host, port):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen(1)
    print(f"Servidor TCP escuchando en puerto {port}")
    return server


def run_server(server):
    try:
        while True:
            print("Esperando cliente...")
            conn, addr = server.accept()
            print("Cliente conectado desde:", addr)
            conn.settimeout(10)

            try:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        print("Cliente desconectado")
                        break

                    message = data.decode("utf-8", "replace")
                    print("Mensaje recibido:", message)

                    print("Enviando respuesta...")
                    conn.send(RESPONSE.encode("utf-8"))

            except OSError as error:
                print("Error de conexión con el cliente:", error)
            finally:
                conn.close()
                print("Conexión cerrada")

    except KeyboardInterrupt:
        print("Servidor detenido por el usuario")
    finally:
        server.close()
        print("Socket del servidor cerrado")


if __name__ == "__main__":
    try:
        connect_wifi(SSID, PASSWORD)
        server_socket = start_tcp_server(HOST, PORT)
        run_server(server_socket)
    except OSError as error:
        print("Error de red:", error)
    except Exception as error:
        print("Error inesperado:", error)
    finally:
        print("Programa finalizado")
