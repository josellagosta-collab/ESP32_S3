"""
Proyecto 15.1 - Control de Motor con Potenciómetro
ESP32-S3 WROOM + MicroPython

Control bidireccional de un motor DC mediante:
- Potenciómetro analógico (GPIO1)
- Driver L293D
- PWM para control de velocidad

Autor: Sistema de aprendizaje
Fecha: 2024
"""

from machine import ADC, Pin, PWM
import time

# ============================================================================
# CONFIGURACIÓN DE PINES
# ============================================================================

# Pines de control del L293D (Control de dirección)
IN1_PIN = Pin(13, Pin.OUT)  # Entrada 1 del motor
IN2_PIN = Pin(14, Pin.OUT)  # Entrada 2 del motor

# Pin de control de velocidad (PWM)
EN_PIN = Pin(12, Pin.OUT)   # Enable con PWM para velocidad

# Pin del potenciómetro (Entrada analógica)
POTENTIOMETER_PIN = ADC(Pin(1))  # GPIO1 - Lectura analógica

# ============================================================================
# CONFIGURACIÓN DEL PWM
# ============================================================================

# Crear objeto PWM con frecuencia de 10 kHz
pwm = PWM(EN_PIN, 10000)

# ============================================================================
# CONSTANTES Y PARÁMETROS DE CONTROL
# ============================================================================

# Valores límite del ADC (0 a 4095)
ADC_MIN = 0
ADC_MAX = 4095
ADC_CENTER = 2048  # Valor central (motor parado)

# Zona muerta: rango de valores alrededor del centro donde el motor no gira
# Evita vibraciones y comportamiento errático
DEAD_ZONE = 100  # ±100 unidades del centro

# Parámetro de escala para la velocidad PWM (0-1023 es el rango típico)
MAX_PWM_DUTY = 1023

# Intervalo de actualización en milisegundos
UPDATE_INTERVAL_MS = 50

# ============================================================================
# FUNCIONES DE CONTROL
# ============================================================================

def read_potentiometer():
    """
    Lee el valor del potenciómetro mediante ADC.
    
    Returns:
        int: Valor entre 0 y 4095
    """
    return POTENTIOMETER_PIN.read()

def determine_direction(adc_value):
    """
    Determina la dirección de giro del motor.
    
    Args:
        adc_value (int): Lectura del potenciómetro
    
    Returns:
        int: 1 para adelante, 0 para atrás
    """
    if adc_value > ADC_CENTER:
        return 1  # Motor adelante
    else:
        return 0  # Motor atrás

def calculate_speed(adc_value):
    """
    Calcula la velocidad del motor a partir de la lectura del potenciómetro.
    La velocidad es proporcional a la distancia del valor central.
    
    Args:
        adc_value (int): Lectura del potenciómetro
    
    Returns:
        int: Velocidad PWM (0-1023)
    """
    # Calcular distancia desde el centro
    distance_from_center = abs(adc_value - ADC_CENTER)
    
    # Aplicar zona muerta
    if distance_from_center < DEAD_ZONE:
        return 0  # Motor parado en la zona muerta
    
    # Restar la zona muerta para obtener rango efectivo
    effective_distance = distance_from_center - DEAD_ZONE
    
    # Escalar a rango de PWM (0-1023)
    # El rango máximo es (ADC_CENTER - DEAD_ZONE) = 1948
    max_effective_distance = ADC_CENTER - DEAD_ZONE
    speed = int((effective_distance / max_effective_distance) * MAX_PWM_DUTY)
    
    # Limitar al rango máximo
    return min(speed, MAX_PWM_DUTY)

def set_motor_direction(direction):
    """
    Establece el sentido de giro del motor mediante los pines IN1 e IN2.
    
    Args:
        direction (int): 1 para adelante, 0 para atrás
    """
    if direction == 1:
        # Motor adelante
        IN1_PIN.value(1)
        IN2_PIN.value(0)
    else:
        # Motor atrás
        IN1_PIN.value(0)
        IN2_PIN.value(1)

def set_motor_speed(speed):
    """
    Establece la velocidad del motor mediante PWM.
    
    Args:
        speed (int): Valor entre 0 y 1023
    """
    pwm.duty(speed)

def calculate_speed_percentage(adc_value):
    """
    Calcula el porcentaje de velocidad para mostrar en serial.
    
    Args:
        adc_value (int): Lectura del potenciómetro
    
    Returns:
        int: Porcentaje de velocidad (0-100)
    """
    distance_from_center = abs(adc_value - ADC_CENTER)
    
    if distance_from_center < DEAD_ZONE:
        return 0
    
    effective_distance = distance_from_center - DEAD_ZONE
    max_effective_distance = ADC_CENTER - DEAD_ZONE
    percentage = int((effective_distance / max_effective_distance) * 100)
    
    return min(percentage, 100)

# ============================================================================
# BUCLE PRINCIPAL
# ============================================================================

def main():
    """
    Función principal que controla el motor continuamente.
    """
    print("\n" + "="*60)
    print("Proyecto 15.1 - Control de Motor con Potenciómetro")
    print("ESP32-S3 WROOM + MicroPython")
    print("="*60)
    print("Sistema iniciado correctamente")
    print("Girando el potenciómetro para controlar el motor...\n")
    
    # Inicializar estado anterior para detectar cambios
    last_speed = -1
    last_direction = -1
    
    try:
        while True:
            # Leer potenciómetro
            adc_value = read_potentiometer()
            
            # Determinar dirección y velocidad
            direction = determine_direction(adc_value)
            speed = calculate_speed(adc_value)
            speed_percentage = calculate_speed_percentage(adc_value)
            
            # Aplicar cambios solo si hay variación significativa (optimización)
            if speed != last_speed or direction != last_direction:
                set_motor_direction(direction)
                set_motor_speed(speed)
                last_speed = speed
                last_direction = direction
            
            # Mostrar datos por monitor serie
            direction_text = "ADELANTE" if direction == 1 else "ATRÁS   "
            
            print(f"ADC: {adc_value:4d} | "
                  f"Velocidad: {speed_percentage:3d}% | "
                  f"PWM: {speed:4d} | "
                  f"Dirección: {direction_text} | "
                  f"Raw PWM: {speed:4d}")
            
            # Esperar antes de siguiente lectura
            time.sleep_ms(UPDATE_INTERVAL_MS)
    
    except KeyboardInterrupt:
        # Detener motor al presionar Ctrl+C
        print("\n\nSistema detenido por el usuario")
        stop_motor()
    
    except Exception as e:
        print(f"Error en la ejecución: {e}")
        stop_motor()

def stop_motor():
    """
    Detiene el motor estableciendo velocidad a cero.
    """
    pwm.duty(0)
    IN1_PIN.value(0)
    IN2_PIN.value(0)
    print("Motor detenido")

# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == "__main__":
    main()
