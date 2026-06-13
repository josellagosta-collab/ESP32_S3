# Proyecto 13.1 – Lámpara de Agua en Movimiento con 74HC595
## ESP32-S3 WROOM + MicroPython

---

## 1. Objetivo del proyecto

En proyectos anteriores se utilizó una barra LED para crear una lámpara de agua en movimiento conectando cada LED directamente a un GPIO del ESP32-S3.

Ese método funciona, pero consume muchos pines GPIO.

En este proyecto aprenderemos a utilizar el circuito integrado **74HC595**, un registro de desplazamiento de 8 bits, para controlar una barra LED utilizando muchos menos pines del ESP32-S3.

El objetivo es crear una animación de luz en movimiento usando:

- ESP32-S3 WROOM.
- Un 74HC595.
- Una barra LED.
- 8 resistencias de 220 Ω.

El efecto será:

```text
LED1 → LED2 → LED3 → LED4 → LED5 → LED6 → LED7 → LED8
```

y después se repetirá continuamente.

---

## 2. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3-WROOM | 1 |
| Placa de expansión GPIO | 1 |
| Protoboard de 830 puntos | 1 |
| Circuito integrado 74HC595 | 1 |
| Barra LED | 1 |
| Resistencias de 220 Ω | 8 |
| Cables Dupont | 15 |

---

## 3. Objetivos de aprendizaje

Al finalizar esta práctica el alumno debe ser capaz de:

1. Comprender qué es un registro de desplazamiento.
2. Utilizar el circuito integrado 74HC595.
3. Reducir el número de GPIO necesarios para controlar varios LEDs.
4. Enviar datos serie desde el ESP32-S3.
5. Convertir datos serie en salidas paralelas.
6. Crear una animación de luz en movimiento.
7. Comprender la importancia de ahorrar pines GPIO en sistemas embebidos.

---

## 4. ¿Qué problema resuelve el 74HC595?

Si queremos controlar 8 LEDs directamente desde el ESP32-S3, necesitamos 8 GPIO.

Con el 74HC595 podemos controlar esos mismos 8 LEDs usando solo 3 o 4 GPIO.

Esto es muy útil porque los GPIO del microcontrolador son recursos limitados.

Ejemplo:

| Método | GPIO necesarios |
|--------|-----------------|
| LED directo | 8 GPIO |
| Con 74HC595 | 3 o 4 GPIO |

---

## 5. ¿Qué es el 74HC595?

El **74HC595** es un registro de desplazamiento de 8 bits con salida paralela.

Permite enviar datos bit a bit desde el microcontrolador y obtener 8 salidas digitales.

Funcionamiento básico:

```text
ESP32-S3 envía bits en serie
          ↓
       74HC595
          ↓
8 salidas paralelas para LEDs
```

---

## 6. Pines principales del 74HC595

| Pin 74HC595 | Nombre habitual | Función |
|------------|-----------------|---------|
| DS | Data | Entrada de datos serie |
| SHCP | Shift Clock | Reloj de desplazamiento |
| STCP | Storage Clock / Latch | Actualiza las salidas |
| OE | Output Enable | Habilita las salidas |
| MR | Master Reset | Reset del registro |
| Q0-Q7 | Salidas | Salidas paralelas |
| VCC | Alimentación | 3.3 V o 5 V según montaje |
| GND | Tierra | GND |

---

## 7. Conexiones usadas en este proyecto

Según el código esperado de la práctica:

```python
chip = Chip74HC595(12, 13, 14, -1)
```

La interpretación del código es:

| ESP32-S3 | 74HC595 | Función |
|---------|---------|---------|
| GPIO 12 | STCP | Latch / Storage Clock |
| GPIO 13 | SHCP | Shift Clock |
| GPIO 14 | DS | Data |
| GND | OE | Output Enable |
| 3.3 V | VCC | Alimentación |
| GND | GND | Tierra |

En el comentario del código original aparece:

```python
# ESP32-12: 74HC595-STCP(12)
# ESP32-13: 74HC595-SHCP(11)
# ESP32-14: 74HC595-DS(14)
# ESP32-GND: 74HC595-OE(13)
```

---

## 8. Conexión de la barra LED

Las salidas Q0-Q7 del 74HC595 se conectan a los 8 segmentos de la barra LED.

Cada LED debe llevar una resistencia de 220 Ω en serie.

| Salida 74HC595 | Segmento barra LED |
|---------------|--------------------|
| Q0 | LED 1 |
| Q1 | LED 2 |
| Q2 | LED 3 |
| Q3 | LED 4 |
| Q4 | LED 5 |
| Q5 | LED 6 |
| Q6 | LED 7 |
| Q7 | LED 8 |

---

## 9. Esquema ASCII simplificado

