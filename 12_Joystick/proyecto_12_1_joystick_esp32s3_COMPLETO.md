# Proyecto 12.1 – Joystick
## ESP32-S3 WROOM + MicroPython

---

# 1. Objetivo del proyecto

En este proyecto aprenderemos a utilizar un módulo **joystick analógico** con una placa **ESP32-S3 WROOM**.

El joystick funciona de forma parecida a dos potenciómetros:

- Un potenciómetro interno mide el movimiento horizontal, eje X.
- Otro potenciómetro interno mide el movimiento vertical, eje Y.
- Además, muchos módulos joystick incluyen un pulsador integrado, llamado SW, que se activa al presionar el joystick hacia abajo.

En esta práctica leeremos los valores de salida del joystick usando el ADC del ESP32-S3 y mostraremos los datos en el monitor serie.

Este proyecto sirve como base para crear sistemas de control como:

- Robots móviles.
- Videojuegos.
- Menús interactivos.
- Control de servomotores.
- Control de cámaras.
- Sistemas HMI.

---

# 2. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard de 830 puntos | 1 |
| Módulo joystick | 1 |
| Cables Dupont | 5 |

---

# 3. Objetivos de aprendizaje

Al finalizar esta práctica, el alumno debe ser capaz de:

1. Identificar los pines principales de un joystick analógico.
2. Comprender que un joystick contiene dos potenciómetros internos.
3. Leer valores analógicos mediante ADC.
4. Leer dos ejes analógicos, X e Y.
5. Leer el pulsador integrado del joystick.
6. Mostrar datos por el monitor serie.
7. Interpretar coordenadas bidimensionales.
8. Crear una base para controlar robots o interfaces interactivas.

---

# 4. Descripción del joystick

Un módulo joystick típico tiene cinco pines:

| Pin del joystick | Función |
|------------------|---------|
| GND | Tierra |
| +5V / VCC | Alimentación |
| VRX | Salida analógica eje X |
| VRY | Salida analógica eje Y |
| SW | Pulsador integrado |

En este proyecto se recomienda alimentar el joystick con **3.3 V**, no con 5 V, para que las señales analógicas no superen el rango seguro del ESP32-S3.

---

# 5. Conexiones del montaje

Según el montaje proporcionado:

| Pin del joystick | Conexión ESP32-S3 |
|------------------|-------------------|
| GND | GND |
| VCC / +5V | 3.3 V |
| VRX | GPIO 1 |
| VRY | GPIO 2 |
| SW | GPIO 41 |

---

# 6. Tabla detallada de conexiones

| Elemento | Terminal | Conexión |
|----------|----------|----------|
| Joystick | GND | GND de la placa |
| Joystick | VCC | 3.3 V |
| Joystick | VRX | GPIO 1 |
| Joystick | VRY | GPIO 2 |
| Joystick | SW | GPIO 41 |
| ESP32-S3 | USB-C | Ordenador |

---

# 7. Esquema ASCII del circuito

```text
               ESP32-S3 WROOM

          +----------------------+
          |                      |
GPIO 1 <--| ADC eje X            |
GPIO 2 <--| ADC eje Y            |
GPIO 41 <-| Pulsador SW          |
3.3V  --->| Alimentación joystick|
GND   --->| GND                  |
          |                      |
          +----------------------+


                 JOYSTICK

             +-------------+
             |             |
             |      O      |
             |             |
             +-------------+

                 Pines:

                 GND  ---- GND
                 VCC  ---- 3.3 V
                 VRX  ---- GPIO 1
                 VRY  ---- GPIO 2
                 SW   ---- GPIO 41
```

---

# 8. ¿Cómo funciona un joystick analógico?

Un joystick analógico tiene dos potenciómetros internos:

## Eje X

Detecta el movimiento horizontal:

```text
Izquierda  <---- Centro ---->  Derecha
```

## Eje Y

Detecta el movimiento vertical:

```text
Arriba
  |
Centro
  |
Abajo
```

Cada eje genera una tensión variable que puede leer el ADC del ESP32-S3.

---

# 9. ADC del ESP32-S3

ADC significa:

```text
Analog to Digital Converter
```

o:

```text
Convertidor Analógico-Digital
```

Su función es convertir una tensión eléctrica en un número.

Rango habitual:

```text
0 V    -> 0
3.3 V  -> 4095
```

El valor central suele estar aproximadamente en:

```text
2048
```

---

# 10. Coordenadas del joystick

En este proyecto se toma como referencia el origen de coordenadas en la esquina superior izquierda.

```text
(0,0)
  +-----------------> X
  |
  |
  |
  v
  Y
```

Por tanto:

- X aumenta al mover el joystick hacia la derecha.
- Y aumenta al mover el joystick hacia abajo.

---

# 11. Valores típicos esperados

