# ============================================================================
# Proyecto 11.1 – Termómetro con Termistor NTC
# ESP32-S3 WROOM + MicroPython
# ============================================================================
# Descripción: Lee un termistor NTC mediante ADC y calcula la temperatura
# Conexiones:
#   - Termistor NTC: 3.3V
#   - Unión NTC + Resistencia: GPIO2 (ADC)
#   - Resistencia 10kΩ: GND
# ============================================================================

from machine import Pin, ADC
import time

# ============================================================================
# Configuración
# ============================================================================

# Inicializar el ADC en GPIO2
# El ESP32-S3 tiene ADC0 y ADC1, GPIO2 está en ADC1
adc_sensor = ADC(Pin(2))

# Configurar la resolución del ADC (12 bits = 0 a 4095)
adc_sensor.awidth(ADC.WIDTH_12BIT)

# Configurar la atenuación del ADC para el rango de voltaje (3.3V)
adc_sensor.atten(ADC.ATTN_11DB)

# Intervalo de lectura en segundos
INTERVALO_LECTURA = 1

# ============================================================================
# Funciones
# ============================================================================

def leer_adc():
    """
    Lee el valor ADC del termistor.
    Retorna un valor entre 0 y 4095.
    """
    valor_adc = adc_sensor.read()
    return valor_adc


def calcular_temperatura(valor_adc):
    """
    Convierte el valor del ADC a temperatura aproximada en grados Celsius.
    
    Utilizamos una aproximación lineal:
    - ADC 0 (máxima resistencia del termistor NTC) ≈ 50°C
    - ADC 4095 (mínima resistencia del termistor NTC) ≈ 0°C
    
    Fórmula: Temperatura = 50 - ((ADC / 4095) * 50)
    """
    temperatura = 50 - ((valor_adc / 4095) * 50)
    return temperatura


def mostrar_datos(valor_adc, temperatura):
    """
    Imprime los datos formateados por el monitor serie.
    """
    print("=" * 50)
    print("LECTURA DE TEMPERATURA - TERMISTOR NTC")
    print("=" * 50)
    print(f"Valor ADC: {valor_adc} (0-4095)")
    print(f"Tensión aproximada: {(valor_adc / 4095) * 3.3:.2f}V")
    print(f"Temperatura: {temperatura:.1f}°C")
    print("=" * 50)
    print()


# ============================================================================
# Bucle principal
# ============================================================================

print("Inicializando sistema...")
print("Monitor de temperatura con termistor NTC iniciado.")
print("Presiona CTRL+C para detener.\n")

try:
    while True:
        # Leer el valor del ADC
        valor_adc = leer_adc()
        
        # Calcular la temperatura
        temperatura = calcular_temperatura(valor_adc)
        
        # Mostrar los datos
        mostrar_datos(valor_adc, temperatura)
        
        # Esperar antes de la siguiente lectura
        time.sleep(INTERVALO_LECTURA)

except KeyboardInterrupt:
    print("\nPrograma detenido por el usuario.")
    print("Sistema apagado.")