```text
                    ESP32-S3 WROOM

              GPIO12 -------- STCP / LATCH
              GPIO13 -------- SHCP / CLOCK
              GPIO14 -------- DS / DATA
              GND   -------- OE
              3.3V  -------- VCC
              GND   -------- GND


                       74HC595
              +----------------------+
 DATA  ------>| DS                Q0 |----[220Ω]---- LED1
 CLOCK ------>| SHCP              Q1 |----[220Ω]---- LED2
 LATCH ------>| STCP              Q2 |----[220Ω]---- LED3
 OE    ------>| OE                Q3 |----[220Ω]---- LED4
              |                   Q4 |----[220Ω]---- LED5
              |                   Q5 |----[220Ω]---- LED6
              |                   Q6 |----[220Ω]---- LED7
              |                   Q7 |----[220Ω]---- LED8
              +----------------------+
```

---

## 10. Funcionamiento del registro de desplazamiento

El ESP32-S3 envía un byte al 74HC595.

Un byte tiene 8 bits:

```text
00000001
00000010
00000100
00001000
00010000
00100000
01000000
10000000
```

Cada bit controla una salida del 74HC595.

Ejemplo:

```text
00000001 → LED 1 encendido
00000010 → LED 2 encendido
00000100 → LED 3 encendido
10000000 → LED 8 encendido
```

---

## 11. Funcionamiento esperado del proyecto

El programa debe:

1. Inicializar el 74HC595.
2. Crear una variable con el valor `0x01`.
3. Enviar ese valor al 74HC595.
4. Desplazar el bit hacia la izquierda.
5. Encender los LEDs de forma secuencial.
6. Repetir el movimiento continuamente.
7. Crear un efecto de agua en movimiento.

---

## 12. Código esperado basado en la práctica

El código de referencia esperado es similar al siguiente:

```python
import time
from my74HC595 import Chip74HC595

chip = Chip74HC595(12, 13, 14, -1)  # STCP, SHCP, DS, OE

while True:
    x = 0x01
    for count in range(8):
        chip.shiftOut(1, x)
        x = x << 1
        time.sleep_ms(300)

    x = 0x01
    for count in range(8):
        chip.shiftOut(0, x)
        x = x << 1
        time.sleep_ms(300)
```

---

## 13. Explicación del código

### Importar time

```python
import time
```

Permite usar retardos.

---

### Importar la librería del 74HC595

```python
from my74HC595 import Chip74HC595
```

Importa la clase necesaria para controlar el integrado.

---

### Crear el objeto del chip

```python
chip = Chip74HC595(12, 13, 14, -1)
```

Los parámetros son:

```text
STCP = GPIO12
SHCP = GPIO13
DS   = GPIO14
OE   = -1
```

El valor `-1` indica que no se controlará OE desde un GPIO, ya que está conectado directamente a GND.

---

### Variable inicial

```python
x = 0x01
```

`0x01` en binario es:

```text
00000001
```

Activa el primer LED.

---

### Desplazamiento

```python
x = x << 1
```

Desplaza el bit una posición a la izquierda.

Ejemplo:

```text
00000001
00000010
00000100
00001000
```

---

### Enviar dato al 74HC595

```python
chip.shiftOut(1, x)
```

Envía el byte al registro de desplazamiento.

---

## 14. Archivo auxiliar `my74HC595.py`

Para que el código funcione, debe existir un archivo llamado:

```text
my74HC595.py
```

en la memoria del ESP32-S3.

Ejemplo de implementación didáctica:

```python
from machine import Pin
import time

class Chip74HC595:
    def __init__(self, stcp, shcp, ds, oe=-1):
        self.stcp = Pin(stcp, Pin.OUT)
        self.shcp = Pin(shcp, Pin.OUT)
        self.ds = Pin(ds, Pin.OUT)

        if oe != -1:
            self.oe = Pin(oe, Pin.OUT)
            self.oe.value(0)
        else:
            self.oe = None

        self.stcp.value(0)
        self.shcp.value(0)
        self.ds.value(0)

    def shiftOut(self, order, value):
        self.stcp.value(0)

        for i in range(8):
            if order == 1:
                bit = (value >> (7 - i)) & 1
            else:
                bit = (value >> i) & 1

            self.ds.value(bit)

            self.shcp.value(1)
            time.sleep_us(1)
            self.shcp.value(0)

        self.stcp.value(1)
        time.sleep_us(1)
        self.stcp.value(0)
```

---

## 15. Código alternativo sin librería externa

También se puede controlar el 74HC595 directamente desde `main.py`.

```python
from machine import Pin
import time

STCP = Pin(12, Pin.OUT)
SHCP = Pin(13, Pin.OUT)
DS = Pin(14, Pin.OUT)

def enviar_byte(valor):
    STCP.value(0)

    for i in range(8):
        bit = (valor >> (7 - i)) & 1
        DS.value(bit)

        SHCP.value(1)
        time.sleep_us(1)
        SHCP.value(0)

    STCP.value(1)
    time.sleep_us(1)
    STCP.value(0)

while True:
    valor = 0x01

    for i in range(8):
        enviar_byte(valor)
        valor = valor << 1
        time.sleep_ms(300)
```

---

## 16. Versión ida y vuelta

