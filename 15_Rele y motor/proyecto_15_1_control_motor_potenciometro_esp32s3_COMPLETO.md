# Proyecto 15.1 – Control de Motor con Potenciómetro
## ESP32-S3 WROOM + MicroPython

---

# 1. Objetivo del proyecto

En este proyecto aprenderemos a controlar la velocidad y el sentido de giro de un motor de corriente continua (DC) utilizando:

- ESP32-S3 WROOM
- Potenciómetro de 10 kΩ
- Driver L293D
- Motor DC con hélice
- Batería externa de 9 V

El usuario podrá girar el potenciómetro para:

- Aumentar o disminuir la velocidad del motor.
- Cambiar automáticamente el sentido de giro al pasar por la posición central.

Este proyecto combina:

- ADC (lectura analógica)
- PWM (control de velocidad)
- Driver de potencia L293D
- Control bidireccional de motores

---

# 2. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| L293D | 1 |
| Potenciómetro 10 kΩ | 1 |
| Motor DC + hélice | 1 |
| Batería 9 V | 1 |
| Conector batería 9 V | 1 |
| Cables Dupont | Varios |

---

# 3. Advertencia importante

⚠️ **Nunca alimentes el motor directamente desde el ESP32-S3.**

Los motores consumen mucha más corriente que la que puede suministrar un GPIO.

Por este motivo utilizamos:

- L293D como etapa de potencia.
- Batería externa de 9 V.

Además:

```text
La tierra (GND) de la batería y del ESP32-S3 deben estar unidas.
```

Si no comparten GND el circuito no funcionará correctamente.

---

# 4. Objetivos de aprendizaje

Al finalizar esta práctica el alumno será capaz de:

1. Comprender el funcionamiento del L293D.
2. Controlar motores DC.
3. Leer un potenciómetro mediante ADC.
4. Generar señales PWM.
5. Variar la velocidad de un motor.
6. Cambiar el sentido de giro.
7. Utilizar alimentación externa de potencia.

---

# 5. ¿Qué es el L293D?

El L293D es un controlador de motores.

Permite:

- Controlar motores DC.
- Cambiar el sentido de giro.
- Regular velocidad mediante PWM.
- Aislar el ESP32-S3 de las corrientes elevadas.

Internamente incorpora dos puentes H.

---

# 6. ¿Qué es un puente H?

Un puente H permite:

```text
Motor hacia delante

Motor hacia atrás

Motor parado
```

Simplemente cambiando las señales digitales de control.

---

# 7. Conexiones según el montaje

## Potenciómetro

| Terminal | Conexión |
|-----------|----------|
| Extremo 1 | 3.3 V |
| Central | GPIO 1 |
| Extremo 2 | GND |

---

## Control del L293D

| ESP32-S3 | L293D |
|-----------|--------|
| GPIO12 | EN1 |
| GPIO13 | IN1 |
| GPIO14 | IN2 |

---

## Motor

| L293D | Motor |
|--------|--------|
| OUT1 | Terminal motor |
| OUT2 | Terminal motor |

---

## Alimentación

| Elemento | Conexión |
|-----------|----------|
| Batería 9V (+) | Vmotor L293D |
| Batería 9V (-) | GND común |
| ESP32 GND | GND común |
| ESP32 3.3V | VCC lógica L293D |

---

# 8. Esquema ASCII

```text
                ESP32-S3

          GPIO13 ---------- IN1

          GPIO14 ---------- IN2

          GPIO12 ---------- EN1(PWM)

          GPIO1  <--------- Potenciómetro

                           L293D

               IN1 ----+
                       |
                       |
               IN2 ----+---- Motor DC
                       |
                       |
               EN1 ----+ PWM


           Batería 9V ---- Alimentación motor
```

---

# 9. Funcionamiento esperado

La posición del potenciómetro determina:

## Centro

```text
Motor parado
```

## Giro a la derecha

```text
Motor adelante

Velocidad creciente
```

## Giro a la izquierda

```text
Motor atrás

Velocidad creciente
```

---

# 10. ADC del ESP32-S3

El ADC devuelve valores entre:

```text
0 y 4095
```

Valor central:

```text
2048
```

---

# 11. PWM para controlar velocidad

El PWM modifica la velocidad media del motor.

```python
pwm.duty(spd)
```

Mayor duty:

```text
Más velocidad
```

Menor duty:

```text
Menos velocidad
```

---

# 12. Código de referencia del proyecto

