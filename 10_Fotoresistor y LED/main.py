from machine import Pin, ADC, PWM
import time

# Configuración del ADC para la LDR en GPIO2
ldr = ADC(Pin(2))
ldr.atten(ADC.ATTN_11DB)  # Permite mediciones más cercanas a 3.3 V
ldr.width(ADC.WIDTH_12BIT)  # Lectura de 0 a 4095

# Configuración del LED PWM en GPIO14
led = PWM(Pin(14), freq=1000)

# Función para mapear la lectura ADC al rango de PWM invertido
def adc_a_pwm(lectura_adc):
    # La lectura ADC va de 0 (oscuro) a 4095 (muy iluminado)
    # Se invierte para que el LED sea más brillante con menos luz ambiental.
    brillo = 65535 - int((lectura_adc / 4095) * 65535)
    return max(0, min(65535, brillo))

while True:
    valor_ldr = ldr.read()
    valor_pwm = adc_a_pwm(valor_ldr)

    # Actualiza el brillo del LED
    led.duty_u16(valor_pwm)

    # Mostrar valores por monitor serie
    porcentaje = int((valor_pwm / 65535) * 100)
    print("LDR ADC:", valor_ldr, "-> Brillo PWM:", valor_pwm, "(~{}%)".format(porcentaje))

    time.sleep_ms(200)