Esta versión hace que la luz vaya de izquierda a derecha y después vuelva.

```python
from machine import Pin
import time

STCP = Pin(12, Pin.OUT)
SHCP = Pin(13, Pin.OUT)
DS = Pin(14, Pin.OUT)

def enviar_byte(valor):
    STCP.value(0)

    for i in range(8):
        bit = (valor >> (7 - i)) & 1
        DS.value(bit)
        SHCP.value(1)
        time.sleep_us(1)
        SHCP.value(0)

    STCP.value(1)
    time.sleep_us(1)
    STCP.value(0)

while True:
    for i in range(8):
        enviar_byte(1 << i)
        time.sleep_ms(200)

    for i in range(6, 0, -1):
        enviar_byte(1 << i)
        time.sleep_ms(200)
```

---

## 17. Errores frecuentes

### No se enciende ningún LED

Posibles causas:

- 74HC595 mal orientado.
- VCC o GND mal conectados.
- OE no conectado a GND.
- MR no conectado correctamente.
- Código usando pines incorrectos.

---

### Solo se enciende un LED

Posibles causas:

- Error en las salidas Q0-Q7.
- Barra LED mal orientada.
- Problema con las resistencias.

---

### Los LEDs se encienden en orden inverso

Posibles causas:

- La barra LED está orientada al revés.
- El orden de bits está invertido.
- Las salidas Q0-Q7 están cableadas en sentido contrario.

Solución:

Cambiar el sentido del desplazamiento o invertir el orden de bits.

---

### La animación va demasiado rápida

Aumentar el retardo:

```python
time.sleep_ms(500)
```

---

### La animación va demasiado lenta

Reducir el retardo:

```python
time.sleep_ms(100)
```

---

## 18. Aplicaciones reales del 74HC595

El 74HC595 se utiliza en:

- Paneles LED.
- Displays de 7 segmentos.
- Matrices LED.
- Ampliación de salidas digitales.
- Automatización.
- Prototipado electrónico.
- Sistemas embebidos con pocos GPIO disponibles.

---

## 19. Retos para el alumnado

### Nivel básico

Modificar la velocidad de la animación.

---

### Nivel medio

Crear un efecto ida y vuelta.

---

### Nivel avanzado

Encender dos LEDs consecutivos.

Ejemplo:

```text
00000011
00000110
00001100
00011000
```

---

### Nivel experto

Conectar dos 74HC595 en cascada para controlar 16 LEDs.

---

## 20. Preguntas para el alumnado

1. ¿Qué es un registro de desplazamiento?
2. ¿Para qué sirve el 74HC595?
3. ¿Cuántas salidas tiene el 74HC595?
4. ¿Cuántos GPIO usa el ESP32-S3 en este proyecto?
5. ¿Qué hace el pin DS?
6. ¿Qué hace el pin SHCP?
7. ¿Qué hace el pin STCP?
8. ¿Qué significa desplazar un bit a la izquierda?
9. ¿Qué valor binario representa `0x01`?
10. ¿Qué ventaja tiene usar un 74HC595 frente a conectar cada LED directamente?

---

## 21. Criterios de evaluación

| Criterio | Logrado | No logrado |
|---------|---------|------------|
| Conecta correctamente el 74HC595 | | |
| Conecta correctamente la barra LED | | |
| Usa resistencias de 220 Ω | | |
| Configura correctamente los GPIO | | |
| Envía datos serie al 74HC595 | | |
| La animación funciona correctamente | | |
| Comprende el desplazamiento de bits | | |
| Código comentado | | |

---

## 22. Prompt optimizado para GitHub Copilot / Cursor / VS Code

Genera un archivo `main.py` para una placa ESP32-S3 WROOM usando MicroPython.

El proyecto se llama **Proyecto 13.1 Lámpara de Agua en Movimiento con 74HC595**.

Conexiones:

- GPIO12 conectado a STCP del 74HC595.
- GPIO13 conectado a SHCP del 74HC595.
- GPIO14 conectado a DS del 74HC595.
- OE del 74HC595 conectado a GND.
- Salidas Q0-Q7 conectadas a una barra LED mediante resistencias de 220 Ω.

Requisitos:

- Controlar una barra LED de 8 segmentos con un 74HC595.
- Crear una animación de luz en movimiento.
- Usar desplazamiento de bits.
- Encender un LED cada vez.
- Desplazar la luz de un extremo al otro.
- Repetir indefinidamente.
- Incluir comentarios explicativos.
- Generar una versión alternativa sin librería externa.
- Generar una versión ida y vuelta.

---

## 23. Resultado esperado

Al ejecutar el programa:

- Los LEDs de la barra se encenderán secuencialmente.
- Solo se usarán unos pocos GPIO del ESP32-S3.
- El 74HC595 transformará los datos serie en salidas paralelas.
- El efecto visual será una lámpara de agua en movimiento.

Este proyecto demuestra cómo ampliar las salidas digitales del ESP32-S3 utilizando un registro de desplazamiento.
