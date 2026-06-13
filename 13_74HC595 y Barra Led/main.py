from machine import Pin
import time

# Pines del ESP32-S3 conectados al 74HC595
STCP_PIN = 12  # LATCH / STCP
SHCP_PIN = 13  # CLOCK / SHCP
DS_PIN = 14    # DATA / DS

# Inicialización de pines como salida
stcp = Pin(STCP_PIN, Pin.OUT)
shcp = Pin(SHCP_PIN, Pin.OUT)
ds = Pin(DS_PIN, Pin.OUT)

# Aseguramos que los pines empiecen en bajo
stcp.value(0)
shcp.value(0)
ds.value(0)


def shift_out(order, value):
    """Envía un byte al 74HC595 usando desplazamiento de bits.

    order: 1 para MSB first, 0 para LSB first.
    value: byte de 0..255.
    """
    stcp.value(0)  # Preparar latch para recibir datos

    for i in range(8):
        if order == 1:
            bit = (value >> (7 - i)) & 1
        else:
            bit = (value >> i) & 1

        ds.value(bit)
        shcp.value(1)
        time.sleep_us(1)
        shcp.value(0)

    stcp.value(1)  # Actualiza las salidas del 74HC595
    time.sleep_us(1)
    stcp.value(0)


def enviar_byte(value):
    """Alternativa sin clase externa: envía un byte directamente."""
    shift_out(1, value)


def animacion_lineal(delay_ms=300):
    """Anima un LED a la vez de un extremo al otro."""
    valor = 0x01
    for _ in range(8):
        enviar_byte(valor)
        valor <<= 1
        time.sleep_ms(delay_ms)


def animacion_ida_y_vuelta(delay_ms=200):
    """Anima la luz de izquierda a derecha y regresa de derecha a izquierda."""
    # Ida: Q0 -> Q7
    for i in range(8):
        enviar_byte(1 << i)
        time.sleep_ms(delay_ms)

    # Vuelta: Q6 -> Q1 (sin repetir el extremo Q7)
    for i in range(6, 0, -1):
        enviar_byte(1 << i)
        time.sleep_ms(delay_ms)


# Bucle principal
while True:
    # Versión principal: ida y vuelta para el efecto de lámpara de agua
    animacion_ida_y_vuelta(250)

    # Si quieres usar la versión lineal simple,
    # reemplaza la línea anterior por:
    # animacion_lineal(300)
