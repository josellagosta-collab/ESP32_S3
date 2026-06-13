from machine import ADC, Pin, PWM
import time

# Configura el ADC del potenciómetro en GPIO14 con resolución de 12 bits.
adc = ADC(Pin(14))
adc.atten(ADC.ATTN_11DB)  # Rango completo aproximado 0-3.3V
adc.width(ADC.WIDTH_12BIT)  # Resolución 12 bits: 0-4095

# Configura el PWM del servomotor en GPIO21 a 50 Hz.
servo = PWM(Pin(21))
servo.freq(50)

# Estado actual del ángulo para suavizar el movimiento.
current_angle = 0


def read_potentiometer(samples=8):
    """Leer varias muestras del ADC y devolver la media.

    Esto reduce el ruido y estabiliza el control del servomotor.
    """
    total = 0
    for _ in range(samples):
        total += adc.read()
        time.sleep_ms(2)
    return total // samples


def adc_to_angle(adc_value):
    """Convertir la lectura ADC (0-4095) a un ángulo entre 0° y 180°."""
    return int((adc_value * 180) / 4095)


def angle_to_duty_u16(angle):
    """Convertir un ángulo a duty_u16 para PWM de 50 Hz.

    Se mapea 0° a un pulso cercano a 0.5 ms y 180° a 2.5 ms.
    """
    min_duty = 1638   # 0.5 ms / 20 ms * 65535
    max_duty = 49151  # 2.5 ms / 20 ms * 65535
    return int(min_duty + (angle / 180) * (max_duty - min_duty))


def move_servo(target_angle):
    """Mover el servo suavemente desde el ángulo actual hasta el ángulo objetivo."""
    global current_angle
    if target_angle < 0:
        target_angle = 0
    elif target_angle > 180:
        target_angle = 180

    if target_angle == current_angle:
        return

    step = 1 if target_angle > current_angle else -1
    for angle in range(current_angle, target_angle + step, step):
        duty = angle_to_duty_u16(angle)
        servo.duty_u16(duty)
        time.sleep_ms(10)

    current_angle = target_angle


# Bucle principal: leer el potenciómetro, mostrar valores y controlar el servo.
while True:
    adc_value = read_potentiometer()
    angle = adc_to_angle(adc_value)

    print("ADC:", adc_value, "Ángulo:", angle)

    move_servo(angle)
    time.sleep_ms(50)
