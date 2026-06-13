"""
Proyecto: Parpadeo de LED con ESP32-S3 WROOM y MicroPython

Conexión del circuito:
  - Ánodo del LED (patilla larga)  -->  GPIO 5 de la ESP32-S3
  - Cátodo del LED (patilla corta)  -->  resistencia de 220 Ω o 330 Ω  -->  GND

Esquema: GPIO 5 ----> ánodo LED ----> cátodo LED ----> resistencia ----> GND
"""

from machine import Pin
import time

# Configurar GPIO 5 como salida digital para controlar el LED externo
led = Pin(5, Pin.OUT)

# Bucle infinito: encender y apagar el LED cada segundo
while True:
    led.value(1)       # Encender el LED (nivel alto en GPIO 5)
    time.sleep(1)      # Mantener encendido durante 1 segundo
    led.value(0)       # Apagar el LED (nivel bajo en GPIO 5)
    time.sleep(1)      # Mantener apagado durante 1 segundo
