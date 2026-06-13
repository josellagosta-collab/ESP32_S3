# Proyecto 16.2 – Servo Knob (Control de Servomotor mediante Potenciómetro)

## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# 1. Introducción

En el proyecto anterior aprendimos a mover un servomotor automáticamente realizando un barrido entre 0° y 180°.

En este nuevo proyecto el movimiento ya no será automático. El usuario controlará manualmente la posición del servomotor utilizando un potenciómetro.

Al girar el potenciómetro:

```text
Potenciómetro a la izquierda  → Servo en 0°

Potenciómetro al centro      → Servo en 90°

Potenciómetro a la derecha   → Servo en 180°
```

Este sistema es similar al funcionamiento de:

- Mandos de control remoto.
- Joysticks industriales.
- Brazos robóticos.
- Sistemas de dirección servoasistida.
- Antenas orientables.

---

# 2. Objetivos del proyecto

Al finalizar esta práctica el alumno será capaz de:

- Leer señales analógicas mediante ADC.
- Utilizar un potenciómetro como dispositivo de entrada.
- Convertir valores ADC en posiciones angulares.
- Controlar un servomotor mediante PWM.
- Realizar conversiones matemáticas entre rangos de valores.
- Comprender el concepto de mapeo de señales.

---

# 3. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| Servomotor SG90 o compatible | 1 |
| Potenciómetro 10kΩ | 1 |
| Cables Dupont | 6 |

---

# 4. Funcionamiento esperado

El sistema debe comportarse de la siguiente manera:

| Posición potenciómetro | Posición servo |
|-----------------------|----------------|
| Mínima | 0° |
| 25% | 45° |
| 50% | 90° |
| 75% | 135° |
| Máxima | 180° |

---

# 5. Análisis del montaje

Según la imagen proporcionada:

## Servomotor

| Cable servo | Conexión |
|------------|-----------|
| Rojo | 5V |
| Negro | GND |
| Naranja | GPIO21 |

### Potenciómetro

| Terminal | Conexión |
|-----------|-----------|
| Extremo izquierdo | 3.3V |
| Terminal central | GPIO14 |
| Extremo derecho | GND |

---

# 6. Advertencia importante sobre la alimentación

> ⚠️ El servomotor debe alimentarse preferiblemente con 5V.

No es recomendable alimentar servos directamente desde el ESP32-S3 cuando:

- El servo trabaja bajo carga.
- El movimiento es continuo.
- Hay varios servos conectados.

Configuración recomendada:

```text
Fuente 5V
     |
     +---- Servo VCC

ESP32 GND
     |
     +---- Servo GND
     |
     +---- Fuente GND
```

Todos los GND deben estar unidos.

---

# 7. Tabla completa de conexiones

## Servo

| Servo | ESP32 |
|---------|---------|
| VCC | 5V |
| GND | GND |
| Signal | GPIO21 |

## Potenciómetro

| Potenciómetro | ESP32 |
|--------------|--------|
| Extremo 1 | 3.3V |
| Centro | GPIO14 |
| Extremo 2 | GND |

---

# 8. Esquema ASCII

```text
                   ESP32-S3

                GPIO21
                   |
                   |
                   +------------- Servo Signal

                GPIO14
                   |
                   |
                   +------------- Potenciómetro centro

                3.3V
                   |
         +---------+---------+
         |                   |
         |             Potenciómetro
         |
         +------------- Extremo 1

                GND
                   |
         +---------+---------+
         |                   |
         |             Potenciómetro
         |
         +------------- Extremo 2
```

---

# 9. ¿Qué es un ADC?

ADC significa:

```text
Analog to Digital Converter
```

o

```text
Conversor Analógico-Digital
```

Permite convertir un voltaje en un número.

---

# 10. ADC en el ESP32-S3

El ADC trabaja normalmente con:

```text
0 V → 0

3.3 V → 4095
```

Por tanto:

| Voltaje | Lectura ADC |
|----------|------------|
| 0V | 0 |
| 1.65V | ≈2048 |
| 3.3V | 4095 |

---

# 11. Funcionamiento del potenciómetro

El potenciómetro actúa como divisor de tensión.

```text
3.3V
  |
 [ POT ]
  |
 GND
```

