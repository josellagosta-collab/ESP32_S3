"""
Proyecto 4.2 - Barra LED con PWM
Efecto de Flowing Light avanzado con ESP32-S3 WROOM

Este programa controla una barra LED de 10 segmentos usando PWM (Pulse Width Modulation)
para crear un efecto de luz fluida que se desplaza de izquierda a derecha.

Hardware:
- Placa ESP32-S3 WROOM
- Barra LED de 10 segmentos
- 10 resistencias de 220 Ω
- Cables Dupont y protoboard
"""

from machine import Pin, PWM
import time

# =============================================================================
# CONFIGURACIÓN DE PINES GPIO
# =============================================================================
# Lista de GPIO conectados a los segmentos de la barra LED
# El orden es importante: coincide con el orden físico de los LEDs
pines_led = [4, 5, 6, 7, 15, 16, 17, 18]

# =============================================================================
# INICIALIZACIÓN DE OBJETOS PWM
# =============================================================================
# Crear una lista para almacenar los objetos PWM
leds = []

# Configurar cada GPIO como salida PWM
for pin in pines_led:
    # Crear un objeto PWM para el pin
    led = PWM(Pin(pin))
    
    # Configurar la frecuencia PWM a 1000 Hz
    led.freq(1000)
    
    # Apagar el LED al inicializar (duty_u16 = 0)
    led.duty_u16(0)
    
    # Añadir el objeto PWM a la lista
    leds.append(led)

# =============================================================================
# DEFINICIÓN DE CONSTANTES DE BRILLO
# =============================================================================
# Estos valores controlan la intensidad del brillo mediante duty_u16()
# duty_u16() acepta valores de 0 a 65535

APAGADO = 0                    # LED completamente apagado
BRILLO_MEDIO = 32768           # 50% de brillo (aproximadamente)
BRILLO_MAXIMO = 65535          # 100% de brillo (máximo)

# =============================================================================
# VELOCIDAD DE LA ANIMACIÓN
# =============================================================================
# Retardo en milisegundos entre cada paso de la animación
# Aumentar este valor ralentiza la animación
# Disminuir este valor acelera la animación
RETARDO_MS = 150

# =============================================================================
# FUNCIONES AUXILIARES
# =============================================================================

def apagar_todos_los_leds():
    """
    Apaga todos los LEDs de la barra.
    
    Esta función se llama antes de cada paso de la animación para limpiar
    el estado anterior y evitar que haya múltiples LEDs encendidos.
    """
    for led in leds:
        led.duty_u16(APAGADO)


def mostrar_posicion(posicion):
    """
    Muestra la animación en una posición específica.
    
    Parámetros:
    - posicion: índice del LED principal (0 a len(leds)-1)
    
    Comportamiento:
    - El LED en 'posicion' brilla con brillo máximo
    - El LED en 'posicion + 1' (si existe) brilla con brillo medio
    - Todos los demás LEDs permanecen apagados
    """
    # Apagar todos los LEDs antes de mostrar la nueva posición
    apagar_todos_los_leds()
    
    # Encender el LED principal con brillo máximo
    leds[posicion].duty_u16(BRILLO_MAXIMO)
    
    # Si existe un LED siguiente, encenderlo con brillo medio
    if posicion + 1 < len(leds):
        leds[posicion + 1].duty_u16(BRILLO_MEDIO)
    
    # Retardo para controlar la velocidad
    time.sleep_ms(RETARDO_MS)


# =============================================================================
# BUCLE PRINCIPAL
# =============================================================================
# El programa se ejecuta indefinidamente

try:
    while True:
        # Recorrer cada posición de izquierda a derecha
        for posicion in range(len(leds)):
            mostrar_posicion(posicion)

except KeyboardInterrupt:
    # Apagar todos los LEDs si el usuario presiona Ctrl+C
    print("Programa interrumpido. Apagando todos los LEDs...")
    apagar_todos_los_leds()
    print("¡Listo!")
