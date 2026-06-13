# Proyecto 4.1 ESP32-S3 WROOM: LED Respiración (Breathing LED)

## Objetivo

Generar un programa en MicroPython para una placa ESP32-S3 WROOM capaz de controlar el brillo de un LED mediante PWM.

El LED debe:
- Aumentar gradualmente su brillo.
- Alcanzar el brillo máximo.
- Disminuir gradualmente su brillo.
- Repetir continuamente el ciclo.

## Componentes necesarios

- ESP32-S3 WROOM x1
- GPIO Extension Board x1
- Protoboard 830 puntos x1
- LED x1
- Resistencia 220 Ω x1
- Cables Dupont x2

## Conexiones

Según el esquema proporcionado:

- GPIO 10 → Resistencia 220 Ω → Ánodo del LED
- Cátodo del LED → GND

Esquema:

GPIO 10 ----> Resistencia 220 Ω ----> LED ----> GND

## ¿Qué es PWM?

PWM (Pulse Width Modulation) permite variar el brillo de un LED modificando el tiempo que permanece encendido y apagado.

Valores típicos:

- 0 = LED apagado
- 32768 = brillo medio
- 65535 = brillo máximo

## Funcionamiento esperado

1. El LED comienza apagado.
2. Aumenta lentamente su brillo.
3. Llega al máximo brillo.
4. Disminuye lentamente.
5. Se apaga.
6. Repite el proceso indefinidamente.

## Requisitos del script

Generar un archivo main.py que:

1. Importe PWM y Pin desde machine.
2. Importe time.
3. Configure GPIO 10 como PWM.
4. Use una frecuencia PWM de 1000 Hz.
5. Aumente progresivamente el brillo.
6. Disminuya progresivamente el brillo.
7. Repita continuamente el efecto.



## Instrucciones para la IA de Visual Studio Code

Genera un archivo main.py para MicroPython.

Características:

- ESP32-S3 WROOM
- LED conectado al GPIO 10
- PWM a 1000 Hz
- Efecto respiración continuo
- Código comentado
- Adecuado para alumnado principiante
