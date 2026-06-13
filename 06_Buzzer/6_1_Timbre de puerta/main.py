from machine import Pin
import time

# Configuración del pulsador en GPIO 2 como entrada con pull-up interno
button = Pin(2, Pin.IN, Pin.PULL_UP)

# Configuración de la salida para controlar la base del transistor S8050 en GPIO 1
buzzer = Pin(1, Pin.OUT)

# Estado inicial: apagado
buzzer.value(0)

# Bucle principal que comprueba el estado del botón continuamente
while True:
    # El pulsador está conectado a GND y usa pull-up, por lo que
    # cuando se pulsa el botón el valor es 0 (LOW) y cuando está suelto es 1 (HIGH).
    if button.value() == 0:
        # Cuando el botón está pulsado, activamos el transistor
        # y el zumbador suena mientras se mantiene pulsado.
        buzzer.value(1)
    else:
        # Cuando el botón está suelto, desactivamos el transistor
        # y el zumbador deja de sonar inmediatamente.
        buzzer.value(0)

    # Pequeña pausa para evitar lecturas muy rápidas del botón
    time.sleep(0.01)
