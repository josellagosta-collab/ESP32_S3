"""
main_ap.py - Punto de acceso WiFi y servidor web básico para ESP32-S3 (MicroPython)

Funcionalidades:
- Crear punto de acceso (AP) con SSID y contraseña configurables
- Mostrar IP del AP
- Servidor HTTP mínimo para permitir futuras conexiones web
- Manejo de errores y reactivación del AP si se cae

Edite `AP_SSID` y `AP_PASSWORD` según desee.
"""

import network
import socket
import time

# --- Configuración del AP ---
AP_SSID = "ESP32_AP"
AP_PASSWORD = "12345678"  # mínimo 8 caracteres para WPA2
CHANNEL = 6
AUTHMODE = 3  # 0=open, 1=WEP, 2=WPA-PSK, 3=WPA2-PSK

# Retrasos
RESTART_DELAY = 3

ap = network.WLAN(network.AP_IF)

def start_ap():
    try:
        if not ap.active():
            ap.active(True)

        ap.config(essid=AP_SSID, password=AP_PASSWORD, channel=CHANNEL, authmode=AUTHMODE)
        time.sleep(1)
        ip_info = ap.ifconfig()
        print("AP activo. IP:", ip_info[0])
        return True
    except Exception as e:
        print("Excepción al activar AP:", e)
        return False

def stop_ap():
    try:
        if ap.active():
            ap.active(False)
            print("AP desactivado")
    except Exception as e:
        print("Excepción en stop_ap():", e)

def simple_http_server(host='0.0.0.0', port=80):
    html = """
<html>
  <head><title>ESP32 AP</title></head>
  <body>
    <h1>ESP32-S3 AP</h1>
    <p>SSID: {ssid}</p>
    <p>IP: {ip}</p>
    <p>Conecte un navegador para futuras interacciones.</p>
  </body>
</html>
""".format(ssid=AP_SSID, ip=ap.ifconfig()[0])

    addr_info = socket.getaddrinfo(host, port)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr_info)
    s.listen(1)
    print('Servidor HTTP escuchando en', addr_info)

    try:
        while True:
            cl, addr = s.accept()
            print('Cliente conectado desde', addr)
            try:
                cl_file = cl.makefile('rwb', 0)
                # Leer petición (cabeceras) y descartar
                while True:
                    line = cl_file.readline()
                    if not line or line == b'\r\n':
                        break

                response = 'HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n' + html
                cl.send(response)
            except Exception as e:
                print('Error manejando cliente:', e)
            finally:
                try:
                    cl.close()
                except:
                    pass

    except Exception as e:
        print('Excepción en servidor HTTP:', e)
    finally:
        try:
            s.close()
        except:
            pass

def main():
    while True:
        if start_ap():
            try:
                simple_http_server()
            except Exception as e:
                print('Servidor terminó con excepción:', e)
                print('Reiniciando servidor en {}s...'.format(RESTART_DELAY))
                time.sleep(RESTART_DELAY)
                # Intentar reactivar AP en caso de fallo
                try:
                    stop_ap()
                    time.sleep(1)
                except:
                    pass
        else:
            print('No se pudo arrancar el AP, reintentando en {}s...'.format(RESTART_DELAY))
            time.sleep(RESTART_DELAY)

if __name__ == '__main__':
    main()
