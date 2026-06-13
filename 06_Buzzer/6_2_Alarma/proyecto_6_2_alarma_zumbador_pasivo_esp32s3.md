# Proyecto 6.2 – Alarma con zumbador pasivo
## ESP32-S3 WROOM + MicroPython

---

## 1. Objetivo del proyecto

En este proyecto construiremos una alarma sencilla utilizando:

- Un botón pulsador.
- Un zumbador pasivo.
- Un transistor NPN S8050.
- Una placa ESP32-S3 WROOM.

El funcionamiento será:

- Al pulsar el botón, el zumbador pasivo emitirá sonido.
- Al soltar el botón, el zumbador dejará de sonar.

A diferencia del proyecto anterior, donde se utilizaba un zumbador activo, en este proyecto se utilizará un zumbador pasivo.  
El zumbador pasivo necesita recibir una señal PWM con una frecuencia determinada para poder emitir sonido.

---

## 2. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3 WROOM | 1 |
| Placa de expansión GPIO | 1 |
| Protoboard de 830 puntos | 1 |
| Transistor NPN S8050 | 2 |
| Zumbador pasivo | 1 |
| Resistencia de 10 kΩ | 2 |
| Resistencia de 1 kΩ | 1 |
| Botón pulsador | 1 |
| Cables Dupont | 6 |

---

## 3. Objetivos de aprendizaje

Al finalizar este proyecto, el alumno debe ser capaz de:

1. Diferenciar entre un zumbador activo y un zumbador pasivo.
2. Comprender por qué un zumbador pasivo necesita PWM.
3. Leer el estado de un botón pulsador desde MicroPython.
4. Activar una salida PWM cuando se pulsa un botón.
5. Detener la señal PWM cuando se suelta el botón.
6. Comprender el uso de un transistor como interruptor electrónico.
7. Crear una alarma básica controlada mediante software.

---

## 4. Descripción del proyecto

El circuito es muy parecido al del proyecto anterior del timbre de puerta.

La diferencia principal es que ahora sustituimos el zumbador activo por un zumbador pasivo.

Un zumbador activo solo necesita recibir tensión para sonar.  
Un zumbador pasivo necesita una señal PWM con una frecuencia determinada.

```text
Botón pulsado
↓
ESP32 genera PWM
↓
Transistor S8050 conmuta
↓
Zumbador pasivo suena
```

```text
Botón liberado
↓
ESP32 detiene PWM
↓
Transistor deja de conducir
↓
Zumbador pasivo se apaga
```

---

## 5. Tabla de conexiones

Se puede utilizar el mismo circuito del proyecto anterior, sustituyendo el zumbador activo por un zumbador pasivo.

| Elemento | Terminal | Conexión |
|----------|----------|----------|
| Botón pulsador | Terminal 1 | GPIO 2 |
| Botón pulsador | Terminal 2 | GND |
| ESP32-S3 | GPIO 2 | Entrada del botón |
| ESP32-S3 | GPIO 1 | Salida PWM hacia transistor |
| GPIO 1 | - | Resistencia de 1 kΩ |
| Resistencia 1 kΩ | - | Base del transistor S8050 |
| Transistor S8050 | Emisor | GND |
| Transistor S8050 | Colector | Terminal negativo del zumbador pasivo |
| Zumbador pasivo | Terminal positivo | 3.3 V |
| Zumbador pasivo | Terminal negativo | Colector del transistor |
| ESP32-S3 | GND | Línea GND de la protoboard |

---

## 6. Esquema ASCII del circuito

```text
                         ESP32-S3 WROOM
                    +----------------------+
                    |                      |
GPIO 2 -------------+                      |
                    |                      |
GPIO 1 -------------+                      |
                    |                      |
GND    -------------+                      |
                    +----------------------+

Parte del botón:

GPIO 2 ----[ BOTÓN ]---- GND

Parte del zumbador pasivo:

GPIO 1 ----[1 kΩ]---- Base S8050

Colector S8050 ---- Terminal negativo zumbador
Terminal positivo zumbador ---- 3.3 V

Emisor S8050 ---- GND
```

---

## 7. ¿Qué es un zumbador pasivo?

