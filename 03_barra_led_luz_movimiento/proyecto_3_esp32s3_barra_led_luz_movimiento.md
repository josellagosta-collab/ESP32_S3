# Proyecto 3 ESP32-S3 WROOM: Luz en movimiento con barra LED

## Objetivo

Generar un script en MicroPython para una placa ESP32-S3 WROOM que controle una barra LED de 10 segmentos y cree un efecto de luz en movimiento, parecido a una lámpara de agua que fluye.

El funcionamiento debe ser:

1. Encender el LED número 1.
2. Esperar un pequeño tiempo.
3. Apagar el LED número 1.
4. Encender el LED número 2.
5. Esperar un pequeño tiempo.
6. Apagar el LED número 2.
7. Repetir el proceso hasta el LED número 10.
8. Volver a empezar indefinidamente.

## Componentes necesarios

- 1 placa ESP32-S3 WROOM
- 1 GPIO Extension Board
- 1 protoboard de 830 puntos
- 1 barra LED de 10 segmentos
- 10 resistencias de 220 ohmios
- 10 cables Dupont

## Conexión de la barra LED

La barra LED tiene 10 LEDs internos. Cada LED debe conectarse a un pin GPIO del ESP32-S3 a través de una resistencia de 220 ohmios.

Según la captura del montaje, usaremos estos GPIO:

| Segmento de la barra LED | GPIO del ESP32-S3 |
|---|---|
| LED 1 | GPIO 4 |
| LED 2 | GPIO 5 |
| LED 3 | GPIO 6 |
| LED 4 | GPIO 7 |
| LED 5 | GPIO 15 |
| LED 6 | GPIO 16 |
| LED 7 | GPIO 17 |
| LED 8 | GPIO 18 |
| LED 9 | GPIO 8 |
| LED 10 | GPIO 3 |

Cada LED debe tener una resistencia de 220 ohmios en serie.

## Esquema lógico de conexión

Para cada segmento de la barra LED:

GPIO del ESP32-S3  ---->  resistencia de 220 ohmios  ---->  segmento de la barra LED

El otro lado de cada LED debe ir conectado a GND, según la orientación de la barra LED.

## Nota importante sobre la orientación de la barra LED

La barra LED tiene polaridad.

Si el programa se ejecuta pero no se enciende ningún LED, revisar:

- La orientación de la barra LED.
- Que el lado marcado de la barra LED coincida con el montaje.
- Que cada LED tenga su resistencia de 220 ohmios.
- Que GND esté correctamente conectado.
- Que los GPIO usados coincidan con los cables conectados.

Si la barra LED estuviera conectada al revés, puede que haya que invertirla físicamente en la protoboard.

## Funcionamiento esperado

El programa debe encender un único LED cada vez.

Ejemplo:

- Se enciende LED 1 y se apaga.
- Se enciende LED 2 y se apaga.
- Se enciende LED 3 y se apaga.
- Así hasta el LED 10.
- Al terminar, vuelve al LED 1.

Este ciclo se repite continuamente para crear el efecto de luz en movimiento.

## Requisitos del script

Genera un archivo llamado `main.py` para MicroPython.

El programa debe:

1. Importar la clase `Pin` desde el módulo `machine`.
2. Importar el módulo `time`.
3. Crear una lista con los GPIO usados.
4. Configurar todos los GPIO como salidas digitales.
5. Apagar todos los LEDs al iniciar el programa.
6. Crear un bucle infinito.
7. Recorrer la lista de LEDs desde el primero hasta el último.
8. Encender un LED.
9. Esperar 100 ms.
10. Apagar ese LED.
11. Pasar al siguiente LED.
12. Repetir indefinidamente.


