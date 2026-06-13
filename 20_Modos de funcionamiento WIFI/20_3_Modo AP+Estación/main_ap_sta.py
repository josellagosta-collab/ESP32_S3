"""
main_ap_sta.py - Modo AP + STA para ESP32-S3 (MicroPython)

Funcionalidades:
- Activa STA y AP simultáneamente
- Conecta STA a una red WiFi (con reintentos)
- Crea un AP con SSID/Password configurable
- Muestra ambas IPs (STA y AP)
- Ejecuta un servidor HTTP sencillo que muestra ambas IPs
- Maneja errores y reconecta automáticamente

Configure `SSID`, `PASSWORD`, `AP_SSID` y `AP_PASSWORD` abajo.
"""

import network
import socket
import time
from machine import reset

# --- Configuración ---
SSID = "MiWiFi"
PASSWORD = "12345678"

AP_SSID = "ESP32_AP"
AP_PASSWORD = "12345678"

RETRY_DELAY = 5
CONNECT_TIMEOUT = 15
MAX_RETRIES = 5

sta = network.WLAN(network.STA_IF)
ap = network.WLAN(network.AP_IF)

def start_ap():
    try:
        if not ap.active():
            ap.active(True)
        ap.config(essid=AP_SSID, password=AP_PASSWORD)
        time.sleep(1)
        print('AP activo, IP:', ap.ifconfig()[0])
        return True
    except Exception as e:
        print('Error start_ap():', e)
        return False

def connect_sta(timeout=CONNECT_TIMEOUT):
    try:
        if not sta.active():
            sta.active(True)

        if sta.isconnected():
            return True

        print('Conectando STA a:', SSID)
        sta.connect(SSID, PASSWORD)
        start = time.time()
        while not sta.isconnected():
            time.sleep(1)
            if time.time() - start > timeout:
                print('Timeout conexión STA')
                return False
        print('STA conectada, IP:', sta.ifconfig()[0])
        return True
    except Exception as e:
        print('Error connect_sta():', e)
        return False

def show_ips():
    try:
        sta_ip = sta.ifconfig()[0] if sta.active() and sta.isconnected() else 'No conectado'
    except Exception as e:
        sta_ip = 'Error'
        print('show_ips STA error:', e)

    try:
        ap_ip = ap.ifconfig()[0] if ap.active() else 'AP inactivo'
    except Exception as e:
        ap_ip = 'Error'
        print('show_ips AP error:', e)

    print('STA IP:', sta_ip)
    print('AP  IP:', ap_ip)
    return sta_ip, ap_ip

def simple_http_server():
    sta_ip, ap_ip = show_ips()
    html = """
<html>
  <head><meta charset='utf-8'><title>ESP32 AP+STA</title></head>
  <body>
    <h1>ESP32-S3 - AP + STA</h1>
    <p><strong>STA IP:</strong> {sta}</p>
    <p><strong>AP IP:</strong> {ap}</p>
    <p>Use esta página como punto de partida para futuras conexiones web.</p>
  </body>
</html>
""".format(sta=sta_ip, ap=ap_ip)

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    print('Servidor HTTP escuchando en', addr)

    try:
        while True:
            cl, addr = s.accept()
            print('Cliente desde', addr)
            try:
                cl_file = cl.makefile('rwb', 0)
                # consumir petición
                while True:
                    line = cl_file.readline()
                    if not line or line == b'\r\n':
                        break

                response = 'HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n' + html
                cl.send(response)
            except Exception as e:
                print('Error manejando cliente:', e)
            finally:
                try:
                    cl.close()
                except:
                    pass

    except Exception as e:
        print('Servidor HTTP error:', e)
    finally:
        try:
            s.close()
        except:
            pass

def main():
    retries = 0
    while True:
        try:
            # Asegurar AP activo
            if not start_ap():
                print('No se pudo activar AP, reintentando...')
                time.sleep(RETRY_DELAY)
                continue

            # Conectar STA (puede estar desconectada, intentamos reconectar)
            if not connect_sta():
                retries += 1
                print('Fallo conexión STA, intento', retries)
                if retries >= MAX_RETRIES:
                    print('Máximos reintentos alcanzados, reiniciando...')
                    time.sleep(2)
                    reset()
                time.sleep(RETRY_DELAY)
                continue
            else:
                retries = 0

            # Mostrar IPs y servir
            show_ips()
            simple_http_server()

        except Exception as e:
            print('Excepción en main():', e)
            time.sleep(RETRY_DELAY)

if __name__ == '__main__':
    main()