Un zumbador pasivo es un componente que puede producir sonido, pero no tiene un oscilador interno.

Esto significa que no basta con conectarlo a 3.3 V y GND.

Para sonar necesita recibir una señal oscilante generada por PWM.

---

## 8. Diferencia entre zumbador activo y pasivo

| Tipo de zumbador | ¿Tiene oscilador interno? | Forma de control |
|------------------|---------------------------|------------------|
| Activo | Sí | Encender/apagar con `value(1)` y `value(0)` |
| Pasivo | No | Generar PWM a una frecuencia determinada |

---

## 9. ¿Por qué usamos PWM?

PWM significa Pulse Width Modulation o modulación por ancho de pulso.

En este proyecto no se usa PWM para controlar brillo, sino para generar una señal sonora.

Una frecuencia PWM de unos 1000 Hz produce un tono audible.

```python
buzzer.freq(1000)
```

Esto indica que el zumbador vibrará a 1000 ciclos por segundo.

---

## 10. Funcionamiento esperado

```text
Botón sin pulsar
↓
PWM detenido
↓
Zumbador apagado
```

```text
Botón pulsado
↓
PWM activo a 1000 Hz
↓
Zumbador sonando
```

```text
Botón liberado
↓
PWM detenido
↓
Zumbador apagado
```

---

## 11. Requisitos obligatorios del código

El archivo `main.py` generado debe cumplir estos requisitos:

1. Utilizar MicroPython.
2. Importar `Pin` y `PWM` desde `machine`.
3. Importar `time`.
4. Configurar el botón en GPIO 2 como entrada digital.
5. Usar `Pin.PULL_UP` para el botón.
6. Configurar GPIO 1 como salida PWM para el zumbador.
7. Usar una frecuencia inicial de 1000 Hz.
8. Activar el PWM mientras el botón esté pulsado.
9. Desactivar el PWM cuando el botón esté liberado.
10. Usar un bucle infinito.
11. Incluir comentarios explicativos.
12. Ser adecuado para alumnado principiante.

---

## 12. Código de referencia esperado

```python
from machine import Pin, PWM
import time

boton = Pin(2, Pin.IN, Pin.PULL_UP)

buzzer = PWM(Pin(1))
buzzer.freq(1000)
buzzer.duty_u16(0)

while True:

    if boton.value() == 0:
        buzzer.duty_u16(32768)
    else:
        buzzer.duty_u16(0)

    time.sleep_ms(10)
```

---

## 13. Versión con antirrebote

```python
from machine import Pin, PWM
import time

boton = Pin(2, Pin.IN, Pin.PULL_UP)

buzzer = PWM(Pin(1))
buzzer.freq(1000)
buzzer.duty_u16(0)

while True:

    if boton.value() == 0:
        time.sleep_ms(30)

        if boton.value() == 0:
            buzzer.duty_u16(32768)

    else:
        buzzer.duty_u16(0)

    time.sleep_ms(10)
```

---

## 14. Versión con sonido de alarma intermitente

```python
from machine import Pin, PWM
import time

boton = Pin(2, Pin.IN, Pin.PULL_UP)

buzzer = PWM(Pin(1))
buzzer.duty_u16(0)

while True:

    if boton.value() == 0:

        buzzer.freq(800)
        buzzer.duty_u16(32768)
        time.sleep_ms(200)

        buzzer.freq(1200)
        buzzer.duty_u16(32768)
        time.sleep_ms(200)

    else:
        buzzer.duty_u16(0)
        time.sleep_ms(10)
```

---

## 15. Valores recomendados

| Parámetro | Valor recomendado |
|----------|-------------------|
| GPIO botón | GPIO 2 |
| GPIO zumbador | GPIO 1 |
| Frecuencia baja | 800 Hz |
| Frecuencia media | 1000 Hz |
| Frecuencia alta | 1200 Hz |
| Duty cycle | 32768 |
| Retardo de lectura | 10 ms |
| Antirrebote | 30 ms |

---

## 16. Errores frecuentes

### 16.1 El zumbador no suena

Posibles causas:

- Se ha usado `value(1)` en lugar de PWM.
- El zumbador es pasivo y no recibe frecuencia.
- El transistor está mal orientado.
- El zumbador está conectado al revés.
- El GPIO no coincide con el montaje.