```python
from machine import ADC, Pin, PWM
import time
import math

in1Pin = Pin(13, Pin.OUT)
in2Pin = Pin(14, Pin.OUT)

enablePin = Pin(12, Pin.OUT)

pwm = PWM(enablePin, 10000)

adc = ADC(Pin(1))

while True:

    potenVal = adc.read()

    if potenVal > 2048:
        rotationDir = 1
    else:
        rotationDir = 0

    rotationSpeed = int(abs((potenVal - 2047) / 2))

    if rotationDir:

        in1Pin.value(1)
        in2Pin.value(0)

    else:

        in1Pin.value(0)
        in2Pin.value(1)

    pwm.duty(rotationSpeed)

    time.sleep_ms(10)
```

---

# 13. Explicación del código

## Configuración de pines

```python
in1Pin = Pin(13, Pin.OUT)
in2Pin = Pin(14, Pin.OUT)
```

Controlan el sentido de giro.

---

## Pin PWM

```python
enablePin = Pin(12, Pin.OUT)
pwm = PWM(enablePin, 10000)
```

Controla la velocidad.

Frecuencia:

```text
10 kHz
```

---

## Lectura del potenciómetro

```python
potenVal = adc.read()
```

Obtiene valores entre:

```text
0 → 4095
```

---

## Determinar dirección

```python
if potenVal > 2048:
```

Mitad superior:

```text
Motor adelante
```

Mitad inferior:

```text
Motor atrás
```

---

## Determinar velocidad

```python
rotationSpeed = int(abs((potenVal - 2047)/2))
```

Cuanto más lejos del centro:

```text
Mayor velocidad
```

---

# 14. Versión con monitor serie

```python
print(
    "ADC:", potenVal,
    "Velocidad:", rotationSpeed,
    "Direccion:", rotationDir
)
```

Ejemplo:

```text
ADC: 3400 Velocidad: 676 Direccion: 1
```

---

# 15. Versión mejorada con zona muerta

Evita vibraciones cerca del centro.

```python
if abs(potenVal - 2048) < 100:

    pwm.duty(0)

else:

    pwm.duty(rotationSpeed)
```

---

# 16. Aplicaciones reales

- Robots móviles.
- Vehículos autónomos.
- Cintas transportadoras.
- Ventiladores inteligentes.
- Sistemas domóticos.
- Automatización industrial.

---

# 17. Errores frecuentes

## El motor no gira

Posibles causas:

- Batería descargada.
- GND no compartido.
- Motor mal conectado.

---

## El motor gira siempre igual

Posibles causas:

- IN1 e IN2 invertidos.
- Error en el código.

---

## El motor vibra

Posibles causas:

- Potenciómetro en posición central.
- Falta zona muerta.

---

## El ESP32 se reinicia

Posibles causas:

- Motor alimentado desde el ESP32.
- Consumo excesivo.

---

# 18. Retos para el alumnado

## Nivel básico

Controlar velocidad.

---

## Nivel medio

Controlar velocidad y sentido.

---

## Nivel avanzado

Mostrar velocidad en porcentaje.

---

## Nivel experto

Controlar el motor con un joystick.

---

# 19. Preguntas para el alumnado

1. ¿Para qué sirve el L293D?
2. ¿Qué es un puente H?
3. ¿Por qué no debemos alimentar el motor desde el ESP32?
4. ¿Qué hace PWM?
5. ¿Qué hace el ADC?
6. ¿Qué representa el valor 2048?
7. ¿Por qué necesitamos una batería externa?
8. ¿Qué ocurre si no compartimos GND?

---

# 20. Criterios de evaluación

| Criterio | Logrado | No logrado |
|-----------|----------|------------|
| Cablea correctamente el L293D | | |
| Configura ADC correctamente | | |
| Configura PWM correctamente | | |
| Controla velocidad | | |
| Controla dirección | | |
| Utiliza alimentación externa | | |
| Código comentado | | |

---

# 21. Prompt optimizado para GitHub Copilot / Cursor

Genera un archivo main.py para ESP32-S3 WROOM utilizando MicroPython.

Conexiones:

- Potenciómetro → GPIO1.
- EN1 del L293D → GPIO12.
- IN1 del L293D → GPIO13.
- IN2 del L293D → GPIO14.
- Motor DC controlado mediante L293D.
- Alimentación externa de 9 V.

Requisitos:

- Leer continuamente el potenciómetro.
- Determinar velocidad y dirección.
- Controlar el motor mediante PWM.
- Implementar una zona muerta alrededor del centro.
- Mostrar datos por monitor serie.
- Incluir comentarios explicativos.

---

# 22. Resultado esperado

Al girar el potenciómetro:

- El motor aumenta o disminuye velocidad.
- Cambia automáticamente de sentido al pasar por el centro.
- Se comporta como una palanca de control proporcional.

Este proyecto introduce los conceptos fundamentales de control de motores DC utilizando MicroPython y ESP32-S3.
