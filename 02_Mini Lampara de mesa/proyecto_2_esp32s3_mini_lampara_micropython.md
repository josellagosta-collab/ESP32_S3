# Proyecto 2.2 ESP32-S3 WROOM: Mini lámpara de mesa con pulsador y LED

## Objetivo

Generar un script en MicroPython para una placa ESP32-S3 WROOM que permita controlar un LED externo mediante un botón pulsador.

El funcionamiento debe ser el siguiente:

- Al pulsar el botón una vez, el LED se enciende.
- Al pulsar el botón otra vez, el LED se apaga.
- El LED no debe estar encendido solo mientras se mantiene pulsado el botón.
- El sistema debe recordar el estado del LED.
- Se debe aplicar antirrebote por software para evitar falsas pulsaciones.

## Hardware necesario

- 1 placa ESP32-S3 WROOM
- 1 LED
- 1 resistencia de 220 Ω o 330 Ω para el LED
- 1 botón pulsador
- Cables Dupont
- Protoboard
- Cable USB para conectar la placa al PC

## Conexión del LED

Conecta el LED externo de esta forma:

- Patilla larga del LED, ánodo positivo: conectar a GPIO 5 de la placa ESP32-S3.
- Patilla corta del LED, cátodo negativo: conectar a una resistencia de 220 Ω o 330 Ω.
- El otro extremo de la resistencia: conectar a GND de la placa ESP32-S3.

Esquema lógico del LED:

GPIO 5  ---->  ánodo LED  
cátodo LED  ---->  resistencia 220 Ω / 330 Ω  ---->  GND

## Conexión del botón pulsador

Usaremos la resistencia interna PULL_UP del ESP32-S3.

Conecta el botón pulsador de esta forma:

- Una patilla del pulsador: conectar a GPIO 4.
- La otra patilla del pulsador: conectar a GND.

No hace falta usar una resistencia externa de 10 kΩ si se activa la resistencia interna PULL_UP desde el programa.

Esquema lógico del pulsador:

GPIO 4  ---->  pulsador  ---->  GND

## Funcionamiento eléctrico del pulsador

Como se usará `Pin.PULL_UP`, el comportamiento será:

- Botón sin pulsar: el GPIO 4 lee valor 1.
- Botón pulsado: el GPIO 4 lee valor 0.

Por tanto, en el programa hay que considerar que el botón está pulsado cuando se lee un 0.

## Antirrebote del pulsador

Cuando se pulsa un botón, sus contactos mecánicos pueden producir pequeñas oscilaciones muy rápidas. Esto se llama rebote.

El microcontrolador puede interpretar esos rebotes como si fueran varias pulsaciones, aunque el usuario solo haya pulsado una vez.

Para evitarlo, el programa debe:

1. Detectar una posible pulsación.
2. Esperar unos milisegundos.
3. Comprobar de nuevo si el botón sigue pulsado.
4. Cambiar el estado del LED solo si la pulsación es estable.
5. Esperar a que el usuario suelte el botón antes de aceptar una nueva pulsación.

## Requisitos del script

Genera un archivo llamado `main.py` para MicroPython.

El programa debe:

1. Importar la clase `Pin` desde el módulo `machine`.
2. Importar el módulo `time`.
3. Configurar el GPIO 5 como salida digital para el LED.
4. Configurar el GPIO 4 como entrada digital con resistencia interna `Pin.PULL_UP`.
5. Crear una variable booleana para guardar el estado del LED.
6. Crear un bucle infinito.
7. Detectar cuándo se pulsa el botón.
8. Aplicar antirrebote por software.
9. Cambiar el estado del LED cada vez que se detecte una pulsación válida.
10. Mantener el LED encendido o apagado hasta la siguiente pulsación.