La salida central proporciona un voltaje variable.

---

# 12. Relación ADC y ángulo

Queremos convertir:

```text
ADC:
0 → 4095
```

en:

```text
Ángulo:
0° → 180°
```

La fórmula utilizada es:

```python
angle = (adcValue * 180) / 4096
```

---

# 13. Ejemplos de conversión

| ADC | Ángulo |
|------|---------|
| 0 | 0° |
| 1024 | 45° |
| 2048 | 90° |
| 3072 | 135° |
| 4095 | 180° |

---

# 14. Código del proyecto

```python
from myServo import myServo
from machine import ADC, Pin
import time

servo = myServo(21)

adc2 = ADC(Pin(14))
adc2.atten(ADC.ATTN_11DB)
adc2.width(ADC.WIDTH_12BIT)

try:

    while True:

        adcValue = adc2.read()

        angle = (adcValue * 180) / 4096

        servo.myServoWriteAngle(int(angle))

        time.sleep_ms(50)

except:

    servo.deinit()
```

---
````
````markdown
# Proyecto 16.2 – Servo Knob
# Parte 2 – Programación Básica y Explicación del Código

## ESP32-S3 WROOM + MicroPython

---

# 15. Introducción a la programación del proyecto

Una vez completado el montaje físico y comprendidos los fundamentos del ADC y los servomotores, podemos comenzar con la programación.

La idea principal es sencilla:

```text
Potenciómetro
      ↓
Lectura ADC
      ↓
Conversión a grados
      ↓
Control PWM
      ↓
Movimiento del servomotor
```

El ESP32-S3 actuará como un traductor entre el potenciómetro y el servomotor.

---

# 16. Flujo general del programa

El funcionamiento completo puede representarse mediante el siguiente diagrama:

```text
INICIO
   ↓
Configurar ADC
   ↓
Configurar Servo
   ↓
Leer ADC
   ↓
Convertir ADC a Ángulo
   ↓
Mover Servo
   ↓
Esperar 50 ms
   ↓
Repetir
```

---

# 17. Librerías utilizadas

El programa utiliza tres librerías.

## Librería del servo

```python
from myServo import myServo
```

Permite simplificar el control del servomotor.

---

## Librería ADC

```python
from machine import ADC, Pin
```

Permite leer el potenciómetro.

---

## Librería Time

```python
import time
```

Se utiliza para introducir retardos.

---

# 18. Código completo del proyecto

```python
from myServo import myServo
from machine import ADC, Pin
import time

servo = myServo(21)

adc2 = ADC(Pin(14))
adc2.atten(ADC.ATTN_11DB)
adc2.width(ADC.WIDTH_12BIT)

try:

    while True:

        adcValue = adc2.read()

        angle = (adcValue * 180) / 4096

        servo.myServoWriteAngle(int(angle))

        time.sleep_ms(50)

except:

    servo.deinit()
```

---

# 19. Análisis línea por línea

## Crear objeto servo

```python
servo = myServo(21)
```

Esta instrucción crea un objeto servo conectado al GPIO 21.

Internamente la librería configura:

```text
PWM
Frecuencia 50 Hz
Control de posición
```

---

## Configurar el ADC

```python
adc2 = ADC(Pin(14))
```

Conecta el conversor analógico-digital al GPIO14.

En nuestro montaje:

```text
Potenciómetro
      ↓
GPIO14
```

---

## Configurar la atenuación

```python
adc2.atten(ADC.ATTN_11DB)
```

Permite medir prácticamente todo el rango de tensión.

Aproximadamente:

```text
0 V → 3.3 V
```

---

## Configurar resolución

```python
adc2.width(ADC.WIDTH_12BIT)
```

Configura una resolución de:

```text
12 bits
```

equivalente a:

```text
0 → 4095
```

---

# 20. Bucle principal

```python
while True:
```

El programa se ejecutará continuamente.

---

# 21. Lectura del potenciómetro

```python
adcValue = adc2.read()
```

Ejemplos:

| Posición | ADC |
|-----------|------|
| Izquierda | 0 |
| Centro | 2048 |
| Derecha | 4095 |

---

# 22. Conversión ADC → Ángulo

La fórmula utilizada es:

```python
angle = (adcValue * 180) / 4096
```

---

## Ejemplos

### Potenciómetro mínimo

```text
ADC = 0

Ángulo = 0°
```

---

### Potenciómetro al centro

```text
ADC = 2048

Ángulo = 90°
```

---

### Potenciómetro máximo

```text
ADC = 4095

Ángulo ≈ 180°
```

---

# 23. Tabla completa de conversión

| ADC | Ángulo |
|------|---------|
| 0 | 0° |
| 512 | 22° |
| 1024 | 45° |
| 1536 | 67° |
| 2048 | 90° |
| 2560 | 112° |
| 3072 | 135° |
| 3584 | 157° |
| 4095 | 180° |

---

# 24. Envío del ángulo al servo

```python
servo.myServoWriteAngle(int(angle))
```

Esta función:

1. Recibe el ángulo.
2. Calcula el PWM necesario.
3. Genera la señal.
4. Mueve el servo.

---

# 25. Conversión interna a PWM

Internamente la librería realiza una operación similar a:

```python
pulse = 500 + (angle * 2000 / 180)
```

---

## Ejemplo

### 0°

```text
500 µs
```

### 90°

```text
1500 µs
```

### 180°

```text
2500 µs
```

---

# 26. Retardo de estabilización

```python
time.sleep_ms(50)
```

Permite:

- Evitar movimientos bruscos.
- Reducir consumo CPU.
- Dar tiempo al servo para moverse.

---

# 27. ¿Por qué 50 ms?

Porque:

```text
20 lecturas por segundo
```

es más que suficiente para un control suave.

---

# 28. Versión con monitor serie

Una mejora interesante consiste en visualizar información.

```python
print(
    "ADC:",
    adcValue,
    " ANGULO:",
    int(angle)
)
```

Salida:

```text
ADC: 1024 ANGULO: 45
ADC: 2048 ANGULO: 90
ADC: 3072 ANGULO: 135
```

---

# 29. Código completo con monitor serie

```python
from myServo import myServo
from machine import ADC, Pin
import time

servo = myServo(21)

adc2 = ADC(Pin(14))
adc2.atten(ADC.ATTN_11DB)
adc2.width(ADC.WIDTH_12BIT)

while True:

    adcValue = adc2.read()

    angle = (adcValue * 180) / 4096

    print(
        "ADC:",
        adcValue,
        " ANGULO:",
        int(angle)
    )

    servo.myServoWriteAngle(int(angle))

    time.sleep_ms(50)
```

---

# 30. Mejora: Zona Muerta

Algunos potenciómetros generan ruido.

Podemos ignorar pequeños cambios.

```python
if abs(angle - lastAngle) > 2:

    servo.myServoWriteAngle(int(angle))
```

---

# 31. Mejora: Filtrado de Lecturas

Promediar varias lecturas.

```python
suma = 0

for i in range(10):

    suma += adc2.read()

adcValue = suma / 10
```

Resultado:

```text
Movimiento más estable
```

---

# 32. Mejora: Movimiento Suavizado

En lugar de saltar directamente:

```text
40° → 120°
```

podemos mover gradualmente:

```text
40°
41°
42°
43°
...
120°
```

---

# 33. Ejercicio práctico 1

Modificar el programa para que:

```text
0° → LED apagado

180° → LED encendido
```

utilizando simultáneamente un LED y un servo.

---

# 34. Ejercicio práctico 2

Mostrar en el terminal:

```text
ADC
Ángulo
Porcentaje
```

Ejemplo:

```text
ADC: 3072

Ángulo: 135°

Potencia: 75%
```

---

# 35. Ejercicio práctico 3

Limitar el recorrido:

```text
30° → 150°
```

en lugar de:

```text
0° → 180°
```

---

# 36. Conceptos aprendidos en esta parte

Al finalizar esta sección el alumno debe comprender:

✅ ADC

✅ Potenciómetros

✅ Conversión ADC → Ángulo

✅ Control básico de servos

✅ PWM aplicado a posicionamiento

✅ Filtrado de señales

✅ Monitor serie

✅ Estructura de programas MicroPython

---

# Fin de la Parte 2

En la Parte 3 desarrollaremos:

