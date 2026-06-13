from machine import Pin
import time

# Pin GPIO para el Trigger del HC-SR04
trig_pin = Pin(13, Pin.OUT, value=0)
# Pin GPIO para el Echo del HC-SR04
echo_pin = Pin(14, Pin.IN)

# Velocidad del sonido en cm/s a temperatura ambiente
SOUND_SPEED = 34000
# Timeout máximo para leer el eco en microsegundos
MAX_ECHO_TIMEOUT_US = 30000

# Variables para almacenar distancia mínima y máxima
min_distance = None
max_distance = None

# Configuración MQTT opcional
MQTT_ENABLED = False
MQTT_BROKER = "192.168.1.100"
MQTT_PORT = 1883
MQTT_TOPIC = b"esp32s3/sonar/distance"
MQTT_CLIENT_ID = b"esp32s3_sonar"


def getSonar():
    # Genera un pulso Trigger para iniciar la medición
    trig_pin.value(0)
    time.sleep_us(2)
    trig_pin.value(1)
    time.sleep_us(10)
    trig_pin.value(0)

    # Espera hasta que el pin Echo se active o se agote el timeout
    start = time.ticks_us()
    while not echo_pin.value():
        if time.ticks_diff(time.ticks_us(), start) > MAX_ECHO_TIMEOUT_US:
            return None

    # Registra el tiempo de inicio del pulso Echo
    pulse_start = time.ticks_us()

    # Espera hasta que el pin Echo se desactive o se agote el timeout
    while echo_pin.value():
        if time.ticks_diff(time.ticks_us(), pulse_start) > MAX_ECHO_TIMEOUT_US:
            return None

    # Registra el tiempo de final del pulso Echo
    pulse_end = time.ticks_us()

    # Calcula la duración del pulso en microsegundos
    pulse_duration = time.ticks_diff(pulse_end, pulse_start)

    # Convierte el tiempo en distancia en centímetros
    distance_cm = (pulse_duration * SOUND_SPEED) // 2 // 10000

    # Devuelve la distancia como entero
    return int(distance_cm)


def mqtt_publish(distance):
    # Publica la distancia en MQTT si la opción está habilitada
    try:
        import network
        from umqtt.simple import MQTTClient
    except Exception:
        print("MQTT no disponible: módulo ausente")
        return

    # Conectar a la red Wi-Fi antes de usar MQTT
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("MQTT: no conectado a Wi-Fi")
        return

    # Crea cliente MQTT y publica el valor
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
    try:
        client.connect()
        payload = b"%d" % distance
        client.publish(MQTT_TOPIC, payload)
        client.disconnect()
        print("MQTT: distancia publicada ->", distance)
    except Exception as exc:
        print("MQTT error:", exc)


if __name__ == "__main__":
    # Espera un poco para estabilizar el hardware
    time.sleep_ms(2000)

    print("Iniciando medición ultrasónica HC-SR04")
    if MQTT_ENABLED:
        print("MQTT activado: prepare la conexión Wi-Fi y broker")
    else:
        print("MQTT desactivado: usando solo terminal")

    # Bucle principal de medición
    while True:
        distance = getSonar()
        if distance is None:
            print("Error: sin lectura de eco (timeout)")
        else:
            # Actualiza los valores mínimo y máximo
            if min_distance is None or distance < min_distance:
                min_distance = distance
            if max_distance is None or distance > max_distance:
                max_distance = distance

            print("Distancia: %d cm" % distance)
            print("Distancia mínima: %s cm" % (min_distance if min_distance is not None else "-") )
            print("Distancia máxima: %s cm" % (max_distance if max_distance is not None else "-"))

            if MQTT_ENABLED:
                mqtt_publish(distance)

        time.sleep_ms(500)
