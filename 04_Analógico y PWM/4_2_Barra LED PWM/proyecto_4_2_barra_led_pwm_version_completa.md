# Proyecto 4.2 – Barra LED con PWM  
## Flowing Light avanzado con ESP32-S3 WROOM y MicroPython

---

## 1. Objetivo del proyecto

El objetivo de este proyecto es utilizar **PWM (Pulse Width Modulation)** para controlar una barra de LED conectada a una placa **ESP32-S3 WROOM**.

En el proyecto anterior de *Flowing Light*, los LEDs solo se encendían y apagaban. En este proyecto se mejora el efecto utilizando PWM, de forma que los LEDs puedan tener distintos niveles de brillo.

El resultado será una luz fluida más atractiva, donde un LED principal se ilumina con brillo máximo y los LEDs cercanos pueden iluminarse con menor intensidad, creando un efecto de desplazamiento suave.

---

## 2. Descripción general

Este proyecto consiste en crear una animación luminosa sobre una barra LED.

La luz debe desplazarse de un extremo al otro de la barra LED. Para mejorar el efecto visual, no solo se encenderá un LED cada vez, sino que se utilizarán distintos niveles de brillo mediante PWM.

Ejemplo visual simplificado:

```text
█▓░░░░░░
░█▓░░░░░
░░█▓░░░░
░░░█▓░░░
░░░░█▓░░
░░░░░█▓░
░░░░░░█▓
░░░░░░░█
```

Leyenda:

```text
█ = LED principal, brillo máximo
▓ = LED vecino, brillo medio
░ = LED apagado
```

---

## 3. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3 WROOM | 1 |
| Placa de extensión GPIO | 1 |
| Protoboard de 830 puntos | 1 |
| Barra LED | 1 |
| Resistencias de 220 Ω | 8 |
| Cables de conexión Dupont | 8 |

---

## 4. Objetivos de aprendizaje

Al finalizar este proyecto, el alumno debe ser capaz de:

1. Comprender qué es una señal PWM.
2. Diferenciar entre encendido digital y control de brillo mediante PWM.
3. Configurar varios GPIO del ESP32-S3 como salidas PWM.
4. Utilizar listas en MicroPython para controlar varios LEDs.
5. Crear una animación secuencial.
6. Ajustar la velocidad de una animación mediante retardos.
7. Modificar el brillo de los LEDs mediante `duty_u16()`.
8. Interpretar errores típicos de conexión y programación.

---

## 5. Pines utilizados

Se utilizarán 8 segmentos de la barra LED.

| Segmento de la barra LED | GPIO ESP32-S3 | Resistencia |
|--------------------------|---------------|-------------|
| LED 1 | GPIO 4 | 220 Ω |
| LED 2 | GPIO 5 | 220 Ω |
| LED 3 | GPIO 6 | 220 Ω |
| LED 4 | GPIO 7 | 220 Ω |
| LED 5 | GPIO 15 | 220 Ω |
| LED 6 | GPIO 16 | 220 Ω |
| LED 7 | GPIO 17 | 220 Ω |
| LED 8 | GPIO 18 | 220 Ω |


---

## 6. Tabla detallada de conexiones

| Elemento | Terminal | Conexión |
|----------|----------|----------|
| ESP32-S3 | GPIO 4 | Resistencia 220 Ω del LED 1 |
| ESP32-S3 | GPIO 5 | Resistencia 220 Ω del LED 2 |
| ESP32-S3 | GPIO 6 | Resistencia 220 Ω del LED 3 |
| ESP32-S3 | GPIO 7 | Resistencia 220 Ω del LED 4 |
| ESP32-S3 | GPIO 15 | Resistencia 220 Ω del LED 5 |
| ESP32-S3 | GPIO 16 | Resistencia 220 Ω del LED 6 |
| ESP32-S3 | GPIO 17 | Resistencia 220 Ω del LED 7 |
| ESP32-S3 | GPIO 18 | Resistencia 220 Ω del LED 8 |
| Cada resistencia | Extremo 1 | GPIO correspondiente |
| Cada resistencia | Extremo 2 | Ánodo del segmento LED correspondiente |
| Barra LED | Cátodos | GND |
| ESP32-S3 | GND | Línea común de GND de la protoboard |

