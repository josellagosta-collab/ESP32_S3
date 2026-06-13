# Proyecto 18.1 – Medición de Distancias por Ultrasonidos
## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# Índice

1. Introducción
2. Objetivos
3. Componentes necesarios
4. ¿Qué es el HC-SR04?
5. Principio de funcionamiento
6. El ultrasonido
7. Tiempo de vuelo
8. Conexiones del proyecto
9. Tabla completa de conexiones
10. Esquema ASCII
11. Funcionamiento del Trigger y Echo
12. Cálculo de la distancia
13. Código completo
14. Explicación línea por línea
15. Análisis matemático
16. Resultado esperado
17. Mejoras del proyecto
18. Aplicaciones reales
19. Errores frecuentes
20. Actividades para alumnado
21. Preguntas tipo examen
22. Rúbrica de evaluación
23. Prompt para GitHub Copilot

---

# 1. Introducción

En este proyecto aprenderemos a utilizar uno de los sensores más populares en robótica y sistemas embebidos:

```text
HC-SR04
```

Este sensor permite medir distancias sin contacto utilizando ondas ultrasónicas.

Es muy utilizado en:

- Robots móviles.
- Sistemas anticolisión.
- Aparcamientos inteligentes.
- Drones.
- Automatización industrial.
- Medición de nivel de depósitos.

---

# 2. Objetivos del proyecto

Al finalizar esta práctica el alumno será capaz de:

- Comprender qué es un sensor ultrasónico.
- Entender el concepto de tiempo de vuelo.
- Medir distancias mediante ultrasonidos.
- Utilizar entradas y salidas digitales.
- Calcular distancias mediante fórmulas físicas.
- Mostrar resultados por terminal serie.

---

# 3. Componentes necesarios

| Componente | Cantidad |
|------------|-----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| Sensor HC-SR04 | 1 |
| Cable Dupont hembra-macho | 4 |

---

# 4. ¿Qué es el HC-SR04?

El HC-SR04 es un sensor ultrasónico capaz de medir distancias.

Rango típico:

```text
2 cm → 400 cm
```

Precisión:

```text
±3 mm
```

Ángulo aproximado:

```text
15°
```

---

# 5. Partes del HC-SR04

El sensor está formado por:

### Emisor ultrasónico

```text
Transmite ultrasonidos
```

---

### Receptor ultrasónico

```text
Recibe el eco
```

---

### Electrónica de control

```text
Calcula el tiempo
```

---

# 6. ¿Qué es un ultrasonido?

Los ultrasonidos son ondas sonoras de frecuencia superior a:

```text
20 kHz
```

El oído humano no puede escucharlas.

El HC-SR04 trabaja aproximadamente a:

```text
40 kHz
```

---

# 7. Principio de funcionamiento

El sensor realiza el siguiente proceso:

```text
Emitir ultrasonido
          ↓
Rebota en un objeto
          ↓
Regresa al sensor
          ↓
Medir tiempo empleado
          ↓
Calcular distancia
```

---

# 8. Concepto de Tiempo de Vuelo

El método utilizado se denomina:

```text
Time Of Flight (TOF)
```

o

```text
Tiempo de vuelo
```

---

# 9. Ejemplo de funcionamiento

Supongamos:

```text
Objeto a 50 cm
```

El sonido recorrerá:

```text
50 cm ida
+
50 cm vuelta

=
100 cm
```

---

# 10. Velocidad del sonido

A temperatura ambiente:

```text
340 m/s
```

equivalente a:

```text
34000 cm/s
```

---

# 11. Pines del HC-SR04

| Pin | Función |
|-------|----------|
| VCC | Alimentación |
| TRIG | Disparo |
| ECHO | Recepción |
| GND | Tierra |

---

# 12. Conexiones según el montaje

Observando el esquema:

| HC-SR04 | ESP32-S3 |
|----------|-----------|
| VCC | 3.3V |
| GND | GND |
| TRIG | GPIO13 |
| ECHO | GPIO14 |

---

# 13. Tabla detallada de conexiones

| Sensor | Función | ESP32 |
|---------|----------|--------|
| VCC | Alimentación | 3.3V |
| GND | Tierra | GND |
| TRIG | Salida | GPIO13 |
| ECHO | Entrada | GPIO14 |

---

# 14. Esquema ASCII

```text
             ESP32-S3

             GPIO13
                |
                |
                +------ TRIG

             GPIO14
                |
                |
                +------ ECHO

              3.3V
                |
                |
                +------ VCC

               GND
                |
                |
                +------ GND


              HC-SR04
```

---

# 15. ¿Qué hace el pin TRIG?

El ESP32 envía un pulso de:

```text
10 microsegundos
```

para iniciar la medición.

---

# 16. ¿Qué hace el pin ECHO?

El HC-SR04 genera un pulso cuya duración depende de la distancia medida.

Cuanto mayor sea la distancia:

```text
Mayor duración del pulso
```

---

# 17. Código completo del proyecto

```python
from machine import Pin
import time

trigPin = Pin(13, Pin.OUT, 0)
echoPin = Pin(14, Pin.IN, 0)

soundVelocity = 340
distance = 0

def getSonar():

    trigPin.value(1)

    time.sleep_us(10)

    trigPin.value(0)

    while not echoPin.value():
        pass

    pingStart = time.ticks_us()

    while echoPin.value():
        pass

    pingStop = time.ticks_us()

    pingTime = time.ticks_diff(
        pingStop,
        pingStart
    )

    distance = (
        pingTime *
        soundVelocity //
        2 //
        10000
    )

    return int(distance)

time.sleep_ms(2000)

while True:

    time.sleep_ms(500)

    print(
        "Distance:",
        getSonar(),
        "cm"
    )
```

