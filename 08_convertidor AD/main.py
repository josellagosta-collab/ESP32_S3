from machine import Pin, ADC
import time

# Configuración del ADC en GPIO 2
potenciometro = ADC(Pin(2))

# Constantes del ADC del ESP32-S3 (12 bits y referencia de 3.3 V)
MAX_ADC = 4095
V_REF = 3.3

# Cambia a True para usar la segunda versión con barra gráfica ASCII
usar_barra_grafica = False


def calcular_porcentaje(valor_adc):
    """Convierte el valor ADC en porcentaje (0-100)."""
    return (valor_adc / MAX_ADC) * 100


def calcular_voltaje(valor_adc):
    """Convierte el valor ADC en voltaje aproximado en base a 3.3 V."""
    return (valor_adc / MAX_ADC) * V_REF


def imprimir_datos(valor_adc, porcentaje, voltaje):
    """Muestra los datos leídos por monitor serie."""
    print("------------------------------")
    print("ADC:", valor_adc)
    print("Porcentaje:", round(porcentaje, 1), "%")
    print("Voltaje:", round(voltaje, 2), "V")


def imprimir_barra_ascii(porcentaje):
    """Muestra una barra gráfica ASCII según el porcentaje."""
    barras = int(porcentaje / 5)
    barra = "[" + "#" * barras + "-" * (20 - barras) + "]"
    print(barra, round(porcentaje, 1), "%")


while True:
    valor_adc = potenciometro.read()
    porcentaje = calcular_porcentaje(valor_adc)
    voltaje = calcular_voltaje(valor_adc)

    if usar_barra_grafica:
        # Segunda versión con barra gráfica ASCII
        imprimir_barra_ascii(porcentaje)
    else:
        # Versión principal mostrando valor ADC, porcentaje y voltaje
        imprimir_datos(valor_adc, porcentaje, voltaje)

    # Actualiza cada 500 ms
    time.sleep(0.5)