---

## 7. Esquema ASCII del circuito

```text
                         ESP32-S3 WROOM
                    +----------------------+
                    |                      |
GPIO 4  ------------+                      |
                    |                      |
GPIO 5  ------------+                      |
                    |                      |
GPIO 6  ------------+                      |
                    |                      |
GPIO 7  ------------+                      |
                    |                      |
GPIO 15 ------------+                      |
                    |                      |
GPIO 16 ------------+                      |
                    |                      |
GPIO 17 ------------+                      |
                    |                      |
GPIO 18 ------------+                      |
                    |                      |
GND    -------------+                      |
                    +----------------------+

Conexión de cada segmento:

GPIO 4  ----[220 Ω]---->| LED 1 ---- GND
GPIO 5  ----[220 Ω]---->| LED 2 ---- GND
GPIO 6  ----[220 Ω]---->| LED 3 ---- GND
GPIO 7  ----[220 Ω]---->| LED 4 ---- GND
GPIO 15 ----[220 Ω]---->| LED 5 ---- GND
GPIO 16 ----[220 Ω]---->| LED 6 ---- GND
GPIO 17 ----[220 Ω]---->| LED 7 ---- GND
GPIO 18 ----[220 Ω]---->| LED 8 ---- GND
```

---

## 8. Nota importante sobre la barra LED

La barra LED tiene polaridad. Cada segmento interno se comporta como un LED independiente.

Si no se enciende ningún segmento, revisar:

- Que la barra LED no esté colocada al revés.
- Que el lado común esté conectado correctamente a GND.
- Que las resistencias estén en serie con cada segmento.
- Que se estén usando los GPIO correctos.
- Que la placa comparta GND con la protoboard.

---

## 9. Fundamentos teóricos

### 9.1 ¿Qué es PWM?

PWM significa **Pulse Width Modulation**, o **modulación por ancho de pulso**.

Un GPIO digital solo puede generar dos estados:

```text
0 = apagado = 0 V
1 = encendido = 3,3 V
```

Sin embargo, si el pin se enciende y apaga muy rápidamente, el ojo humano no percibe el parpadeo, sino un nivel de brillo medio.

---

### 9.2 Duty Cycle

El **duty cycle** indica el porcentaje de tiempo que la señal permanece encendida dentro de cada ciclo.

| Duty Cycle | Estado visual del LED |
|------------|-----------------------|
| 0 % | Apagado |
| 25 % | Brillo bajo |
| 50 % | Brillo medio |
| 75 % | Brillo alto |
| 100 % | Brillo máximo |

Ejemplo:

```text
Duty Cycle 25 %

ENCENDIDO: █
APAGADO:   ░░░
Resultado: brillo bajo
```

```text
Duty Cycle 75 %

ENCENDIDO: ███
APAGADO:   ░
Resultado: brillo alto
```

---

### 9.3 PWM en MicroPython

En MicroPython se utiliza la clase `PWM` del módulo `machine`.

Ejemplo:

```python
from machine import Pin, PWM

led = PWM(Pin(4))
led.freq(1000)
led.duty_u16(32768)
```

La función:

```python
led.freq(1000)
```

configura la frecuencia PWM en 1000 Hz.

La función:

```python
led.duty_u16(valor)
```

controla el brillo.

Valores habituales:

| Valor `duty_u16()` | Brillo |
|--------------------|--------|
| 0 | Apagado |
| 10000 | Bajo |
| 25000 | Medio-bajo |
| 40000 | Medio-alto |
| 65535 | Máximo |

---

## 10. Funcionamiento esperado del programa

El programa debe:

1. Configurar los 8 GPIO como salidas PWM.
2. Apagar todos los LEDs al iniciar.
3. Encender el LED principal con brillo máximo.
4. Encender el LED vecino con brillo medio.
5. Mantener apagados el resto de LEDs.
6. Desplazar el efecto hacia la derecha.
7. Repetir indefinidamente.

Ejemplo de secuencia:

```text
Paso 1: █▓░░░░░░
Paso 2: ░█▓░░░░░
Paso 3: ░░█▓░░░░
Paso 4: ░░░█▓░░░
Paso 5: ░░░░█▓░░
Paso 6: ░░░░░█▓░
Paso 7: ░░░░░░█▓
Paso 8: ░░░░░░░█
```

