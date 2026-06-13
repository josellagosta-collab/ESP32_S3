import time

# Proyecto 7.1 Serial Print - MicroPython para ESP32-S3 WROOM
# Este programa envía por la consola serie el tiempo transcurrido desde
# el arranque de la placa, mostrando una línea nueva cada segundo.

# Mensaje inicial que indica que la placa ha arrancado correctamente
print("ESP32S3 initialization completed!")

# Bucle infinito: calcula y muestra el tiempo transcurrido cada segundo
while True:
    # time.ticks_ms() devuelve milisegundos desde el arranque
    milisegundos = time.ticks_ms()

    # Convertimos milisegundos a segundos (división entera para un valor sencillo)
    segundos = milisegundos // 1000

    # Imprimimos el tiempo en el formato solicitado
    print("Running time :", segundos, "s")

    # Esperamos 1 segundo antes de la siguiente impresión
    time.sleep(1)
