from machine import Pin, ADC, PWM
import time

# Configuración del potenciómetro en GPIO 2 como entrada ADC
pot = ADC(Pin(2))

# Configuración del LED en GPIO 1 como salida PWM
led = PWM(Pin(1))
led.freq(1000)  # Frecuencia PWM de 1000 Hz

while True:
    # Leer el valor analógico del potenciómetro (0-4095)
    valor_adc = pot.read()

    # Convertir el valor ADC al rango PWM de 16 bits (0-65535)
    brillo = int((valor_adc / 4095) * 65535)

    # Calcular el porcentaje de brillo para mostrar en el monitor serie
    porcentaje = (valor_adc / 4095) * 100

    # Aplicar el valor PWM al LED
    led.duty_u16(brillo)

    # Imprimir valores en el monitor serie
    print(
        "ADC:", valor_adc,
        "PWM:", brillo,
        "Brillo:", round(porcentaje, 1), "%"
    )

    # Pequeña espera para estabilizar la lectura y no saturar el puerto serie
    time.sleep(0.2)