---

## 11. Requisitos obligatorios del código

El archivo `main.py` generado debe cumplir estos requisitos:

1. Usar MicroPython.
2. Importar `Pin` y `PWM` desde `machine`.
3. Importar `time`.
4. Usar los GPIO 4, 5, 6, 7, 15, 16, 17 y 18.
5. Crear una lista con los pines.
6. Crear una lista de objetos PWM.
7. Configurar todos los PWM a 1000 Hz.
8. Usar `duty_u16()` para controlar el brillo.
9. Crear una animación de luz fluida.
10. Ejecutarse en un bucle infinito.
11. Apagar todos los LEDs antes de pasar al siguiente paso.
12. Utilizar comentarios claros.
13. Utilizar nombres de variables comprensibles.
14. Ser fácil de entender para alumnado principiante.

---

## 12. Código de referencia esperado

```python
from machine import Pin, PWM
import time

# Pines GPIO conectados a los segmentos de la barra LED
pines_led = [4, 5, 6, 7, 15, 16, 17, 18]

# Crear objetos PWM para cada LED
leds = []

for pin in pines_led:
    led = PWM(Pin(pin))
    led.freq(1000)
    led.duty_u16(0)
    leds.append(led)

# Niveles de brillo
APAGADO = 0
BRILLO_MEDIO = 25000
BRILLO_MAXIMO = 65535

while True:
    for posicion in range(len(leds)):

        # Apagar todos los LEDs antes de dibujar el nuevo paso
        for led in leds:
            led.duty_u16(APAGADO)

        # LED principal con brillo máximo
        leds[posicion].duty_u16(BRILLO_MAXIMO)

        # LED siguiente con brillo medio, si existe
        if posicion + 1 < len(leds):
            leds[posicion + 1].duty_u16(BRILLO_MEDIO)

        # Retardo para controlar la velocidad de la animación
        time.sleep_ms(120)
```

---

## 13. Código alternativo: efecto ida y vuelta

Este código genera un efecto similar al de una luz que va y vuelve.

```python
from machine import Pin, PWM
import time

pines_led = [4, 5, 6, 7, 15, 16, 17, 18]

leds = []

for pin in pines_led:
    led = PWM(Pin(pin))
    led.freq(1000)
    led.duty_u16(0)
    leds.append(led)

APAGADO = 0
BRILLO_SUAVE = 12000
BRILLO_MEDIO = 30000
BRILLO_MAXIMO = 65535

def apagar_todos():
    for led in leds:
        led.duty_u16(APAGADO)

def mostrar_posicion(posicion):
    apagar_todos()

    leds[posicion].duty_u16(BRILLO_MAXIMO)

    if posicion - 1 >= 0:
        leds[posicion - 1].duty_u16(BRILLO_MEDIO)

    if posicion + 1 < len(leds):
        leds[posicion + 1].duty_u16(BRILLO_MEDIO)

while True:
    for posicion in range(len(leds)):
        mostrar_posicion(posicion)
        time.sleep_ms(100)

    for posicion in range(len(leds) - 2, 0, -1):
        mostrar_posicion(posicion)
        time.sleep_ms(100)
```

---

## 14. Errores frecuentes

### 14.1 Ningún LED se enciende

Posibles causas:

- La placa no está alimentada.
- La barra LED está conectada al revés.
- Falta la conexión GND.
- Los GPIO del código no coinciden con el cableado.
- Las resistencias no están bien colocadas.

Solución:

- Revisar primero GND.
- Probar un único LED con un código sencillo.
- Verificar la orientación de la barra LED.

---

### 14.2 Solo se enciende un LED

Posibles causas:

- Solo un GPIO está correctamente conectado.
- Hay un error en la lista de pines.
- La barra LED no está bien insertada en la protoboard.

Solución:

- Revisar la lista:

```python
pines_led = [4, 5, 6, 7, 15, 16, 17, 18]
```

- Comprobar los cables uno a uno.

---

### 14.3 Los LEDs se encienden en orden incorrecto

Posibles causas:

- El orden de los cables no coincide con el orden de la lista.
- La barra LED está orientada al revés.

