# Proyecto 3: Luz en movimiento con barra LED
# ESP32-S3 WROOM - MicroPython
# Efecto de luz en movimiento en una barra de 10 LEDs

# Importar las librerías necesarias
from machine import Pin
import time

# Lista con los pines GPIO conectados a la barra LED
# Cada número representa un pin GPIO del ESP32-S3
pines_led = [4, 5, 6, 7, 15, 16, 17, 18, 8, 3]

# Crear objetos Pin para cada LED
# mode=Pin.OUT: configurar cada pin como SALIDA (output)
leds = []
for pin in pines_led:
    leds.append(Pin(pin, Pin.OUT))

# Apagar todos los LEDs al iniciar el programa
# Led apagado = valor 0
for led in leds:
    led.value(0)

# Tiempo de espera entre cambios de LED (en segundos)
# 0.1 segundos = 100 milisegundos
tiempo_espera = 0.1

# Bucle infinito para crear el efecto de luz en movimiento
while True:
    # Recorrer cada LED en la lista
    for led in leds:
        # Encender el LED actual
        # Led encendido = valor 1
        led.value(1)
        
        # Esperar el tiempo definido (LED encendido)
        time.sleep(tiempo_espera)
        
        # Apagar el LED actual
        # Led apagado = valor 0
        led.value(0)
        
        # El siguiente LED se encenderá automáticamente en la siguiente iteración
        # Esto crea el efecto de luz en movimiento

# El programa se ejecutará indefinidamente
# Para detener: pulsa Ctrl+C en la consola de MicroPython o desconecta el ESP32-S3
