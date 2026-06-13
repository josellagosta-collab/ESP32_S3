# Proyecto 5.2 – Luz de color degradado con LED RGB
## ESP32-S3 WROOM + MicroPython

---

## 1. Objetivo del proyecto

El objetivo de este proyecto es controlar un LED RGB con una placa ESP32-S3 WROOM para crear una luz multicolor con transiciones suaves.

En el proyecto 5.1 se generaban colores aleatorios. El resultado era correcto, pero los cambios de color eran bruscos.

En este proyecto se utilizará un modelo de color gradual, con valores entre 0 y 255, para que el LED RGB cambie suavemente de un color a otro.

El efecto esperado será parecido a una barra de degradado de color:

```text
Rojo → Amarillo → Verde → Cian → Azul → Magenta → Rojo
```

---

## 2. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3 WROOM | 1 |
| Placa de expansión GPIO | 1 |
| Protoboard de 830 puntos | 1 |
| LED RGB | 1 |
| Resistencia de 220 Ω | 3 |
| Cable Dupont | 4 |

---

## 3. Circuito utilizado

El circuito es el mismo que en el proyecto 5.1: Luz de color aleatorio.

Se usará un LED RGB conectado a tres salidas PWM del ESP32-S3.

---

## 4. Tabla de conexiones

Según el montaje usado en el proyecto anterior:

| Color del LED RGB | GPIO ESP32-S3 | Resistencia |
|-------------------|---------------|-------------|
| Rojo | GPIO 42 | 220 Ω |
| Verde | GPIO 41 | 220 Ω |
| Azul | GPIO 40 | 220 Ω |
| Terminal común del LED RGB | GND | - |

Cada color del LED RGB debe tener su propia resistencia de 220 Ω.

---

## 5. Esquema ASCII del circuito

```text
                         ESP32-S3 WROOM

                    +----------------------+
                    |                      |
GPIO 42 ------------+                      |
                    |                      |
GPIO 41 ------------+                      |
                    |                      |
GPIO 40 ------------+                      |
                    |                      |
GND    -------------+                      |
                    +----------------------+

Conexión del LED RGB:

GPIO 42 ----[220 Ω]---- Rojo  GPIO 41 ----[220 Ω]---- Verde  >---- LED RGB ---- GND
GPIO 40 ----[220 Ω]---- Azul  /
```

---

## 6. ¿Qué es un LED RGB?

Un LED RGB es un componente que contiene tres LEDs dentro de un mismo encapsulado:

- R: Red / Rojo
- G: Green / Verde
- B: Blue / Azul

Controlando el brillo de cada color podemos obtener muchos colores diferentes.

Ejemplos:

| Rojo | Verde | Azul | Color resultante |
|------|-------|------|------------------|
| 255 | 0 | 0 | Rojo |
| 0 | 255 | 0 | Verde |
| 0 | 0 | 255 | Azul |
| 255 | 255 | 0 | Amarillo |
| 0 | 255 | 255 | Cian |
| 255 | 0 | 255 | Magenta |
| 255 | 255 | 255 | Blanco |
| 0 | 0 | 0 | Apagado |

---

## 7. Fundamento teórico: modelo de color

En este proyecto se utiliza un valor numérico entre 0 y 255 para representar la posición dentro de un degradado de color.

La idea es recorrer progresivamente ese rango:

```text
0 → 1 → 2 → 3 → ... → 255
```

Cada valor genera una combinación diferente de rojo, verde y azul.

El resultado visual será una transición suave de colores.

---

## 8. PWM y conversión de valores

En muchos modelos de color se trabaja con valores entre 0 y 255.

Sin embargo, en MicroPython, la función `duty_u16()` usa valores entre:

```text
0 y 65535
```

Por tanto, es necesario convertir los valores de color de 8 bits a 16 bits.

Conversión:

```python
valor_pwm = valor_8bits * 257
```

Ejemplos:

| Valor 8 bits | Valor PWM 16 bits |
|-------------|-------------------|
| 0 | 0 |
| 85 | 21845 |
| 170 | 43690 |
| 255 | 65535 |

---

## 9. Funcionamiento esperado

El programa debe:

1. Configurar tres salidas PWM.
2. Usar una salida para el rojo.
3. Usar una salida para el verde.
4. Usar una salida para el azul.
5. Recorrer progresivamente valores de 0 a 255.
6. Convertir cada valor en un color RGB.
7. Aplicar el color al LED RGB.
8. Repetir el proceso indefinidamente.

