from machine import Pin
import time

# Configuración de pines
LED_PIN = 5        # LED conectado al GPIO 5
BUTTON_PIN = 4     # Pulsador conectado al GPIO 4 y a GND
DEBOUNCE_MS = 50   # Tiempo de antirrebote en milisegundos

# Inicializar LED como salida
led = Pin(LED_PIN, Pin.OUT)

# Inicializar botón como entrada con resistencia interna pull-up
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

# Estado actual del LED (False = apagado, True = encendido)
led_state = False
led.value(0)

def toggle_led():
    global led_state
    led_state = not led_state
    led.value(1 if led_state else 0)


def wait_for_release():
    # Espera hasta que el botón sea soltado (leer 1)
    while button.value() == 0:
        time.sleep_ms(10)


def main_loop():
    # Bucle principal
    while True:
        # Detectar pulsación (activo bajo: 0 cuando se pulsa)
        if button.value() == 0:
            # Pequeña espera para eliminar rebotes eléctricos
            time.sleep_ms(DEBOUNCE_MS)
            # Comprobar de nuevo si sigue pulsado
            if button.value() == 0:
                # Pulsación válida: cambiar estado del LED
                toggle_led()
                # Esperar a que el usuario suelte el botón antes de aceptar otra pulsación
                wait_for_release()
        # Pequeña pausa para no consumir 100% CPU
        time.sleep_ms(10)


if __name__ == '__main__':
    main_loop()
