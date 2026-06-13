# Proyecto 6.1 – Timbre de puerta con ESP32-S3 WROOM
## Control de un zumbador mediante un pulsador

---

# 1. Objetivo del proyecto

En este proyecto construiremos un timbre electrónico similar al de una puerta.

El funcionamiento será muy sencillo:

- Al pulsar el botón, el zumbador emitirá sonido.
- Al soltar el botón, el zumbador dejará de sonar.

Este proyecto es equivalente al proyecto del LED controlado mediante pulsador, pero sustituyendo el LED por un zumbador activo.

---

# 2. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| Transistor NPN S8050 | 2 |
| Zumbador activo | 1 |
| Resistencia 10 kΩ | 2 |
| Resistencia 1 kΩ | 1 |
| Pulsador | 1 |
| Cables Dupont | 6 |

---

# 3. Objetivos de aprendizaje

Al finalizar esta práctica el alumno será capaz de:

- Utilizar entradas digitales.
- Utilizar salidas digitales.
- Leer el estado de un pulsador.
- Controlar un zumbador activo.
- Comprender el uso de un transistor como interruptor electrónico.
- Programar entradas y salidas en MicroPython.

---

# 4. Descripción del circuito

El pulsador se conecta a una entrada digital del ESP32-S3.

Cuando el usuario pulsa el botón:

1. El ESP32 detecta la pulsación.
2. Activa la salida conectada al transistor.
3. El transistor permite el paso de corriente hacia el zumbador.
4. El zumbador emite sonido.

Cuando el botón se libera:

1. El ESP32 detecta el cambio de estado.
2. Desactiva la salida.
3. El transistor deja de conducir.
4. El zumbador deja de sonar.

---

# 5. Tabla de conexiones

Según el esquema del kit:

| Elemento | Conexión |
|-----------|-----------|
| Pulsador | GPIO 2 |
| Pulsador | GND |
| Base transistor S8050 | GPIO 1 mediante resistencia 1 kΩ |
| Emisor transistor | GND |
| Colector transistor | Terminal negativo del zumbador |
| Terminal positivo del zumbador | 3.3 V |
| Resistencias 10 kΩ | Pull-up / polarización según esquema |

---

# 6. Esquema ASCII simplificado

```text
                 ESP32-S3

                 GPIO 2
                    |
                    |
                 [BOTÓN]
                    |
                    |
                   GND


                 GPIO 1
                    |
                  [1kΩ]
                    |
                    |
                Base S8050
                    |
                    |
                 Colector
                    |
                ZUMBADOR
                    |
                   3.3V

Emisor S8050
      |
     GND
```

---

# 7. ¿Qué es un zumbador activo?

Existen dos tipos principales de zumbadores:

## Zumbador activo

Contiene un oscilador interno.

Solo necesita alimentación para emitir sonido.

Ejemplo:

```python
buzzer.value(1)
```

produce sonido.

---

## Zumbador pasivo

No contiene oscilador interno.

Necesita una señal PWM para producir sonido.

Este proyecto utiliza un zumbador activo.

---

# 8. ¿Por qué se utiliza un transistor?

Aunque el ESP32 puede activar dispositivos pequeños, muchas veces es recomendable utilizar un transistor.

Ventajas:

- Protege la salida GPIO.
- Permite manejar más corriente.
- Mejora la fiabilidad del circuito.

El transistor S8050 funciona como un interruptor electrónico.

```text
GPIO = 1
↓
Transistor conduce
↓
Zumbador suena
```

```text
GPIO = 0
↓
Transistor bloqueado
↓
Zumbador apagado
```

---

# 9. Funcionamiento esperado

Estado inicial:

```text
Botón suelto
↓
Zumbador apagado
```

Al pulsar:

```text
Botón pulsado
↓
Zumbador encendido
```

Al liberar:

```text
Botón suelto
↓
Zumbador apagado
```

---

# 10. Requisitos obligatorios del código

El archivo main.py debe:

1. Utilizar MicroPython.
2. Importar Pin desde machine.
3. Configurar el GPIO del pulsador como entrada.
4. Configurar el GPIO del zumbador como salida.
5. Leer continuamente el estado del pulsador.
6. Activar el zumbador mientras el botón permanezca pulsado.
7. Desactivar el zumbador cuando el botón se libere.
8. Utilizar un bucle infinito.
9. Incluir comentarios explicativos.