El cambio de color no debe ser brusco, sino suave y progresivo.

---

## 10. Modelo de color recomendado

Para conseguir una transición suave, se puede usar una función que convierta un valor entre 0 y 255 en tres valores RGB.

Secuencia aproximada:

| Rango | Transición |
|------|------------|
| 0 - 42 | Rojo a amarillo |
| 43 - 85 | Amarillo a verde |
| 86 - 127 | Verde a cian |
| 128 - 170 | Cian a azul |
| 171 - 212 | Azul a magenta |
| 213 - 255 | Magenta a rojo |

---

## 11. Requisitos obligatorios del código

El archivo `main.py` generado debe cumplir estos requisitos:

1. Usar MicroPython.
2. Importar `Pin` y `PWM` desde `machine`.
3. Importar `time`.
4. Crear tres canales PWM.
5. Usar GPIO 42 para rojo.
6. Usar GPIO 41 para verde.
7. Usar GPIO 40 para azul.
8. Configurar frecuencia PWM de 1000 Hz.
9. Crear una función para convertir valores de 0 a 255 en colores RGB.
10. Convertir valores RGB de 0-255 a valores PWM de 0-65535.
11. Cambiar el color de forma suave.
12. Ejecutarse indefinidamente.
13. Incluir comentarios explicativos.
14. Usar nombres de variables claros.

---

## 12. Código de referencia esperado

```python
from machine import Pin, PWM
import time

# Configuración de los canales PWM del LED RGB
rojo = PWM(Pin(42))
verde = PWM(Pin(41))
azul = PWM(Pin(40))

# Frecuencia PWM
rojo.freq(1000)
verde.freq(1000)
azul.freq(1000)


def convertir_8bits_a_pwm(valor):
    """Convierte un valor de 0-255 a 0-65535."""
    return valor * 257


def aplicar_color(r, g, b):
    """Aplica un color RGB al LED."""
    rojo.duty_u16(convertir_8bits_a_pwm(r))
    verde.duty_u16(convertir_8bits_a_pwm(g))
    azul.duty_u16(convertir_8bits_a_pwm(b))


def rueda_color(posicion):
    """
    Convierte un valor de 0 a 255 en un color RGB.
    El color cambia de forma suave siguiendo una rueda de color.
    """

    if posicion < 43:
        r = 255
        g = posicion * 6
        b = 0

    elif posicion < 86:
        posicion -= 43
        r = 255 - posicion * 6
        g = 255
        b = 0

    elif posicion < 129:
        posicion -= 86
        r = 0
        g = 255
        b = posicion * 6

    elif posicion < 172:
        posicion -= 129
        r = 0
        g = 255 - posicion * 6
        b = 255

    elif posicion < 215:
        posicion -= 172
        r = posicion * 6
        g = 0
        b = 255

    else:
        posicion -= 215
        r = 255
        g = 0
        b = 255 - posicion * 6

    return r, g, b


while True:
    for posicion in range(256):
        r, g, b = rueda_color(posicion)
        aplicar_color(r, g, b)
        time.sleep_ms(20)
```

---

## 13. Versión alternativa más sencilla

Esta versión utiliza menos teoría y es más fácil para alumnado principiante.

```python
from machine import Pin, PWM
import time

rojo = PWM(Pin(42))
verde = PWM(Pin(41))
azul = PWM(Pin(40))

for canal in (rojo, verde, azul):
    canal.freq(1000)

def pwm(valor):
    return valor * 257

while True:

    # Rojo a verde
    for i in range(256):
        rojo.duty_u16(pwm(255 - i))
        verde.duty_u16(pwm(i))
        azul.duty_u16(0)
        time.sleep_ms(15)

    # Verde a azul
    for i in range(256):
        rojo.duty_u16(0)
        verde.duty_u16(pwm(255 - i))
        azul.duty_u16(pwm(i))
        time.sleep_ms(15)

    # Azul a rojo
    for i in range(256):
        rojo.duty_u16(pwm(i))
        verde.duty_u16(0)
        azul.duty_u16(pwm(255 - i))
        time.sleep_ms(15)
```

---

## 14. Errores frecuentes

### 14.1 El LED RGB no se enciende

Posibles causas:

- El LED RGB está conectado al revés.
- Falta la conexión GND.
- Las resistencias no están bien conectadas.
- Los GPIO del código no coinciden con el montaje.

