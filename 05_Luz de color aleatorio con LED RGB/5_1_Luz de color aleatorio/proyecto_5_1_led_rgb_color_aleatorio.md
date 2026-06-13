# Proyecto 5.1 – Luz de color aleatorio con LED RGB
## ESP32-S3 WROOM + MicroPython

---

# 1. Objetivo del proyecto

En este proyecto aprenderemos a controlar un LED RGB utilizando PWM.

Un LED RGB contiene tres LEDs internos:

- Rojo (Red)
- Verde (Green)
- Azul (Blue)

Combinando diferentes niveles de brillo en cada color podemos generar millones de colores distintos.

El objetivo es crear una luz multicolor que cambie automáticamente de color utilizando valores aleatorios.

---

# 2. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| LED RGB | 1 |
| Resistencias 220 Ω | 3 |
| Cables Dupont | 4 |

---

# 3. Objetivos de aprendizaje

- Comprender el funcionamiento de un LED RGB.
- Aprender a utilizar PWM en varios canales simultáneamente.
- Generar colores mezclando rojo, verde y azul.
- Utilizar números aleatorios en MicroPython.
- Crear efectos luminosos dinámicos.

---

# 4. Conexiones

Según el montaje mostrado:

| Color LED RGB | GPIO ESP32-S3 |
|--------------|---------------|
| Rojo | GPIO 42 |
| Verde | GPIO 41 |
| Azul | GPIO 40 |
| Terminal común | GND |

Cada color debe conectarse mediante una resistencia de 220 Ω.

---

# 5. Esquema ASCII

```text
                 ESP32-S3

GPIO 42 ----[220Ω]---- Rojo
GPIO 41 ----[220Ω]---- Verde
GPIO 40 ----[220Ω]---- Azul

                       |
                       |
                    LED RGB
                       |
                       |
                      GND
```

---

# 6. Fundamentos teóricos

## ¿Qué es un LED RGB?

Un LED RGB contiene tres LEDs independientes dentro del mismo encapsulado:

```text
R = Red (Rojo)
G = Green (Verde)
B = Blue (Azul)
```

Al variar el brillo de cada uno mediante PWM se pueden generar diferentes colores.

Ejemplos:

| Rojo | Verde | Azul | Color |
|-------|--------|------|--------|
| 255 | 0 | 0 | Rojo |
| 0 | 255 | 0 | Verde |
| 0 | 0 | 255 | Azul |
| 255 | 255 | 0 | Amarillo |
| 255 | 0 | 255 | Magenta |
| 0 | 255 | 255 | Cian |
| 255 | 255 | 255 | Blanco |

---

## PWM

PWM (Pulse Width Modulation) permite controlar el brillo de cada color.

En MicroPython:

```python
led.duty_u16(valor)
```

donde:

```text
0      = apagado
65535  = brillo máximo
```

---

# 7. Funcionamiento esperado

El programa debe:

1. Crear tres canales PWM.
2. Uno para el color rojo.
3. Uno para el color verde.
4. Uno para el color azul.
5. Generar valores aleatorios para cada color.
6. Aplicar esos valores mediante PWM.
7. Mostrar el nuevo color durante un tiempo.
8. Repetir indefinidamente.

Ejemplo:

```text
Color 1 -> Rojo
Color 2 -> Azul
Color 3 -> Verde
Color 4 -> Amarillo
Color 5 -> Rosa
Color 6 -> Turquesa
...
```

---

# 8. Requisitos obligatorios

El archivo main.py debe:

1. Utilizar MicroPython.
2. Importar Pin y PWM.
3. Importar random.
4. Configurar tres canales PWM.
5. Utilizar frecuencia PWM de 1000 Hz.
6. Generar colores aleatorios.
7. Cambiar automáticamente cada segundo.
8. Ejecutarse indefinidamente.
9. Incluir comentarios explicativos.

---

# 9. Código de referencia esperado

```python
from machine import Pin, PWM
import random
import time

rojo = PWM(Pin(42))
verde = PWM(Pin(41))
azul = PWM(Pin(40))

for led in (rojo, verde, azul):
    led.freq(1000)

while True:

    rojo.duty_u16(random.randint(0, 65535))
    verde.duty_u16(random.randint(0, 65535))
    azul.duty_u16(random.randint(0, 65535))

    time.sleep(1)
```

---

# 10. Errores frecuentes

## El LED siempre aparece apagado

- Revisar la conexión común.
- Revisar las resistencias.
- Revisar el GPIO utilizado.

## Solo aparece un color

- Uno de los canales RGB está mal conectado.
- Una resistencia está desconectada.

## Los colores no cambian

- Falta importar random.
- El bucle principal no se está ejecutando.

## El LED parece blanco casi siempre

- Los valores aleatorios son muy altos en los tres canales.
- Probar escalando los valores PWM.

---

# 11. Retos para el alumnado

## Nivel básico

Cambiar el color cada 2 segundos.

## Nivel medio

Crear colores predefinidos usando una lista.

## Nivel avanzado

Crear una transición suave entre colores.

## Nivel experto

Crear una lámpara RGB controlada mediante un potenciómetro o mediante WiFi.

---

# 12. Prompt optimizado para GitHub Copilot

Genera un archivo main.py para una placa ESP32-S3 WROOM utilizando MicroPython.

Requisitos:

- Utilizar un LED RGB.
- GPIO 42 para rojo.
- GPIO 41 para verde.
- GPIO 40 para azul.
- Utilizar PWM a 1000 Hz.
- Crear tres canales PWM.
- Generar valores aleatorios para cada color.
- Mostrar un nuevo color cada segundo.
- Ejecutarse indefinidamente.
- Código comentado y fácil de entender.