- Servo profesional con duty_u16()
- Servo tipo radar
- Servo tipo barrera
- Servo tipo brazo robótico
- Control de velocidad
- Movimiento suave avanzado
- Librería propia para servomotores
````
````markdown
# Proyecto 16.2 – Servo Knob
# Parte 3 – Técnicas Avanzadas y Aplicaciones Profesionales

## ESP32-S3 WROOM + MicroPython

---

# 37. Introducción

En la Parte 2 hemos conseguido controlar un servomotor utilizando un potenciómetro.

El sistema ya funciona correctamente:

```text
Potenciómetro
      ↓
ADC
      ↓
Ángulo
      ↓
Servo
```

Sin embargo, todavía podemos mejorar considerablemente:

- Mayor precisión.
- Movimientos más suaves.
- Eliminación de vibraciones.
- Mejor respuesta.
- Aplicaciones robóticas reales.

En esta parte aprenderemos técnicas profesionales utilizadas en robótica y automatización.

---

# 38. Limitaciones de la versión básica

El código desarrollado hasta ahora presenta algunas limitaciones.

## Problema 1: Saltos bruscos

Si el potenciómetro cambia rápidamente:

```text
30°
↓
120°
```

el servo intenta llegar inmediatamente.

Esto provoca:

- Tirones.
- Vibraciones.
- Desgaste mecánico.

---

## Problema 2: Ruido ADC

Las lecturas analógicas nunca son perfectas.

Por ejemplo:

```text
2047
2049
2048
2051
2046
```

Aunque el potenciómetro no se mueva.

Esto provoca pequeñas oscilaciones del servo.

---

## Problema 3: Resolución limitada

La función clásica:

```python
servo.duty()
```

utiliza poca resolución.

En ESP32-S3 es preferible:

```python
servo.duty_u16()
```

---

# 39. PWM Profesional con duty_u16()

Las versiones modernas de MicroPython incorporan:

```python
PWM.duty_u16()
```

Rango:

```text
0 → 65535
```

Mucho más preciso que:

```text
0 → 1023
```

---

# 40. Conversión profesional de ángulo

## Cálculo del pulso

Un servo estándar utiliza:

| Ángulo | Pulso |
|----------|----------|
| 0° | 500 µs |
| 90° | 1500 µs |
| 180° | 2500 µs |

---

## Fórmula

```python
pulse = 500 + angle * 2000 / 180
```

---

## Conversión a duty_u16

Periodo PWM:

```text
20 ms
```

equivale a:

```text
20000 µs
```

---

Fórmula:

```python
duty = int((pulse / 20000) * 65535)
```

---

# 41. Función profesional de movimiento

```python
def moveServo(angle):

    pulse = 500 + (angle * 2000 / 180)

    duty = int(
        (pulse / 20000) * 65535
    )

    servo.duty_u16(duty)
```

---

# 42. Código profesional completo

```python
from machine import Pin, PWM, ADC
import time

servo = PWM(Pin(21))
servo.freq(50)

adc = ADC(Pin(14))

while True:

    value = adc.read()

    angle = value * 180 / 4095

    pulse = 500 + angle * 2000 / 180

    duty = int(
        (pulse / 20000) * 65535
    )

    servo.duty_u16(duty)

    time.sleep_ms(50)
```

---

# 43. Filtrado de ruido ADC

Una técnica habitual consiste en promediar varias muestras.

---

## Método de media

```python
suma = 0

for i in range(10):

    suma += adc.read()

valor = suma / 10
```

---

## Ventajas

```text
Lectura más estable

Menos vibraciones

Mayor precisión
```

---

# 44. Función de filtrado

```python
def readADC():

    total = 0

    for i in range(10):

        total += adc.read()

    return total / 10
```

---

# 45. Suavizado de movimiento

Otra técnica muy utilizada consiste en evitar cambios bruscos.

---

## Sin suavizado

```text
20°
↓
140°
```

---

## Con suavizado

```text
20°
21°
22°
23°
...
140°
```

---

# 46. Función SmoothMove

```python
def smoothMove(target):

    global currentAngle

    if target > currentAngle:

        step = 1

    else:

        step = -1

    for angle in range(
        int(currentAngle),
        int(target),
        step
    ):

        moveServo(angle)

        time.sleep_ms(10)

    currentAngle = target
```

