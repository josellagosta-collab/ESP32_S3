"""
main.py - Conexión WiFi con reconexión automática para ESP32-S3 (MicroPython)

Requisitos implementados:
- Conectar a WiFi
- Mostrar IP
- Gestionar errores
- Reconectar automáticamente

Edite las variables `SSID` y `PASSWORD` abajo según su red.
Guarde como `main.py` en la raíz del dispositivo para ejecución automática al arrancar.
"""

import network
import time
from machine import reset

# --- Configuración ---
SSID = "CASAAGUILERA_XIOAMI"
PASSWORD = "CARLOSFUERA1996#2017"

# Retrasos y límites (segundos)
RETRY_DELAY = 5
CONNECT_TIMEOUT = 15
MAX_RETRIES = 5

wlan = network.WLAN(network.STA_IF)

def connect(timeout=CONNECT_TIMEOUT):
    try:
        if not wlan.active():
            wlan.active(True)

        if wlan.isconnected():
            return True

        print("Conectando a WiFi: {}".format(SSID))
        wlan.connect(SSID, PASSWORD)

        start = time.time()
        while not wlan.isconnected():
            time.sleep(1)
            if time.time() - start > timeout:
                print("Timeout de conexión ({}s)".format(timeout))
                return False

        return True

    except Exception as e:
        print("Excepción en connect():", e)
        return False

def show_ip():
    try:
        if wlan.isconnected():
            ip, mask, gateway, dns = wlan.ifconfig()
            print("Conectado. IP:", ip)
            return ip
        else:
            print("No hay conexión WiFi.")
            return None
    except Exception as e:
        print("Excepción en show_ip():", e)
        return None

def main():
    retries = 0
    while True:
        try:
            ok = connect()
            if ok:
                retries = 0
                show_ip()

                # Monitoriza la conexión; si se pierde, salimos al bucle de reconexión
                while wlan.isconnected():
                    time.sleep(5)

                print("Conexión perdida, intentaremos reconectar...")

            else:
                retries += 1
                print("Intento fallido de conexión #{}".format(retries))
                if retries >= MAX_RETRIES:
                    print("Máximos reintentos alcanzados, reiniciando dispositivo...")
                    time.sleep(2)
                    reset()
                time.sleep(RETRY_DELAY)

        except Exception as e:
            print("Excepción en main():", e)
            time.sleep(RETRY_DELAY)

if __name__ == '__main__':
    main()
