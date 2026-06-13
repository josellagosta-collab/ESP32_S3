# Proyecto 14.1 – Pantalla de 7 segmentos con 74HC595
## ESP32-S3 WROOM + MicroPython

---

## 1. Objetivo del proyecto

En este proyecto aprenderemos a controlar una **pantalla de 7 segmentos** usando un **registro de desplazamiento 74HC595** y una placa **ESP32-S3 WROOM**.

La pantalla de 7 segmentos permite mostrar números y algunos caracteres sencillos. En este proyecto se mostrarán caracteres numéricos del **0 al 9**.

El uso del 74HC595 permite controlar varios segmentos utilizando pocos pines GPIO del ESP32-S3.

---

## 2. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3-WROOM | 1 |
| Placa de expansión GPIO | 1 |
| Protoboard de 830 puntos | 1 |
| 74HC595 | 1 |
| Pantalla de 7 segmentos de 1 dígito | 1 |
| Resistencias de 220 Ω | 8 |
| Cables Dupont | Varios |

---

## 3. Objetivos de aprendizaje

Al finalizar esta práctica, el alumno debe ser capaz de:

1. Comprender el funcionamiento de una pantalla de 7 segmentos.
2. Identificar los segmentos A, B, C, D, E, F, G y DP.
3. Usar el 74HC595 para ampliar salidas digitales.
4. Enviar datos serie desde el ESP32-S3.
5. Convertir datos serie en salidas paralelas.
6. Mostrar números del 0 al 9.
7. Comprender el uso de tablas de patrones binarios.
8. Ahorrar pines GPIO en sistemas embebidos.

---

## 4. ¿Qué es una pantalla de 7 segmentos?

Una pantalla de 7 segmentos está formada por siete LEDs colocados de forma que permiten representar números.

Los segmentos se llaman:

```text
     A
   -----
F |     | B
  |  G  |
   -----
E |     | C
  |     |
   -----
     D
```

Además, muchas pantallas incorporan un punto decimal:

```text
DP
```

Por tanto, una pantalla de 7 segmentos suele tener 8 LEDs internos:

- A
- B
- C
- D
- E
- F
- G
- DP

---

## 5. Tipos de pantalla de 7 segmentos

Existen dos tipos principales:

| Tipo | Característica |
|------|----------------|
| Cátodo común | Los cátodos están unidos a GND |
| Ánodo común | Los ánodos están unidos a VCC |

En este proyecto se asumirá una pantalla de **cátodo común**, donde un segmento se enciende enviando un `1`.

Si tu pantalla es de ánodo común, puede ser necesario invertir los bits.

---

## 6. ¿Por qué usar un 74HC595?

Si conectamos la pantalla directamente al ESP32-S3, necesitaríamos hasta 8 GPIO:

| Segmento | GPIO necesario |
|----------|----------------|
| A | 1 |
| B | 1 |
| C | 1 |
| D | 1 |
| E | 1 |
| F | 1 |
| G | 1 |
| DP | 1 |

Con el 74HC595 podemos controlar esos 8 segmentos utilizando solo 3 GPIO principales:

- DS
- SHCP
- STCP

Esto permite ahorrar pines para otros sensores o actuadores.

---

## 7. ¿Qué es el 74HC595?

El 74HC595 es un **registro de desplazamiento de 8 bits con salidas paralelas**.

Permite enviar un byte desde el ESP32-S3 bit a bit y obtener 8 salidas digitales.

Funcionamiento:

```text
ESP32-S3 envía 8 bits en serie
              ↓
           74HC595
              ↓
8 salidas paralelas Q0-Q7
              ↓
Segmentos de la pantalla
```

---

## 8. Pines principales del 74HC595

| Pin 74HC595 | Nombre | Función |
|------------|--------|---------|
| DS | Data | Entrada de datos serie |
| SHCP | Shift Clock | Reloj de desplazamiento |
| STCP | Storage Clock / Latch | Actualiza salidas |
| OE | Output Enable | Habilita salidas |
| MR | Master Reset | Reinicio del registro |
| Q0-Q7 | Salidas | Salidas paralelas |
| VCC | Alimentación | 3.3 V / 5 V |
| GND | Tierra | GND |