| Posición del joystick | Valor X | Valor Y |
|-----------------------|---------|---------|
| Centro | ≈ 2048 | ≈ 2048 |
| Izquierda | ≈ 0 | ≈ 2048 |
| Derecha | ≈ 4095 | ≈ 2048 |
| Arriba | ≈ 2048 | ≈ 0 |
| Abajo | ≈ 2048 | ≈ 4095 |

Los valores pueden variar ligeramente según el joystick y el montaje.

---

# 12. Funcionamiento esperado

El programa debe:

1. Configurar GPIO 1 como entrada ADC para el eje X.
2. Configurar GPIO 2 como entrada ADC para el eje Y.
3. Configurar GPIO 41 como entrada digital para el pulsador.
4. Leer continuamente los valores X e Y.
5. Leer el estado del pulsador SW.
6. Mostrar todos los datos por el monitor serie.
7. Actualizar la información cada 200 ms.

---

# 13. Código básico para leer X e Y

```python
from machine import Pin, ADC
import time

x_axis = ADC(Pin(1))
y_axis = ADC(Pin(2))

while True:

    x = x_axis.read()
    y = y_axis.read()

    print("X =", x, "Y =", y)

    time.sleep(0.2)
```

---

# 14. Código con formato mejorado

```python
from machine import Pin, ADC
import time

x_axis = ADC(Pin(1))
y_axis = ADC(Pin(2))

while True:

    x = x_axis.read()
    y = y_axis.read()

    print("--------------------")
    print("Eje X:", x)
    print("Eje Y:", y)

    time.sleep(0.2)
```

---

# 15. Lectura del pulsador SW

El pulsador integrado se leerá como una entrada digital.

Usaremos resistencia interna `Pin.PULL_UP`.

Con esta configuración:

| Estado del pulsador | Lectura |
|---------------------|---------|
| Sin pulsar | 1 |
| Pulsado | 0 |

Ejemplo:

```python
from machine import Pin

button = Pin(41, Pin.IN, Pin.PULL_UP)

if button.value() == 0:
    print("Pulsado")
else:
    print("Sin pulsar")
```

---

# 16. Código completo del proyecto

```python
from machine import Pin, ADC
import time

# Ejes analógicos del joystick
x_axis = ADC(Pin(1))
y_axis = ADC(Pin(2))

# Pulsador integrado del joystick
button = Pin(41, Pin.IN, Pin.PULL_UP)

while True:

    # Leer valores analógicos
    x = x_axis.read()
    y = y_axis.read()

    # Leer pulsador
    if button.value() == 0:
        estado_boton = "PULSADO"
    else:
        estado_boton = "SIN PULSAR"

    # Mostrar resultados por monitor serie
    print("--------------------")
    print("X:", x)
    print("Y:", y)
    print("SW:", estado_boton)

    time.sleep(0.2)
```

---

# 17. Versión con porcentajes

Esta versión convierte los valores ADC a porcentaje.

```python
from machine import Pin, ADC
import time

x_axis = ADC(Pin(1))
y_axis = ADC(Pin(2))
button = Pin(41, Pin.IN, Pin.PULL_UP)

while True:

    x = x_axis.read()
    y = y_axis.read()

    x_percent = int((x / 4095) * 100)
    y_percent = int((y / 4095) * 100)

    if button.value() == 0:
        estado_boton = "PULSADO"
    else:
        estado_boton = "SIN PULSAR"

    print(
        "X:", x_percent, "%",
        "Y:", y_percent, "%",
        "SW:", estado_boton
    )

    time.sleep(0.2)
```

---

# 18. Versión avanzada: detección de dirección

Esta versión interpreta la dirección del joystick.

```python
from machine import Pin, ADC
import time

x_axis = ADC(Pin(1))
y_axis = ADC(Pin(2))
button = Pin(41, Pin.IN, Pin.PULL_UP)

CENTRO_MIN = 1600
CENTRO_MAX = 2500

while True:

    x = x_axis.read()
    y = y_axis.read()

    direccion = "CENTRO"

    if x < CENTRO_MIN:
        direccion = "IZQUIERDA"
    elif x > CENTRO_MAX:
        direccion = "DERECHA"

    if y < CENTRO_MIN:
        direccion = "ARRIBA"
    elif y > CENTRO_MAX:
        direccion = "ABAJO"

    if button.value() == 0:
        pulsador = "PULSADO"
    else:
        pulsador = "SIN PULSAR"

    print("X:", x, "Y:", y, "Direccion:", direccion, "SW:", pulsador)

    time.sleep(0.2)
```

---

# 19. Versión avanzada: coordenadas normalizadas

Esta versión transforma el rango ADC 0-4095 en coordenadas de -100 a 100.

```python
from machine import Pin, ADC
import time

x_axis = ADC(Pin(1))
y_axis = ADC(Pin(2))

def normalizar(valor):
    return int(((valor - 2048) / 2048) * 100)

while True:

    x = x_axis.read()
    y = y_axis.read()

    x_norm = normalizar(x)
    y_norm = normalizar(y)

    print("X:", x_norm, "Y:", y_norm)

    time.sleep(0.2)
```