Solución:

- Cambiar el orden de la lista de pines.
- No es necesario cambiar el programa entero.

Ejemplo:

```python
pines_led = [18, 17, 16, 15, 7, 6, 5, 4]
```

---

### 14.4 El efecto va demasiado rápido

Solución:

Aumentar el retardo:

```python
time.sleep_ms(200)
```

---

### 14.5 El efecto va demasiado lento

Solución:

Reducir el retardo:

```python
time.sleep_ms(60)
```

---

### 14.6 El efecto se ve brusco

Posibles causas:

- Solo se usan dos niveles de brillo.
- El retardo es demasiado alto.
- No hay LEDs vecinos con brillo intermedio.

Solución:

Añadir más niveles de brillo:

```python
BRILLO_SUAVE = 10000
BRILLO_MEDIO = 30000
BRILLO_MAXIMO = 65535
```

---

## 15. Propuesta de ampliaciones para clase

### Nivel básico

Modificar la velocidad de desplazamiento cambiando el valor de:

```python
time.sleep_ms(120)
```

---

### Nivel medio

Invertir el sentido de la animación.

---

### Nivel medio-alto

Crear un efecto de ida y vuelta.

---

### Nivel avanzado

Crear un efecto tipo **Knight Rider**.

---

### Nivel experto

Añadir un potenciómetro conectado a una entrada ADC para controlar la velocidad de la animación.

---

## 16. Preguntas para el alumnado

1. ¿Qué significa PWM?
2. ¿Qué diferencia hay entre encender un LED con `value(1)` y controlar su brillo con `duty_u16()`?
3. ¿Qué valor de `duty_u16()` corresponde al brillo máximo?
4. ¿Por qué es necesario usar una resistencia con cada LED?
5. ¿Qué pasaría si conectamos un LED directamente al GPIO sin resistencia?
6. ¿Cómo podrías hacer que la animación fuera más lenta?
7. ¿Cómo podrías invertir el sentido de desplazamiento?
8. ¿Qué ventaja tiene usar listas para controlar varios LEDs?

---

## 17. Criterios de evaluación

| Criterio | Logrado | No logrado |
|----------|---------|------------|
| Conecta correctamente la barra LED |  |  |
| Usa resistencias de 220 Ω |  |  |
| Configura correctamente los GPIO |  |  |
| Usa PWM en todos los LEDs |  |  |
| El programa se ejecuta sin errores |  |  |
| La animación se desplaza correctamente |  |  |
| El código está comentado |  |  |
| El alumno entiende el funcionamiento básico |  |  |

---

## 18. Prompt optimizado para GitHub Copilot / Cursor / IA de VS Code

Genera un archivo `main.py` para MicroPython destinado a una placa ESP32-S3 WROOM.

El proyecto consiste en controlar una barra LED usando PWM para crear un efecto de luz fluida.

Requisitos técnicos:

- Utilizar los GPIO 4, 5, 6, 7, 15, 16, 17, 18, 8 y 3.
- Cada GPIO controla un segmento de la barra LED.
- Cada segmento tiene una resistencia de 220 Ω.
- Todos los LEDs comparten GND.
- Utilizar la clase `PWM` del módulo `machine`.
- Configurar todos los PWM con frecuencia de 1000 Hz.
- Usar `duty_u16()` para controlar el brillo.
- Crear una lista de pines y una lista de objetos PWM.
- El LED principal debe iluminarse con brillo máximo.
- El LED vecino debe iluminarse con brillo medio.
- El resto de LEDs deben permanecer apagados.
- La animación debe desplazarse de izquierda a derecha.
- El programa debe ejecutarse indefinidamente.
- El código debe estar comentado.
- El código debe ser sencillo y adecuado para alumnado principiante de Formación Profesional.

Genera un código claro, estructurado y fácil de modificar.

---

## 19. Resultado esperado

Al ejecutar el archivo `main.py` en el ESP32-S3 WROOM, la barra LED mostrará una luz que se desplaza suavemente por los segmentos, usando diferentes niveles de brillo gracias al PWM.

El alumno deberá observar que el efecto es más suave y visualmente más atractivo que el encendido y apagado simple de LEDs.