---

## 9. Conexiones del ESP32-S3 al 74HC595

Basándonos en el proyecto anterior con 74HC595, se utilizarán los mismos GPIO:

| ESP32-S3 | 74HC595 | Función |
|---------|---------|---------|
| GPIO 12 | STCP | Latch |
| GPIO 13 | SHCP | Clock |
| GPIO 14 | DS | Data |
| GND | OE | Habilitar salidas |
| 3.3 V | VCC | Alimentación |
| GND | GND | Tierra |

---

## 10. Conexiones del 74HC595 a la pantalla de 7 segmentos

Las salidas Q0-Q7 del 74HC595 se conectan a los segmentos de la pantalla mediante resistencias de 220 Ω.

Una asignación habitual es:

| Salida 74HC595 | Segmento |
|---------------|----------|
| Q0 | A |
| Q1 | B |
| Q2 | C |
| Q3 | D |
| Q4 | E |
| Q5 | F |
| Q6 | G |
| Q7 | DP |

Cada segmento debe llevar una resistencia de 220 Ω en serie.

---

## 11. Tabla detallada de conexiones

| Elemento | Terminal | Conexión |
|----------|----------|----------|
| ESP32-S3 | GPIO 12 | STCP del 74HC595 |
| ESP32-S3 | GPIO 13 | SHCP del 74HC595 |
| ESP32-S3 | GPIO 14 | DS del 74HC595 |
| ESP32-S3 | GND | OE del 74HC595 |
| ESP32-S3 | 3.3 V | VCC del 74HC595 |
| ESP32-S3 | GND | GND del 74HC595 |
| 74HC595 | Q0 | Segmento A mediante 220 Ω |
| 74HC595 | Q1 | Segmento B mediante 220 Ω |
| 74HC595 | Q2 | Segmento C mediante 220 Ω |
| 74HC595 | Q3 | Segmento D mediante 220 Ω |
| 74HC595 | Q4 | Segmento E mediante 220 Ω |
| 74HC595 | Q5 | Segmento F mediante 220 Ω |
| 74HC595 | Q6 | Segmento G mediante 220 Ω |
| 74HC595 | Q7 | Punto decimal DP mediante 220 Ω |

---

## 12. Esquema ASCII simplificado

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
 DATA  ------>| DS                Q0 |----[220Ω]---- A
 CLOCK ------>| SHCP              Q1 |----[220Ω]---- B
 LATCH ------>| STCP              Q2 |----[220Ω]---- C
 OE    ------>| OE                Q3 |----[220Ω]---- D
              |                   Q4 |----[220Ω]---- E
              |                   Q5 |----[220Ω]---- F
              |                   Q6 |----[220Ω]---- G
              |                   Q7 |----[220Ω]---- DP
              +----------------------+

                 Pantalla 7 segmentos
```

---

## 13. Representación de números

Para mostrar un número se encienden varios segmentos.

### Número 0

Se encienden:

```text
A, B, C, D, E, F
```

Se apaga:

```text
G
```

### Número 1

Se encienden:

```text
B, C
```

### Número 8

Se encienden todos:

```text
A, B, C, D, E, F, G
```

---

## 14. Tabla de segmentos para los números 0-9

| Número | Segmentos encendidos |
|--------|----------------------|
| 0 | A B C D E F |
| 1 | B C |
| 2 | A B D E G |
| 3 | A B C D G |
| 4 | B C F G |
| 5 | A C D F G |
| 6 | A C D E F G |
| 7 | A B C |
| 8 | A B C D E F G |
| 9 | A B C D F G |

---

## 15. Patrones binarios

Si usamos la relación:

```text
Q0 = A
Q1 = B
Q2 = C
Q3 = D
Q4 = E
Q5 = F
Q6 = G
Q7 = DP
```

Los números pueden representarse con estos patrones:

| Número | Binario | Hexadecimal |
|--------|---------|-------------|
| 0 | 00111111 | 0x3F |
| 1 | 00000110 | 0x06 |
| 2 | 01011011 | 0x5B |
| 3 | 01001111 | 0x4F |
| 4 | 01100110 | 0x66 |
| 5 | 01101101 | 0x6D |
| 6 | 01111101 | 0x7D |
| 7 | 00000111 | 0x07 |
| 8 | 01111111 | 0x7F |
| 9 | 01101111 | 0x6F |

---

## 16. Funcionamiento esperado del proyecto

El programa debe:

1. Configurar los GPIO del 74HC595.
2. Crear una tabla con los patrones de los números 0-9.
3. Enviar un patrón al 74HC595.
4. Mostrar el número correspondiente en la pantalla.
5. Esperar un tiempo.
6. Pasar al siguiente número.
7. Repetir continuamente.

---

## 17. Código de referencia sin librería externa

Este código controla directamente el 74HC595 desde `main.py`.

```python
from machine import Pin
import time