Comprobar que se usa:

```python
buzzer = PWM(Pin(1))
buzzer.freq(1000)
buzzer.duty_u16(32768)
```

---

### 16.2 El zumbador suena siempre

Posibles causas:

- El botón está mal conectado.
- No se usa `Pin.PULL_UP`.
- La lógica está invertida.
- El transistor está conduciendo permanentemente.

Con `Pin.PULL_UP`:

```text
Botón sin pulsar = 1
Botón pulsado = 0
```

---

### 16.3 El sonido es muy bajo

Posibles causas:

- Duty cycle demasiado bajo.
- Alimentación insuficiente.
- Zumbador pasivo de baja sensibilidad.

Probar:

```python
buzzer.duty_u16(32768)
```

---

### 16.4 El sonido no es agradable

Cambiar la frecuencia:

```python
buzzer.freq(500)
buzzer.freq(1000)
buzzer.freq(1500)
buzzer.freq(2000)
```

---

### 16.5 El ESP32 se reinicia

Posibles causas:

- Cortocircuito.
- Zumbador conectado directamente al GPIO sin transistor.
- Error de conexión en el transistor.
- Consumo excesivo.

---

## 17. Retos para el alumnado

### Nivel básico

Cambiar la frecuencia del sonido.

### Nivel medio

Hacer que la alarma suene de forma intermitente.

### Nivel avanzado

Crear una sirena que suba y baje de tono.

### Nivel experto

Añadir un LED RGB que cambie de color mientras suena la alarma.

---

## 18. Preguntas para el alumnado

1. ¿Qué diferencia hay entre un zumbador activo y uno pasivo?
2. ¿Por qué el zumbador pasivo necesita PWM?
3. ¿Qué instrucción se usa para cambiar la frecuencia?
4. ¿Qué instrucción se usa para apagar el zumbador?
5. ¿Qué valor lee el GPIO del botón cuando se pulsa usando `Pin.PULL_UP`?
6. ¿Para qué sirve el transistor S8050?
7. ¿Qué ocurre si conectamos el zumbador directamente al GPIO?
8. ¿Cómo harías que la alarma tuviera dos tonos diferentes?

---

## 19. Criterios de evaluación

| Criterio | Logrado | No logrado |
|---------|---------|------------|
| Conecta correctamente el botón | | |
| Conecta correctamente el transistor | | |
| Conecta correctamente el zumbador pasivo | | |
| Usa PWM en el zumbador | | |
| El zumbador suena al pulsar | | |
| El zumbador se apaga al soltar | | |
| El código está comentado | | |
| El alumno entiende la diferencia entre zumbador activo y pasivo | | |

---

## 20. Prompt optimizado para GitHub Copilot / Cursor / IA de VS Code

Genera un archivo `main.py` para MicroPython destinado a una placa ESP32-S3 WROOM.

El proyecto consiste en crear una alarma con un zumbador pasivo controlado mediante un botón.

Requisitos:

- Utilizar un botón pulsador conectado al GPIO 2.
- Configurar el botón como entrada con `Pin.PULL_UP`.
- Utilizar un zumbador pasivo controlado mediante transistor S8050.
- El GPIO 1 debe generar la señal PWM para el zumbador.
- Configurar el PWM inicialmente a 1000 Hz.
- El zumbador debe sonar mientras el botón esté pulsado.
- El zumbador debe apagarse al soltar el botón.
- Para activar el sonido usar `duty_u16(32768)`.
- Para apagar el sonido usar `duty_u16(0)`.
- El programa debe ejecutarse indefinidamente.
- Incluir comentarios explicativos.
- Código claro y adecuado para alumnado principiante de Formación Profesional.

---

## 21. Resultado esperado

Al ejecutar el programa en el ESP32-S3 WROOM:

- Si el botón no está pulsado, el zumbador permanece apagado.
- Si el botón está pulsado, el ESP32 genera PWM y el zumbador pasivo suena.
- Al soltar el botón, el zumbador deja de sonar.

Este proyecto permite comprender cómo se controla un dispositivo sonoro pasivo usando una señal PWM.