---

# 47. Servo tipo Radar

Aplicación típica:

```text
Sensores ultrasónicos
```

Movimiento:

```text
0°
↓
180°
↓
0°
```

---

## Código Radar

```python
while True:

    for angle in range(0,181):

        moveServo(angle)

        time.sleep_ms(10)

    for angle in range(180,-1,-1):

        moveServo(angle)

        time.sleep_ms(10)
```

---

# 48. Servo tipo Barrera

Simulación de una barrera automática.

---

## Abrir

```text
0° → 90°
```

---

## Cerrar

```text
90° → 0°
```

---

## Código

```python
moveServo(90)

time.sleep(3)

moveServo(0)
```

---

# 49. Servo tipo Puerta Automática

Similar a una puerta de garaje.

---

## Estados

```text
Cerrada
↓
Abriendo
↓
Abierta
↓
Cerrando
```

---

# 50. Servo tipo Brazo Robótico

Un servo puede actuar como articulación.

Ejemplo:

```text
Base
Codo
Muñeca
Pinza
```

Cada articulación utiliza un servo.

---

# 51. Servo tipo Seguidor Solar

Aplicación muy utilizada.

El servo orienta:

```text
Panel solar
```

hacia la posición del Sol.

---

# 52. Servo controlado por porcentaje

En lugar de usar grados:

```text
0%
↓
100%
```

---

## Conversión

```python
angle = porcentaje * 180 / 100
```

---

# 53. Servo controlado por joystick

Proyecto futuro:

```text
Joystick
      ↓
ADC
      ↓
Servo
```

---

# 54. Servo controlado por web

Aplicación IoT.

```text
Página Web
      ↓
WiFi
      ↓
ESP32
      ↓
Servo
```

---

# 55. Servo controlado por MQTT

Aplicación industrial.

```text
Broker MQTT
       ↓
ESP32
       ↓
Servo
```

---

# 56. Diagnóstico avanzado

## El servo vibra

Posibles causas:

- Ruido ADC.
- Alimentación insuficiente.
- Cableado incorrecto.

---

## El servo se mueve solo

Posibles causas:

- Potenciómetro defectuoso.
- Falta filtrado.

---

## El servo no llega a 180°

Posibles causas:

- Servo limitado.
- PWM incorrecto.

---

# 57. Optimización de rendimiento

Buenas prácticas:

- Filtrar ADC.
- Usar duty_u16().
- Utilizar movimientos suaves.
- Evitar bucles excesivamente rápidos.

---

# 58. Mini proyecto avanzado

Construir un sistema de puntería:

```text
Potenciómetro
      ↓
Servo
      ↓
Láser
```

---

# 59. Conceptos aprendidos

Al finalizar esta parte el alumno debe dominar:

✅ duty_u16()

✅ Conversión precisa PWM

✅ Filtrado ADC

✅ Suavizado de movimiento

✅ Servo Radar

✅ Servo Barrera

✅ Servo IoT

✅ Aplicaciones industriales

---

# 60. Preparación para la Parte 4

En la siguiente parte veremos:

- Aplicaciones industriales reales.
- Casos de uso profesionales.
- Errores frecuentes.
- Resolución de problemas.
- Actividades para alumnado.
- Preguntas de examen.
- Respuestas.
- Rúbrica de evaluación.
- Prompt profesional para GitHub Copilot.

---

# Fin de la Parte 3
````
# Proyecto 16.2 – Servo Knob
# Parte 4 – Aplicaciones Profesionales, Evaluación y Recursos Didácticos

## ESP32-S3 WROOM + MicroPython

---

# 61. Introducción

En las partes anteriores hemos aprendido:

- Qué es un servomotor.
- Cómo funciona internamente.
- Cómo controlar un servo mediante PWM.
- Cómo utilizar un potenciómetro como dispositivo de entrada.
- Cómo convertir una lectura ADC en una posición angular.
- Cómo realizar movimientos suaves y precisos.

En esta última parte veremos cómo se utilizan estos conceptos en sistemas reales y cómo evaluar correctamente el proyecto en un entorno educativo.