# Pines conectados al 74HC595
STCP = Pin(12, Pin.OUT)   # Latch
SHCP = Pin(13, Pin.OUT)   # Clock
DS = Pin(14, Pin.OUT)     # Data

# Patrones para pantalla de 7 segmentos de cátodo común
# Q0=A, Q1=B, Q2=C, Q3=D, Q4=E, Q5=F, Q6=G, Q7=DP
numeros = [
    0x3F,  # 0
    0x06,  # 1
    0x5B,  # 2
    0x4F,  # 3
    0x66,  # 4
    0x6D,  # 5
    0x7D,  # 6
    0x07,  # 7
    0x7F,  # 8
    0x6F   # 9
]

def enviar_byte(valor):
    # Envía un byte al 74HC595
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
    for numero in numeros:
        enviar_byte(numero)
        time.sleep(1)
```

---

## 18. Código usando librería `my74HC595.py`

Si se utiliza la librería del proyecto anterior:

```python
import time
from my74HC595 import Chip74HC595

chip = Chip74HC595(12, 13, 14, -1)

numeros = [
    0x3F,
    0x06,
    0x5B,
    0x4F,
    0x66,
    0x6D,
    0x7D,
    0x07,
    0x7F,
    0x6F
]

while True:
    for numero in numeros:
        chip.shiftOut(1, numero)
        time.sleep(1)
```

---

## 19. Archivo auxiliar `my74HC595.py`

Si se usa la librería, debe existir en el ESP32-S3 un archivo llamado:

```text
my74HC595.py
```

Ejemplo:

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

## 20. Versión con cuenta regresiva

```python
from machine import Pin
import time

STCP = Pin(12, Pin.OUT)
SHCP = Pin(13, Pin.OUT)
DS = Pin(14, Pin.OUT)

numeros = [
    0x3F,
    0x06,
    0x5B,
    0x4F,
    0x66,
    0x6D,
    0x7D,
    0x07,
    0x7F,
    0x6F
]

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
    for i in range(9, -1, -1):
        enviar_byte(numeros[i])
        time.sleep(1)
```

---

## 21. Versión para ánodo común

Si la pantalla es de ánodo común, los bits se invierten:

```python
enviar_byte(255 - numeros[i])
```

Ejemplo:

```python
while True:
    for numero in numeros:
        enviar_byte(255 - numero)
        time.sleep(1)
