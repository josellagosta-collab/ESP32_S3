# Proyecto 4.1: LED Respiración (Breathing LED)
# ESP32-S3 WROOM con MicroPython
# Descripción: Control del brillo de un LED mediante PWM con efecto de respiración

# ============================================================================
# IMPORTACIONES
# ============================================================================

from machine import Pin, PWM  # Para controlar GPIO y PWM
import time                    # Para controlar los tiempos

# ============================================================================
# CONFIGURACIÓN DEL PWM
# ============================================================================

# Definir el pin GPIO 10 como salida PWM
# Parámetros:
#   - Pin(10): GPIO 10 donde está conectado el LED
#   - freq=1000: Frecuencia PWM de 1000 Hz
led_pwm = PWM(Pin(10), freq=1000)

# ============================================================================
# VARIABLES DE CONFIGURACIÓN
# ============================================================================

# Rango de valores PWM (0 = apagado, 65535 = brillo máximo)
PWM_MIN = 0           # Brillo mínimo
PWM_MAX = 65535       # Brillo máximo

# Velocidad del efecto respiración (en segundos)
STEP_DELAY = 0.05     # Tiempo entre incrementos (más bajo = más rápido)

# Incremento de brillo en cada paso
# Dividimos el rango máximo entre pasos para obtener incrementos suaves
BRIGHTNESS_STEPS = 100  # Número de pasos para subir o bajar
STEP_SIZE = PWM_MAX // BRIGHTNESS_STEPS

# ============================================================================
# FUNCIÓN PARA EFECTO DE RESPIRACIÓN
# ============================================================================

def breathing_effect():
    """
    Función que implementa el efecto de respiración continuo.
    
    Proceso:
    1. Aumenta el brillo gradualmente (de 0 a máximo)
    2. Disminuye el brillo gradualmente (de máximo a 0)
    3. Repite indefinidamente
    """
    
    # FASE 1: Aumentar el brillo (0 a máximo)
    print("Aumentando brillo...")
    for brightness in range(PWM_MIN, PWM_MAX, STEP_SIZE):
        led_pwm.duty_u16(brightness)  # Establecer brillo actual
        time.sleep(STEP_DELAY)         # Esperar antes del siguiente paso
    
    # Asegurar que se alcanza el máximo exacto
    led_pwm.duty_u16(PWM_MAX)
    time.sleep(STEP_DELAY)
    
    # FASE 2: Disminuir el brillo (máximo a 0)
    print("Disminuyendo brillo...")
    for brightness in range(PWM_MAX, PWM_MIN, -STEP_SIZE):
        led_pwm.duty_u16(brightness)  # Establecer brillo actual
        time.sleep(STEP_DELAY)         # Esperar antes del siguiente paso
    
    # Asegurar que se apaga completamente
    led_pwm.duty_u16(PWM_MIN)
    time.sleep(STEP_DELAY)

# ============================================================================
# BUCLE PRINCIPAL
# ============================================================================

print("=== LED Respiración Iniciado ===")
print("GPIO 10 - Frecuencia PWM: 1000 Hz")
print("Efecto de respiración en ejecución...")
print()

try:
    # Bucle infinito para repetir el efecto continuamente
    while True:
        breathing_effect()
        
except KeyboardInterrupt:
    # Manejo de interrupción por teclado (Ctrl+C)
    print("\nPrograma interrumpido por el usuario")
    led_pwm.duty_u16(0)  # Apagar el LED
    print("LED apagado")
