from machine import Pin, ADC
import time

# Configuración de los pines del joystick
x_axis = ADC(Pin(1))  # VRX conectado a GPIO 1
y_axis = ADC(Pin(2))  # VRY conectado a GPIO 2
button = Pin(41, Pin.IN, Pin.PULL_UP)  # SW conectado a GPIO 41 con resistencia interna pull-up

# Constantes para convertir a porcentaje y detectar direcciones
ADC_MAX = 4095
CENTRO_MIN = 1600
CENTRO_MAX = 2500


def convertir_porcentaje(valor):
    """Convierte un valor ADC 0-4095 a porcentaje 0-100."""
    return int((valor * 100) / ADC_MAX)


def detectar_direccion(x, y):
    """Detecta la dirección del joystick según los valores X e Y."""
    direccion = "CENTRO"

    if x < CENTRO_MIN:
        direccion = "IZQUIERDA"
    elif x > CENTRO_MAX:
        direccion = "DERECHA"

    if y < CENTRO_MIN:
        direccion = "ARRIBA"
    elif y > CENTRO_MAX:
        direccion = "ABAJO"

    return direccion


while True:
    # Leer los valores analógicos de los ejes X e Y
    x_value = x_axis.read()
    y_value = y_axis.read()

    # Leer el estado del botón SW
    if button.value() == 0:
        sw_state = "PULSADO"
    else:
        sw_state = "SIN PULSAR"

    # Convertir los valores a porcentaje
    x_percent = convertir_porcentaje(x_value)
    y_percent = convertir_porcentaje(y_value)

    # Detectar la dirección del joystick
    direction = detectar_direccion(x_value, y_value)

    # Mostrar resultados en el monitor serie
    print("--------------------------")
    print("Eje X:", x_value, "(", x_percent, "%)")
    print("Eje Y:", y_value, "(", y_percent, "%)")
    print("Dirección:", direction)
    print("SW:", sw_state)

    # Esperar 200 ms antes de la siguiente lectura
    time.sleep(0.2)