---

# 18. Explicación línea por línea

## Configuración del Trigger

```python
trigPin = Pin(
    13,
    Pin.OUT,
    0
)
```

GPIO13 configurado como salida.

---

## Configuración del Echo

```python
echoPin = Pin(
    14,
    Pin.IN,
    0
)
```

GPIO14 configurado como entrada.

---

## Velocidad del sonido

```python
soundVelocity = 340
```

metros por segundo.

---

# 19. Función getSonar()

Esta función realiza una medición completa.

---

## Generar pulso Trigger

```python
trigPin.value(1)

time.sleep_us(10)

trigPin.value(0)
```

Pulso de:

```text
10 µs
```

---

## Esperar inicio del eco

```python
while not echoPin.value():
    pass
```

---

## Registrar instante inicial

```python
pingStart =
time.ticks_us()
```

---

## Esperar fin del eco

```python
while echoPin.value():
    pass
```

---

## Registrar instante final

```python
pingStop =
time.ticks_us()
```

---

# 20. Calcular tiempo

```python
pingTime =
time.ticks_diff(
    pingStop,
    pingStart
)
```

---

# 21. Calcular distancia

Fórmula:

```python
distance =
(
 pingTime *
 soundVelocity
 //
 2
 //
 10000
)
```

---

# 22. Explicación matemática

Sabemos que:

```text
Distancia =
Velocidad × Tiempo
```

Pero el sonido realiza:

```text
IDA + VUELTA
```

Por tanto:

```text
Distancia =
(Velocidad × Tiempo)
/ 2
```

---

# 23. Ejemplo práctico

Supongamos:

```text
Tiempo = 3000 µs
```

Resultado:

```text
≈ 51 cm
```

---

# 24. Resultado esperado

Terminal:

```text
Distance: 23 cm

Distance: 24 cm

Distance: 23 cm

Distance: 25 cm
```

---

# 25. Frecuencia de actualización

Actualmente:

```python
time.sleep_ms(500)
```

Actualización:

```text
2 veces por segundo
```

---

# 26. Mejoras posibles

Mostrar:

- Distancia mínima.
- Distancia máxima.
- Distancia media.

---

# 27. Mostrar distancia en LCD1602

Proyecto combinado:

```text
HC-SR04
      ↓
ESP32
      ↓
LCD1602
```

---

# 28. Mostrar distancia mediante MQTT

```text
HC-SR04
      ↓
ESP32
      ↓
MQTT
      ↓
Node-RED
```

---

# 29. Aplicaciones reales

## Robot evita obstáculos

```text
Si distancia < 20 cm

→ Girar
```

---

## Aparcamiento inteligente

Medición automática de plazas.

---

## Medición de depósitos

Nivel de agua.

---

## Automatización industrial

Detección de presencia.

---

# 30. Errores frecuentes

## Siempre mide 0 cm

Posibles causas:

- Echo mal conectado.
- Trigger incorrecto.

---

## Valores erráticos

Posibles causas:

- Obstáculos irregulares.
- Interferencias.

---

## No mide objetos blandos

La espuma y tejidos absorben ultrasonidos.

---

# 31. Actividades para alumnado

## Nivel básico

Medir distancia.

---

## Nivel medio

Activar LED cuando:

```text
Distancia < 20 cm
```

---

## Nivel avanzado

Mostrar distancia en LCD1602.

---

## Nivel experto

Crear radar ultrasónico usando servomotor.

---

# 32. Preguntas tipo examen

1. ¿Qué significa HC-SR04?
2. ¿Qué es un ultrasonido?
3. ¿Qué frecuencia utiliza?
4. ¿Qué hace TRIG?
5. ¿Qué hace ECHO?
6. ¿Qué es TOF?
7. ¿Cuál es la velocidad del sonido?
8. ¿Por qué dividimos entre 2?
9. ¿Qué rango tiene el sensor?
10. ¿Qué aplicaciones industriales tiene?

---

# 33. Rúbrica de evaluación

| Criterio | Logrado | No logrado |
|-----------|----------|------------|
| Cableado correcto | | |
| Configuración GPIO | | |
| Función getSonar() | | |
| Cálculo correcto | | |
| Visualización por terminal | | |
| Comprensión teórica | | |

---

# 34. Prompt optimizado para GitHub Copilot

A partir de la especificaciones del archivo .md des este proyecto genera un programa MicroPython para ESP32-S3.

Conexiones:

- HC-SR04 Trigger → GPIO13
- HC-SR04 Echo → GPIO14

Requisitos:

- Crear función getSonar().
- Medir distancia en centímetros.
- Mostrar resultados por terminal.
- Añadir control de errores.
- Comentar cada línea.
- Mostrar distancia mínima y máxima.
- Preparar versión para MQTT.

---

# 35. Conclusiones

En este proyecto hemos aprendido a utilizar el sensor ultrasónico HC-SR04 para medir distancias sin contacto.

Hemos aplicado conceptos fundamentales:

- Entradas digitales.
- Temporización en microsegundos.
- Física del sonido.
- Cálculo matemático.
- Procesamiento de señales.

Estos conocimientos constituyen la base para futuros proyectos de:

- Robótica móvil.
- Automatización industrial.
- IoT.
- Vehículos autónomos.
- Sistemas de navegación.