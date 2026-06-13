# Proyecto ESP32-S3 WROOM: Parpadeo de un LED con MicroPython

## Objetivo

Generar un script en MicroPython para una placa ESP32-S3 WROOM que haga parpadear un LED externo conectado a un pin GPIO.

## Hardware necesario

- 1 placa ESP32-S3 WROOM
- 1 LED
- 1 resistencia de 220 Ω o 330 Ω
- Cables Dupont
- Protoboard
- Cable USB para conectar la placa al PC

## Conexión del LED

Conecta el LED externo de esta forma:

- Patilla larga del LED, ánodo positivo: conectar a GPIO 5 de la placa ESP32-S3.
- Patilla corta del LED, cátodo negativo: conectar a una resistencia de 220 Ω o 330 Ω.
- El otro extremo de la resistencia: conectar a GND de la placa ESP32-S3.

Esquema lógico:

GPIO 5  ---->  ánodo LED
cátodo LED  ---->  resistencia 220 Ω / 330 Ω  ---->  GND

## Funcionamiento esperado

El LED debe encenderse durante 1 segundo y apagarse durante 1 segundo de forma repetida e indefinida.

## Requisitos del script

Genera un archivo llamado `main.py` para MicroPython.

El programa debe:

1. Importar la clase `Pin` desde el módulo `machine`.
2. Importar el módulo `time`.
3. Configurar el GPIO 5 como salida digital.
4. Crear un bucle infinito.
5. Encender el LED.
6. Esperar 1 segundo.
7. Apagar el LED.
8. Esperar 1 segundo.
9. Repetir el proceso indefinidamente.