```

---

## 22. Errores frecuentes

### No se enciende ningún segmento

Posibles causas:

- Pantalla mal orientada.
- 74HC595 mal orientado.
- GND o VCC mal conectados.
- OE no conectado a GND.
- MR no conectado correctamente.
- Código usando GPIO incorrectos.

---

### Se encienden segmentos incorrectos

Posibles causas:

- Q0-Q7 no coinciden con A-G.
- Tabla de patrones incorrecta.
- Orden de bits invertido.

Solución:

- Cambiar el orden de los cables.
- Modificar la tabla de patrones.
- Invertir el orden en `enviar_byte()`.

---

### Los números aparecen al revés o sin sentido

Posibles causas:

- Pantalla de ánodo común en vez de cátodo común.
- Segmentos conectados en otro orden.
- Código pensado para otra asignación de pines.

---

### La pantalla muestra siempre 8

Posibles causas:

- Salidas del 74HC595 siempre activas.
- Cortocircuitos.
- Tabla incorrecta.
- Pantalla mal conectada.

---

### La pantalla no cambia de número

Posibles causas:

- Pin STCP no funciona.
- No se actualiza el latch.
- Error en la función `enviar_byte()`.

---

## 23. Aplicaciones reales

Las pantallas de 7 segmentos se utilizan en:

- Relojes digitales.
- Contadores.
- Temporizadores.
- Multímetros.
- Fuentes de alimentación.
- Electrodomésticos.
- Paneles industriales.
- Básculas electrónicas.
- Indicadores de producción.

---

## 24. Retos para el alumnado

### Nivel básico

Modificar el retardo entre números.

---

### Nivel medio

Crear una cuenta regresiva de 9 a 0.

---

### Nivel avanzado

Mostrar solo números pares:

```text
0, 2, 4, 6, 8
```

---

### Nivel avanzado 2

Mostrar solo números impares:

```text
1, 3, 5, 7, 9
```

---

### Nivel experto

Conectar dos displays de 7 segmentos usando dos 74HC595 en cascada.

---

## 25. Preguntas para el alumnado

1. ¿Qué es una pantalla de 7 segmentos?
2. ¿Cuántos segmentos tiene una pantalla de 7 segmentos?
3. ¿Qué función tiene el punto decimal DP?
4. ¿Qué diferencia hay entre cátodo común y ánodo común?
5. ¿Para qué sirve el 74HC595?
6. ¿Qué hace el pin DS?
7. ¿Qué hace el pin SHCP?
8. ¿Qué hace el pin STCP?
9. ¿Por qué se usan resistencias de 220 Ω?
10. ¿Qué ventaja tiene usar un 74HC595 en este proyecto?

---

## 26. Criterios de evaluación

| Criterio | Logrado | No logrado |
|---------|---------|------------|
| Cablea correctamente el 74HC595 | | |
| Cablea correctamente el display | | |
| Usa resistencias en los segmentos | | |
| Configura correctamente los GPIO | | |
| Envía datos al 74HC595 | | |
| Muestra números del 0 al 9 | | |
| Comprende la tabla de segmentos | | |
| Código comentado | | |

---

## 27. Prompt optimizado para GitHub Copilot / Cursor / VS Code

A a partir de la expecificaciones que encontrarás en el archivo .md de este proyecto genera un archivo `main.py` para una placa ESP32-S3 WROOM usando MicroPython.

El proyecto se llama **Proyecto 14.1 Pantalla de 7 segmentos con 74HC595**.

Conexiones:

- GPIO12 conectado a STCP del 74HC595.
- GPIO13 conectado a SHCP del 74HC595.
- GPIO14 conectado a DS del 74HC595.
- OE del 74HC595 conectado a GND.
- Q0-Q7 conectados a los segmentos A, B, C, D, E, F, G y DP mediante resistencias de 220 Ω.
- Display de 7 segmentos de cátodo común.

Requisitos:

- Controlar una pantalla de 7 segmentos con un 74HC595.
- Mostrar los números del 0 al 9.
- Usar una tabla de patrones hexadecimales.
- Actualizar la pantalla cada segundo.
- Incluir comentarios explicativos.
- Añadir una función `enviar_byte(valor)`.
- Crear una versión alternativa con cuenta regresiva.
- Explicar cómo invertir los bits para una pantalla de ánodo común.

---

## 28. Resultado esperado

Al ejecutar el programa:

- La pantalla de 7 segmentos mostrará los números del 0 al 9.
- Cada número permanecerá visible aproximadamente 1 segundo.
- El ESP32-S3 controlará la pantalla usando pocos GPIO gracias al 74HC595.
- El alumno comprenderá cómo una tabla de patrones permite representar números en una pantalla de segmentos.