---

# 62. Aplicaciones Industriales Reales

Los servomotores están presentes en prácticamente todos los sectores industriales.

## Automatización Industrial

Se utilizan para:

- Posicionar piezas.
- Clasificar productos.
- Abrir compuertas.
- Ajustar sensores.
- Manipular objetos.

Ejemplo:

```text
Cinta transportadora
        ↓
Sensor detecta pieza
        ↓
Servo gira 90°
        ↓
Desvía la pieza
```

---

## Robótica Industrial

Aplicaciones:

- Robots pick & place.
- Robots cartesianos.
- Robots SCARA.
- Robots colaborativos.

Ejemplo:

```text
Servo 1 → Base

Servo 2 → Brazo

Servo 3 → Antebrazo

Servo 4 → Pinza
```

---

## Automoción

Los servos aparecen en:

- Sistemas HVAC.
- Regulación de faros.
- Apertura de trampillas.
- Retrovisores automáticos.

---

## Aeronáutica

Aplicaciones:

- Alerones.
- Timones.
- Flaps.
- Trenes de aterrizaje.

---

## Domótica

Los servomotores permiten automatizar:

- Persianas.
- Ventanas.
- Cerraduras.
- Puertas automáticas.

---

# 63. Aplicaciones IoT

Una de las grandes ventajas del ESP32-S3 es la conectividad.

Podemos controlar un servo mediante:

## WiFi

```text
Página Web
      ↓
ESP32
      ↓
Servo
```

---

## MQTT

```text
Broker MQTT
       ↓
ESP32
       ↓
Servo
```

---

## Bluetooth

```text
Teléfono móvil
        ↓
Bluetooth
        ↓
ESP32
        ↓
Servo
```

---

# 64. Aplicaciones en Robótica Educativa

Algunas ideas para ampliar el proyecto:

### Brazo robótico

Controlar varias articulaciones.

---

### Radar ultrasónico

```text
Servo
     ↓
Sensor HC-SR04
     ↓
Escaneo 180°
```

---

### Cámara Pan-Tilt

```text
Servo Horizontal

Servo Vertical
```

---

### Seguidor solar

El servo orienta un panel solar.

---

# 65. Proyecto Integrador

## Estación Clasificadora

Aplicación relacionada con proyectos industriales.

```text
Sensor
   ↓
ESP32
   ↓
Servo
   ↓
Desviador
```

Dependiendo del tamaño detectado:

- Caja A
- Caja B
- Caja C

---

# 66. Errores Frecuentes

## El servo no se mueve

Posibles causas:

- GPIO incorrecto.
- PWM mal configurado.
- Servo averiado.

---

## El servo vibra constantemente

Posibles causas:

- ADC inestable.
- Ruido eléctrico.
- Fuente insuficiente.

---

## El servo gira poco

Posibles causas:

- Duty incorrecto.
- Servo limitado mecánicamente.

---

## El servo se calienta

Posibles causas:

- Movimiento bloqueado.
- Exceso de carga.

---

## El ESP32 se reinicia

Posibles causas:

- Servo alimentado desde USB.
- Consumo excesivo.

---

# 67. Procedimiento de Diagnóstico

## Paso 1

Comprobar alimentación.

```text
5V presentes
```

---

## Paso 2

Comprobar masa común.

```text
GND Servo

GND ESP32

GND Fuente
```

---

## Paso 3

Comprobar PWM.

---

## Paso 4

Probar servo con código básico.

---

## Paso 5

Verificar ADC.

---

# 68. Optimización del Proyecto

Buenas prácticas:

- Utilizar fuente externa.
- Filtrar lecturas ADC.
- Aplicar suavizado.
- Evitar movimientos bruscos.
- Utilizar duty_u16().

---

# 69. Actividades para el Alumnado

## Nivel Básico

Mover el servo entre:

```text
0°
90°
180°
```

---

## Nivel Medio

Controlar el servo mediante potenciómetro.

---

## Nivel Avanzado

Mostrar:

- ADC.
- Ángulo.
- Porcentaje.

por monitor serie.

---

## Nivel Experto

Controlar un servo mediante un joystick.

---

# 70. Actividad de Investigación

Buscar información sobre:

- Servos digitales.
- Servos analógicos.
- Servos industriales.
- Servos brushless.

Elaborar un informe comparativo.

---

# 71. Actividad de Programación

Modificar el código para que:

```text
0° → LED apagado

180° → LED encendido
```

---

# 72. Actividad de Integración

Combinar:

- Potenciómetro.
- Servo.
- LED RGB.

El color debe variar según el ángulo.

---

# 73. Preguntas Tipo Examen

## Pregunta 1

¿Qué es un servomotor?

---

## Pregunta 2

¿Qué diferencia existe entre un servo y un motor DC?

---

## Pregunta 3

¿Qué frecuencia PWM utilizan habitualmente los servos?

---

## Pregunta 4

¿Qué rango de valores devuelve un ADC de 12 bits?

---

## Pregunta 5

¿Qué función realiza el potenciómetro?

---

## Pregunta 6

¿Qué hace duty_u16()?

---

## Pregunta 7

¿Por qué es importante compartir GND?

---

## Pregunta 8

¿Qué ventajas tiene utilizar una fuente externa?

---

## Pregunta 9

¿Qué aplicaciones tienen los servos en robótica?

---

## Pregunta 10

¿Qué es un sistema de control en lazo cerrado?

---

# 74. Respuestas Correctas

## Respuesta 1

Actuador capaz de posicionarse en un ángulo concreto.

---

## Respuesta 2

El motor DC gira continuamente; el servo controla posición.

---

## Respuesta 3

50 Hz.

---

## Respuesta 4

0 a 4095.

---

## Respuesta 5

Generar un voltaje variable.

---

## Respuesta 6

Generar PWM de alta resolución.

---

## Respuesta 7

Permite compartir la referencia eléctrica.

---

## Respuesta 8

Aporta corriente suficiente.

---

## Respuesta 9

Robots, brazos, drones, cámaras, automatización.

---

## Respuesta 10

Sistema que compara posición deseada y posición real.

---

# 75. Rúbrica de Evaluación

| Criterio | Excelente | Bien | Mejorable |
|-----------|-----------|------|-----------|
| Cableado | Correcto y ordenado | Correcto | Presenta errores |
| Configuración ADC | Funciona perfectamente | Funciona | Errores |
| Control Servo | Preciso y estable | Correcto | Inestable |
| Código | Comentado y estructurado | Funcional | Poco organizado |
| Comprensión Teórica | Excelente | Adecuada | Insuficiente |

---

# 76. Proyecto de Ampliación

## Servo + MQTT

Objetivo:

Controlar el servo desde Node-RED.

Arquitectura:

```text
Node-RED
     ↓
MQTT
     ↓
ESP32-S3
     ↓
Servo
```

---

## Servo + Web

Crear una interfaz web con:

- Botón izquierda.
- Botón centro.
- Botón derecha.

---

## Servo + Joystick

Control proporcional.

---

# 77. Prompt Profesional para GitHub Copilot

A parir de las especificación del archivo .md de este proyecto genera un archivo `main.py` para ESP32-S3 WROOM utilizando MicroPython.

Conexiones:

- Potenciómetro en GPIO14.
- Servomotor en GPIO21.

Requisitos:

- Configurar ADC de 12 bits.
- Leer continuamente el potenciómetro.
- Convertir el valor ADC a un ángulo entre 0° y 180°.
- Controlar el servo mediante PWM.
- Mostrar ADC y ángulo por monitor serie.
- Añadir filtrado de lecturas.
- Implementar movimiento suave.
- Utilizar duty_u16().
- Comentar todas las funciones.

---

# 78. Conclusiones

Este proyecto ha permitido integrar dos conceptos fundamentales de los sistemas embebidos:

## Entrada Analógica

```text
Potenciómetro
```

---

## Salida PWM

```text
Servomotor
```

La combinación de ambos permite crear sistemas de control proporcional utilizados en:

- Robótica.
- Automatización industrial.
- Domótica.
- IoT.
- Mecatrónica.

Además, constituye una excelente base para proyectos más avanzados que involucren varios servos, sensores y comunicaciones inalámbricas.

---

# Fin del Proyecto 16.2 – Servo Knob

Manual completo dividido en 4 partes.