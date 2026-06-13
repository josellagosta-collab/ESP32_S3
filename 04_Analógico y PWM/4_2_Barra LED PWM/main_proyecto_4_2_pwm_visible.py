"""
Proyecto 4.2 - Barra LED con PWM visible
ESP32-S3 WROOM + MicroPython

Este programa mejora el efecto anterior.
Ahora cada LED aumenta y disminuye gradualmente su brillo usando PWM,
por lo que el efecto PWM se aprecia mucho mejor.

IMPORTANTE:
Se usan 8 LEDs porque esta versión de MicroPython en ESP32-S3
indica un límite de 8 canales PWM.

Conexiones:
LED 1 -> GPIO 4
LED 2 -> GPIO 5
LED 3 -> GPIO 6
LED 4 -> GPIO 7
LED 5 -> GPIO 15
LED 6 -> GPIO 16
LED 7 -> GPIO 17
LED 8 -> GPIO 18
"""

from machine import Pin, PWM
import time

# Pines usados para los 8 LEDs
pines_led = [4, 5, 6, 7, 15, 16, 17, 18]

# Crear objetos PWM
leds = []

for pin in pines_led:
    led = PWM(Pin(pin))
    led.freq(1000)
    led.duty_u16(0)
    leds.append(led)

# Parámetros del efecto
BRILLO_MIN = 0
BRILLO_MAX = 65535
PASO_BRILLO = 2500
RETARDO_FADE_MS = 8
RETARDO_ENTRE_LEDS_MS = 20


def apagar_todos():
    """Apaga todos los LEDs."""
    for led in leds:
        led.duty_u16(0)


def fade_led(led):
    """Sube y baja progresivamente el brillo de un LED."""

    # Subida progresiva de brillo
    for brillo in range(BRILLO_MIN, BRILLO_MAX, PASO_BRILLO):
        led.duty_u16(brillo)
        time.sleep_ms(RETARDO_FADE_MS)

    # Bajada progresiva de brillo
    for brillo in range(BRILLO_MAX, BRILLO_MIN, -PASO_BRILLO):
        led.duty_u16(brillo)
        time.sleep_ms(RETARDO_FADE_MS)

    led.duty_u16(0)


try:
    while True:

        # Movimiento de izquierda a derecha
        for led in leds:
            fade_led(led)
            time.sleep_ms(RETARDO_ENTRE_LEDS_MS)

        # Movimiento de derecha a izquierda
        for led in reversed(leds):
            fade_led(led)
            time.sleep_ms(RETARDO_ENTRE_LEDS_MS)

except KeyboardInterrupt:
    apagar_todos()
    print("Programa detenido. LEDs apagados.")
