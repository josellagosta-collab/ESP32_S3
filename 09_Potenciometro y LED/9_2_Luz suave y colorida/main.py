from machine import Pin, ADC, PWM
import time

# Configuración ADC para los potenciómetros
adc_red = ADC(Pin(14))
adc_red.atten(ADC.ATTN_11DB)
adc_green = ADC(Pin(13))
adc_green.atten(ADC.ATTN_11DB)
adc_blue = ADC(Pin(12))
adc_blue.atten(ADC.ATTN_11DB)

# Configuración PWM para el LED RGB
pwm_red = PWM(Pin(38), freq=1000, duty_u16=0)
pwm_green = PWM(Pin(39), freq=1000, duty_u16=0)
pwm_blue = PWM(Pin(40), freq=1000, duty_u16=0)

# Conversion ADC -> PWM
def adc_to_pwm(value):
    return int((value / 4095) * 65535)

# Lectura filtrada del ADC
def read_adc_filtered(adc):
    total = adc.read() + adc.read() + adc.read()
    return total // 3

print("Iniciando control RGB con ADC y PWM")

while True:
    red_adc = read_adc_filtered(adc_red)
    green_adc = read_adc_filtered(adc_green)
    blue_adc = read_adc_filtered(adc_blue)

    red_pwm = adc_to_pwm(red_adc)
    green_pwm = adc_to_pwm(green_adc)
    blue_pwm = adc_to_pwm(blue_adc)

    pwm_red.duty_u16(red_pwm)
    pwm_green.duty_u16(green_pwm)
    pwm_blue.duty_u16(blue_pwm)

    print(
        "ADC R:{} G:{} B:{}  PWM R:{} G:{} B:{}".format(
            red_adc, green_adc, blue_adc, red_pwm, green_pwm, blue_pwm
        )
    )

    time.sleep(0.1)