---

# 20. Aplicaciones reales

Los joysticks analógicos se utilizan en:

- Mandos de videojuegos.
- Robots móviles.
- Drones.
- Control de cámaras.
- Sillas de ruedas eléctricas.
- Simuladores.
- Grúas industriales.
- Sistemas de control HMI.
- Control de servomotores.

---

# 21. Errores frecuentes

## El eje X siempre vale 0

Posibles causas:

- VRX mal conectado.
- GPIO incorrecto.
- Cable suelto.

---

## El eje Y siempre vale 4095

Posibles causas:

- VRY mal conectado.
- Cortocircuito con 3.3 V.
- Error de conexión.

---

## Los valores son inestables

Posibles causas:

- Cables flojos.
- Alimentación incorrecta.
- Joystick defectuoso.

---

## El botón SW no funciona

Posibles causas:

- SW conectado a otro GPIO.
- Falta `Pin.PULL_UP`.
- Error de lógica.

Recordatorio:

```text
Pin.PULL_UP:
Sin pulsar = 1
Pulsado = 0
```

---

## Los valores X e Y están invertidos

Solución:

- Intercambiar los cables VRX y VRY.
- O cambiar los pines en el código.

---

## La dirección arriba/abajo aparece invertida

Algunos módulos joystick tienen orientación distinta.

Solución:

- Invertir la interpretación del eje Y en el código.

---

# 22. Retos para el alumnado

## Nivel básico

Mostrar solo los valores X e Y.

---

## Nivel medio

Mostrar valores en porcentaje.

---

## Nivel avanzado

Detectar dirección:

```text
ARRIBA
ABAJO
IZQUIERDA
DERECHA
CENTRO
```

---

## Nivel avanzado 2

Controlar el brillo de un LED con el eje X.

---

## Nivel experto

Controlar un LED RGB:

- Eje X controla rojo.
- Eje Y controla verde.
- Pulsador cambia modo de color.

---

# 23. Preguntas para el alumnado

1. ¿Qué es un joystick analógico?
2. ¿Cuántos potenciómetros tiene internamente?
3. ¿Qué mide el eje X?
4. ¿Qué mide el eje Y?
5. ¿Qué función tiene el pulsador SW?
6. ¿Qué hace el ADC del ESP32-S3?
7. ¿Qué valor aproximado aparece cuando el joystick está centrado?
8. ¿Qué ocurre al mover el joystick hacia la derecha?
9. ¿Qué ocurre al mover el joystick hacia abajo?
10. ¿Por qué usamos `Pin.PULL_UP` para el pulsador?

---

# 24. Criterios de evaluación

| Criterio | Logrado | No logrado |
|-----------|----------|------------|
| Cablea correctamente el joystick | | |
| Configura correctamente los ADC | | |
| Lee correctamente el eje X | | |
| Lee correctamente el eje Y | | |
| Lee correctamente el pulsador SW | | |
| Muestra información por monitor serie | | |
| Interpreta direcciones básicas | | |
| Código comentado | | |
| Comprende el funcionamiento del joystick | | |

---

# 25. Prompt optimizado para GitHub Copilot / Cursor / VS Code

Genera un archivo `main.py` para una placa ESP32-S3 WROOM usando MicroPython.

El proyecto se llama **Proyecto 12.1 Joystick**.

Conexiones:

- VRX del joystick conectado a GPIO 1.
- VRY del joystick conectado a GPIO 2.
- SW del joystick conectado a GPIO 41.
- VCC del joystick conectado a 3.3 V.
- GND del joystick conectado a GND.

Requisitos:

- Importar `Pin` y `ADC` desde `machine`.
- Importar `time`.
- Configurar GPIO 1 como ADC para el eje X.
- Configurar GPIO 2 como ADC para el eje Y.
- Configurar GPIO 41 como entrada digital con `Pin.PULL_UP`.
- Leer continuamente los valores X e Y.
- Leer el estado del pulsador SW.
- Mostrar todos los valores por monitor serie.
- Actualizar cada 200 ms.
- Incluir comentarios explicativos.
- Crear una versión adicional que convierta X e Y a porcentaje.
- Crear otra versión que detecte las direcciones: ARRIBA, ABAJO, IZQUIERDA, DERECHA y CENTRO.
- Código sencillo, claro y adecuado para alumnado principiante de Formación Profesional.

---

# 26. Resultado esperado

Al ejecutar el programa:

- Al mover el joystick a izquierda/derecha, cambia el valor X.
- Al mover el joystick arriba/abajo, cambia el valor Y.
- Al presionar el joystick, se detecta el pulsador SW.
- Los datos se muestran continuamente en el monitor serie.
- El centro del joystick aparece aproximadamente alrededor de 2048 en ambos ejes.

Este proyecto permite comprender cómo leer controles analógicos bidimensionales con el ESP32-S3.
