# Kit de proyectos ESP32-S3 con MicroPython

Este repositorio contiene una colección de prácticas y experimentos educativos para la placa ESP32-S3 WROOM usando MicroPython. Está pensado como un material de aprendizaje práctico para familiarizarse con entradas/salidas digitales, PWM, sensores, comunicación serie, Wi-Fi, Bluetooth, TCP/IP y control de periféricos.

## ¿Qué encontrarás aquí?

La carpeta principal está organizada por temas y proyectos progresivos, desde los más básicos hasta los más completos:

- 01_Parpadeo LED: introducción a GPIO y control básico de un LED.
- 02_Mini Lampara de mesa: proyecto simple de iluminación y uso de salidas digitales.
- 03_barra_led_luz_movimiento: detección de luz y control de una barra LED.
- 04_Analógico y PWM: señales analógicas, modulación por ancho de pulso y respiración de LEDs.
- 05_Luz de color aleatorio con LED RGB: generación de colores y efectos visuales con LED RGB.
- 06_Buzzer: sonido, tonos y alarmas con zumbador.
- 07_Comunicación serie: depuración y comunicación mediante puerto serie.
- 08_convertidor AD: lectura de entradas analógicas con ADC.
- 09_Potenciometro y LED: control de intensidad luminosa mediante potenciómetro.
- 10_Fotoresistor y LED: detección de luz con fotorresistor y activación de LED.
- 11_Termistor: medición de temperatura y uso de sensores térmicos.
- 12_Joystick: lectura de ejes analógicos y control de un sistema simple.
- 13_74HC595 y Barra Led: expansión de salidas con registro de desplazamiento.
- 14_74HC595 y Display de 7 segmentos: visualización numérica con display.
- 15_Rele y motor: control de actuadores y relés.
- 16_Servo: posicionamiento y barrido de servomotores.
- 17_LCD 1602: visualización de texto en pantallas LCD I2C.
- 18_Medición ultrasónica: medición de distancia mediante sensor HC-SR04.
- 19_Bluetooth: comunicación inalámbrica basada en Bluetooth.
- 20_Modos de funcionamiento WIFI: modo estación, AP y AP+estación.
- 21_TCP IP: comunicación de red con protocolo TCP/IP.
- 22_control LLED por web: control de un LED desde una página web.

Además, en la carpeta Super-Starter-Kit-for-ESP32-S3-WROOM-main se incluye material de referencia adicional del kit de inicio.

## Estructura del proyecto

Cada carpeta suele contener:

- main.py: programa principal del experimento.
- boot.py: inicialización o configuración de arranque.
- archivos .md: manuales, explicaciones o guías del proyecto.

Esta organización permite estudiar cada práctica por separado y cargar los ejemplos directamente en la placa ESP32-S3.

## Requisitos

Para trabajar con este proyecto necesitas:

- Una placa ESP32-S3 WROOM.
- Firmware MicroPython instalado en la placa.
- Un cable USB para programación y alimentación.
- Un editor o entorno como Thonny, uPyCraft o similar.
- Los componentes electrónicos indicados en cada práctica.

## Cómo usar este repositorio

1. Elige la carpeta del proyecto que quieras probar.
2. Abre el archivo main.py y revisa la lógica del ejemplo.
3. Sube el programa a la placa ESP32-S3.
4. Ajusta los pines, redes Wi-Fi o parámetros según sea necesario.
5. Ejecuta el ejemplo y observa el comportamiento en hardware.

## Objetivo del repositorio

Este material busca enseñar de forma práctica cómo programar una ESP32-S3 con MicroPython, combinando teoría, electrónica y programación en una misma colección de proyectos.

## Nota

Algunos proyectos incluyen manuales detallados en formato Markdown dentro de sus carpetas. Se recomienda revisarlos antes de realizar la conexión física de los componentes.
