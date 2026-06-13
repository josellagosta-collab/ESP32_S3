# Proyecto 10.1 – Lámpara Nocturna
## ESP32-S3 WROOM + MicroPython

---

# 1. Objetivo del proyecto

En este proyecto aprenderemos a utilizar una **fotorresistencia (LDR)** para medir la luz ambiental y controlar automáticamente el brillo de un LED.

Funcionamiento esperado:

- Cuando hay mucha luz ambiental, el LED disminuirá su brillo.
- Cuando hay poca luz ambiental, el LED aumentará su brillo.
- En completa oscuridad, el LED alcanzará su brillo máximo.

Este comportamiento es similar al de una lámpara nocturna automática.

---

# 2. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| Fotorresistencia (LDR) | 1 |
| Resistencia 10 kΩ | 1 |
| LED | 1 |
| Resistencia 220 Ω | 1 |
| Cables Dupont | 4 |

---

# 3. Objetivos de aprendizaje

1. Utilizar una fotorresistencia.
2. Leer valores analógicos mediante ADC.
3. Utilizar PWM para controlar un LED.
4. Construir un divisor de tensión.
5. Relacionar una entrada analógica con una salida PWM.
6. Diseñar sistemas automáticos sensibles a la luz.

---

# 4. Conexiones del circuito

Según el esquema proporcionado:

## LED

| Elemento | Conexión |
|----------|----------|
| GPIO 14 | Resistencia 220 Ω |
| Resistencia 220 Ω | Ánodo LED |
| Cátodo LED | GND |

## Fotorresistencia

| Elemento | Conexión |
|----------|----------|
| LDR | 3.3 V |
| Unión LDR + Resistencia 10 kΩ | GPIO 2 (ADC) |
| Resistencia 10 kΩ | GND |

---

# 5. Esquema ASCII

```text
                ESP32-S3

             GPIO14
                |
                |
             [220Ω]
                |
               LED
                |
               GND


3.3V
 |
[LDR]
 |
 +------ GPIO2 (ADC)
 |
[10kΩ]
 |
GND
```

---

# 6. ¿Qué es una fotorresistencia?

Una LDR (Light Dependent Resistor) es una resistencia cuyo valor cambia en función de la luz.

- Mucha luz → resistencia baja.
- Poca luz → resistencia alta.

---

# 7. Divisor de tensión

La LDR y la resistencia de 10 kΩ forman un divisor de tensión.

El ESP32-S3 mide la tensión del punto central mediante el ADC.

```text
3.3V
 |
[LDR]
 |
 +---- ADC
 |
[10k]
 |
GND
```

---

# 8. ADC del ESP32-S3

El ADC convierte una tensión analógica en un número.

Rango habitual:

```text
0 → 4095
```

---

# 9. PWM para controlar el LED

El brillo del LED se controla mediante:

```python
led.duty_u16(valor)
```

Rango:

```text
0 → apagado
65535 → brillo máximo
```

---

# 10. Lógica del proyecto

Queremos que:

```text
Más luz  → menos brillo

Menos luz → más brillo
```

Por tanto debemos invertir la lectura ADC.

---

# 11. Código de referencia

```python
from machine import Pin, ADC, PWM
import time

ldr = ADC(Pin(2))

led = PWM(Pin(14))
led.freq(1000)

while True:

    luz = ldr.read()

    brillo = 65535 - int((luz / 4095) * 65535)

    led.duty_u16(brillo)

    time.sleep_ms(50)
```

---

# 12. Versión con monitor serie

```python
from machine import Pin, ADC, PWM
import time

ldr = ADC(Pin(2))

led = PWM(Pin(14))
led.freq(1000)

while True:

    luz = ldr.read()

    brillo = 65535 - int((luz / 4095) * 65535)

    porcentaje = int((brillo / 65535) * 100)

    led.duty_u16(brillo)

    print(
        "ADC:", luz,
        "Brillo:", porcentaje, "%"
    )

    time.sleep(0.2)
```

---

# 13. Versión avanzada con filtrado

```python
lectura = (
    ldr.read()
    + ldr.read()
    + ldr.read()
) // 3
```

Esto reduce fluctuaciones.

---

# 14. Aplicaciones reales

- Luces nocturnas.
- Alumbrado automático.
- Domótica.
- Sensores crepusculares.
- Automatización industrial.
- Sistemas de ahorro energético.

---

# 15. Errores frecuentes

## El LED nunca se enciende

- GPIO incorrecto.
- LED invertido.
- Resistencia mal conectada.

## El LED siempre está al máximo

- ADC incorrecto.
- LDR mal conectada.

## El LED responde al revés

Invertir la fórmula:

```python
brillo = 65535 - valor_pwm
```

---

# 16. Retos para el alumnado

## Nivel básico

Mostrar el valor ADC.

## Nivel medio

Mostrar el porcentaje de brillo.

## Nivel avanzado

Encender el LED únicamente cuando la luz sea inferior a un umbral.

## Nivel experto

Controlar un LED RGB según el nivel de iluminación.

---

# 17. Preguntas para el alumnado

1. ¿Qué es una LDR?
2. ¿Cómo cambia su resistencia con la luz?
3. ¿Qué hace el ADC?
4. ¿Qué hace PWM?
5. ¿Por qué usamos un divisor de tensión?
6. ¿Por qué invertimos la lectura ADC?
7. ¿Qué aplicaciones tiene una lámpara nocturna automática?

---

# 18. Criterios de evaluación

| Criterio | Logrado | No logrado |
|----------|----------|------------|
| Cablea correctamente la LDR | | |
| Configura correctamente el ADC | | |
| Configura correctamente el PWM | | |
| Controla automáticamente el brillo | | |
| Comprende el divisor de tensión | | |
| Código comentado | | |

---

# 19. Prompt optimizado para GitHub Copilot / Cursor

Genera un archivo main.py para una placa ESP32-S3 WROOM usando MicroPython.

Conexiones:

- LDR conectada a GPIO2 mediante ADC.
- LED conectado a GPIO14 mediante PWM.
- Frecuencia PWM de 1000 Hz.

Requisitos:

- Leer continuamente la LDR.
- Convertir la lectura ADC en brillo PWM.
- Invertir la lectura para que el LED brille más cuando haya menos luz.
- Mostrar opcionalmente los valores por monitor serie.
- Incluir comentarios explicativos.

---

# 20. Resultado esperado

Al tapar la fotorresistencia:

- El LED aumenta progresivamente su brillo.

Al iluminar la fotorresistencia:

- El LED disminuye progresivamente su brillo.

El sistema se comportará como una lámpara nocturna automática.