---

### 14.2 Los colores salen cambiados

Posibles causas:

- El pin del rojo, verde o azul está intercambiado.
- El LED RGB tiene un orden de patas diferente al esperado.

Solución:

Cambiar la asignación de pines en el código:

```python
rojo = PWM(Pin(42))
verde = PWM(Pin(41))
azul = PWM(Pin(40))
```

---

### 14.3 El color cambia a saltos

Posibles causas:

- El retardo es demasiado grande.
- El incremento entre colores es demasiado alto.

Solución:

Usar:

```python
time.sleep_ms(10)
```

o:

```python
time.sleep_ms(20)
```

---

### 14.4 El LED parece siempre blanco

Posibles causas:

- Los tres colores están muy altos al mismo tiempo.
- El código no está generando bien la rueda de color.

---

### 14.5 El LED funciona al revés

Algunos LEDs RGB son de ánodo común en lugar de cátodo común.

Si tu LED RGB es de ánodo común, el brillo se invierte:

- 0 puede significar máximo brillo.
- 65535 puede significar apagado.

En ese caso, se debe modificar la función de aplicación de color:

```python
def aplicar_color(r, g, b):
    rojo.duty_u16(65535 - convertir_8bits_a_pwm(r))
    verde.duty_u16(65535 - convertir_8bits_a_pwm(g))
    azul.duty_u16(65535 - convertir_8bits_a_pwm(b))
```

---

## 15. Desafíos para el alumnado

### Nivel básico

Cambiar la velocidad del degradado.

---

### Nivel medio

Crear una lista de colores y hacer transiciones entre ellos.

---

### Nivel avanzado

Añadir un botón para cambiar entre modo aleatorio y modo degradado.

---

### Nivel experto

Controlar el color RGB desde una página web servida por el ESP32-S3.

---

## 16. Preguntas para el alumnado

1. ¿Qué significa RGB?
2. ¿Por qué un LED RGB necesita tres resistencias?
3. ¿Qué diferencia hay entre el proyecto 5.1 y el proyecto 5.2?
4. ¿Qué es PWM?
5. ¿Por qué se convierte de 0-255 a 0-65535?
6. ¿Qué ocurre si intercambiamos los pines rojo y azul?
7. ¿Qué significa que un LED RGB sea de ánodo común?
8. ¿Cómo harías que el cambio de color fuera más rápido?

---

## 17. Criterios de evaluación

| Criterio | Logrado | No logrado |
|---------|---------|------------|
| Conecta correctamente el LED RGB | | |
| Usa tres resistencias de 220 Ω | | |
| Configura correctamente tres canales PWM | | |
| Genera colores mediante valores RGB | | |
| Realiza una transición suave | | |
| El programa se ejecuta indefinidamente | | |
| El código está comentado | | |
| El alumno comprende la conversión 0-255 a 0-65535 | | |

---

## 18. Prompt optimizado para GitHub Copilot / Cursor / IA de VS Code

Genera un archivo `main.py` para MicroPython destinado a una placa ESP32-S3 WROOM.

El proyecto consiste en controlar un LED RGB para crear una luz de color degradado.

Requisitos:

- Utilizar GPIO 42 para el color rojo.
- Utilizar GPIO 41 para el color verde.
- Utilizar GPIO 40 para el color azul.
- Cada color debe conectarse mediante una resistencia de 220 Ω.
- El terminal común del LED RGB va conectado a GND.
- Crear tres canales PWM.
- Configurar la frecuencia PWM a 1000 Hz.
- Trabajar con valores RGB entre 0 y 255.
- Convertir los valores RGB de 0-255 al rango de PWM de MicroPython 0-65535.
- Crear una función llamada `rueda_color(posicion)` que convierta un valor entre 0 y 255 en un color RGB.
- Crear una función llamada `aplicar_color(r, g, b)`.
- Recorrer los valores de 0 a 255 de forma continua.
- El LED RGB debe cambiar de color suavemente.
- El programa debe ejecutarse indefinidamente.
- El código debe ser claro, comentado y adecuado para alumnado principiante de Formación Profesional.

---

## 19. Resultado esperado

Al ejecutar el archivo `main.py` en el ESP32-S3 WROOM, el LED RGB debe cambiar suavemente de color siguiendo un degradado continuo.

El efecto debe ser más moderno y agradable que el cambio aleatorio de colores del proyecto 5.1.
