import network
import time
import machine

SSID = "CASAAGUILERA_XIOAMI"
PASSWORD = "CARLOSFUERA1996#2017"

print("Intentando conectar a WiFi...")
print("SSID:", SSID)

wlan = network.WLAN(network.STA_IF)

# Reinicio limpio de la interfaz WiFi
wlan.active(False)
time.sleep(1)

wlan.active(True)
time.sleep(1)

# Si ya estaba conectado, desconectamos antes
if wlan.isconnected():
    wlan.disconnect()
    time.sleep(1)

try:
    wlan.connect(SSID, PASSWORD)

    timeout = 20

    while not wlan.isconnected() and timeout > 0:
        print("Conectando...")
        time.sleep(1)
        timeout -= 1

    if wlan.isconnected():
        print("WiFi conectado correctamente")
        print("Datos de red:", wlan.ifconfig())
        print("IP del ESP32-S3:", wlan.ifconfig()[0])
    else:
        print("No se pudo conectar a la WiFi")
        print("Comprueba SSID, contraseña y que la red sea de 2.4 GHz")

except OSError as e:
    print("Error interno WiFi:", e)
    print("Reiniciando ESP32-S3 en 5 segundos...")
    time.sleep(5)
    machine.reset()