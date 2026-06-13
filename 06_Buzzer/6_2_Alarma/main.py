from machine import Pin, PWM
import time

# Configuración del botón en GPIO 2 como entrada con resistencia pull-up interna.
boton = Pin(2, Pin.IN, Pin.PULL_UP)

# Configuración del buzzer pasivo en GPIO 1 usando PWM.
buzzer = PWM(Pin(1))
buzzer.freq(1000)        # Frecuencia inicial de 1000 Hz
buzzer.duty_u16(0)       # Comenzar con el buzzer apagado

# Bucle principal que se ejecuta indefinidamente.
while True:
    # El botón está conectado a GND cuando se pulsa, por lo que su valor es 0 al pulsarlo.
    if boton.value() == 0:
        # Activar sonido en el buzzer pasivo
        buzzer.duty_u16(32768)
    else:
        # Apagar el buzzer cuando el botón no está pulsado
        buzzer.duty_u16(0)

    # Pequeña pausa para estabilizar la lectura del botón y evitar lecturas demasiado rápidas.
    time.sleep_ms(10)
