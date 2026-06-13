from machine import Pin, PWM
import time

# Configura el pin GPIO1 como salida PWM para controlar el servomotor.
servo = PWM(Pin(1))
servo.freq(50)  # Frecuencia estándar de servomotores: 50 Hz

# Función que convierte un ángulo de 0° a 180° en un valor adecuado para duty_u16.
def move_servo(angle):
    # Limitar el ángulo al rango válido.
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180

    # Los servos suelen interpretar pulsos de aproximadamente 0.5 ms a 2.5 ms
    # dentro de un periodo de 20 ms. Con duty_u16 usamos valores entre 0 y 65535.
    # Aquí mapeamos 0° a un duty cercano a 1638 (0.5 ms) y 180° a 49151 (2.5 ms).
    min_duty = 1638
    max_duty = 49151
    duty = int(min_duty + (angle / 180) * (max_duty - min_duty))

    servo.duty_u16(duty)

# Bucle principal: barrido suave de 0° a 180° y de regreso a 0°.
while True:
    for angle in range(0, 181, 2):
        move_servo(angle)
        time.sleep_ms(20)

    for angle in range(180, -1, -2):
        move_servo(angle)
        time.sleep_ms(20)
