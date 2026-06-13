from machine import Pin, PWM
import random
import time

# Configuración de los pines PWM para cada color del LED RGB.
# Según el proyecto, usamos:
# - GPIO 42 para el rojo
# - GPIO 41 para el verde
# - GPIO 40 para el azul
rojo = PWM(Pin(42))
verde = PWM(Pin(41))
azul = PWM(Pin(40))

# Establecemos la frecuencia PWM en 1000 Hz para los tres canales.
for led in (rojo, verde, azul):
    led.freq(1000)

# Bucle principal: genera un color nuevo cada segundo de forma indefinida.
while True:
    # Generar valores aleatorios para cada canal PWM.
    # duty_u16 acepta valores entre 0 (apagado) y 65535 (brillo máximo).
    rojo.duty_u16(random.randint(0, 65535))
    verde.duty_u16(random.randint(0, 65535))
    azul.duty_u16(random.randint(0, 65535))

    # Mantener el color actual durante 1 segundo.
    time.sleep(1)