---

# 11. Código de referencia esperado

```python
from machine import Pin
import time

# Pulsador
boton = Pin(2, Pin.IN, Pin.PULL_UP)

# Salida hacia el transistor
buzzer = Pin(1, Pin.OUT)

while True:

    if boton.value() == 0:
        buzzer.value(1)
    else:
        buzzer.value(0)

    time.sleep_ms(10)
```

---

# 12. Versión con antirrebote

```python
from machine import Pin
import time

boton = Pin(2, Pin.IN, Pin.PULL_UP)
buzzer = Pin(1, Pin.OUT)

while True:

    if boton.value() == 0:

        time.sleep_ms(30)

        if boton.value() == 0:
            buzzer.value(1)

    else:
        buzzer.value(0)

    time.sleep_ms(10)
```

---

# 13. Errores frecuentes

## El zumbador no suena

Posibles causas:

- GPIO incorrecto.
- Transistor conectado al revés.
- Zumbador invertido.
- Falta alimentación.

---

## El zumbador suena siempre

Posibles causas:

- Pulsador mal cableado.
- Resistencia de pull-up incorrecta.
- Lógica invertida.

---

## El zumbador suena de forma intermitente

Posibles causas:

- Rebotes mecánicos del pulsador.
- Conexiones flojas.
- Falta antirrebote por software.

---

## El ESP32 se reinicia al sonar

Posibles causas:

- Consumo excesivo.
- Cortocircuito.
- Transistor mal conectado.

---

# 14. Retos para el alumnado

## Nivel básico

Cambiar el GPIO utilizado.

---

## Nivel medio

Añadir un LED que se encienda mientras suena el timbre.

---

## Nivel avanzado

Crear un temporizador para que el timbre suene durante 3 segundos.

---

## Nivel experto

Convertir el timbre en una alarma con diferentes patrones de sonido.

---

# 15. Preguntas para el alumnado

1. ¿Qué diferencia existe entre un zumbador activo y uno pasivo?
2. ¿Para qué sirve el transistor S8050?
3. ¿Qué ocurre cuando el pulsador está presionado?
4. ¿Qué ocurre cuando se libera el pulsador?
5. ¿Por qué se utiliza una resistencia de 1 kΩ en la base?
6. ¿Qué es el antirrebote?
7. ¿Qué ventaja tiene usar Pin.PULL_UP?
8. ¿Cómo podríamos añadir un LED indicador?

---

# 16. Criterios de evaluación

| Criterio | Logrado | No logrado |
|-----------|----------|------------|
| Cablea correctamente el pulsador | | |
| Cablea correctamente el transistor | | |
| Cablea correctamente el zumbador | | |
| Configura las entradas y salidas | | |
| El timbre funciona correctamente | | |
| El código está comentado | | |
| Comprende el funcionamiento del transistor | | |
| Comprende el funcionamiento del pulsador | | |

---

# 17. Prompt optimizado para GitHub Copilot / Cursor

Genera un archivo main.py para MicroPython destinado a una placa ESP32-S3 WROOM.

El proyecto consiste en crear un timbre electrónico.

Requisitos:

- Utilizar un pulsador conectado al GPIO 2.
- Utilizar un transistor S8050 para controlar un zumbador activo.
- Utilizar GPIO 1 como salida hacia la base del transistor mediante una resistencia de 1 kΩ.
- El zumbador debe sonar únicamente mientras el botón permanezca pulsado.
- Al liberar el botón debe dejar de sonar inmediatamente.
- Utilizar Pin.PULL_UP para la entrada.
- Utilizar un bucle infinito.
- Incluir comentarios explicativos.
- Código sencillo y adecuado para alumnado principiante.

---

# 18. Resultado esperado

Al ejecutar el programa:

- Pulsador sin presionar → zumbador apagado.
- Pulsador presionado → zumbador encendido.
- Pulsador liberado → zumbador apagado.

El comportamiento debe ser idéntico al de un timbre de puerta convencional.
