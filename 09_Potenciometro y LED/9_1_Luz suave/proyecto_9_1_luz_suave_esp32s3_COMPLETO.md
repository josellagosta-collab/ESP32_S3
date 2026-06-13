# Proyecto 9.1 – Luz Suave
## ESP32-S3 WROOM + MicroPython

---

# 1. Objetivo del proyecto

En los capítulos anteriores hemos aprendido dos conceptos fundamentales del ESP32-S3:

- ADC (Analog to Digital Converter)
- PWM (Pulse Width Modulation)

En este proyecto combinaremos ambas tecnologías para construir una luz suave regulable.

El ESP32-S3 leerá la posición de un potenciómetro mediante una entrada ADC y utilizará esa lectura para generar una señal PWM que controlará el brillo de un LED.

Al girar el potenciómetro:

- Hacia la izquierda → LED apagado.
- Posición central → brillo medio.
- Hacia la derecha → brillo máximo.

---

# 2. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| Potenciómetro 10 kΩ | 1 |
| LED rojo | 1 |
| Resistencia 220 Ω | 1 |
| Cables Dupont | 5 |

---

# 3. Objetivos de aprendizaje

1. Utilizar entradas ADC.
2. Utilizar salidas PWM.
3. Leer valores analógicos.
4. Convertir lecturas ADC en señales PWM.
5. Controlar el brillo de un LED.
6. Comprender la relación entre sensores y actuadores.

---

# 4. Tabla de conexiones

## Potenciómetro

| Terminal | Conexión |
|-----------|----------|
| Extremo izquierdo | 3.3 V |
| Terminal central | GPIO 2 |
| Extremo derecho | GND |

## LED

| Terminal | Conexión |
|-----------|----------|
| Ánodo (+) | GPIO 1 |
| Cátodo (-) | Resistencia 220 Ω |
| Resistencia | GND |

---

# 5. Esquema ASCII

```text
                 ESP32-S3

                +---------+
                |         |
GPIO 1 ---------| PWM     |
                |         |
GPIO 2 ---------| ADC     |
                |         |
3.3V -----------|         |
                |         |
GND ------------|         |
                +---------+

GPIO1 ----->|----[220Ω]---- GND

3.3V ----/\/\/\/\/\/\/\/\---- GND
                    |
                    |
                 GPIO2
```

---

# 6. Fundamento teórico

## ADC

Convierte una tensión analógica en un número digital.

Rango:

- 0 V → 0
- 3.3 V → 4095

## PWM

Controla el brillo del LED mediante:

```python
led.duty_u16(valor)
```

Rango:

- 0 → apagado
- 65535 → brillo máximo

---

# 7. Conversión ADC → PWM

```python
brillo = int((valor_adc / 4095) * 65535)
```

---

# 8. Código de referencia

```python
from machine import Pin, ADC, PWM
import time

pot = ADC(Pin(2))

led = PWM(Pin(1))
led.freq(1000)

while True:

    valor_adc = pot.read()

    brillo = int((valor_adc / 4095) * 65535)

    led.duty_u16(brillo)

    time.sleep_ms(20)
```

---

# 9. Versión con monitor serie

```python
from machine import Pin, ADC, PWM
import time

pot = ADC(Pin(2))

led = PWM(Pin(1))
led.freq(1000)

while True:

    valor_adc = pot.read()

    brillo = int((valor_adc / 4095) * 65535)

    porcentaje = (valor_adc / 4095) * 100

    led.duty_u16(brillo)

    print(
        "ADC:", valor_adc,
        "PWM:", brillo,
        "Brillo:", round(porcentaje,1), "%"
    )

    time.sleep(0.2)
```

---

# 10. Aplicaciones reales

- Reguladores de intensidad luminosa.
- Domótica.
- Control de motores.
- Robótica.
- Instrumentación electrónica.

---

# 11. Errores frecuentes

## El LED no se enciende

- LED invertido.
- GPIO incorrecto.
- Resistencia mal conectada.

## El LED siempre está encendido

- Potenciómetro mal cableado.
- Cursor conectado a 3.3 V.

## El brillo cambia a saltos

- Lecturas ADC inestables.
- Potenciómetro defectuoso.

---

# 12. Retos para el alumnado

### Nivel básico

Mostrar el porcentaje de brillo.

### Nivel medio

Mostrar ADC y PWM simultáneamente.

### Nivel avanzado

Controlar una barra LED.

### Nivel experto

Controlar un LED RGB usando tres potenciómetros.

---

# 13. Preguntas para el alumnado

1. ¿Qué es un ADC?
2. ¿Qué es PWM?
3. ¿Por qué se convierte ADC a PWM?
4. ¿Cuál es el rango del ADC?
5. ¿Cuál es el rango del PWM?

---

# 14. Criterios de evaluación

| Criterio | Logrado | No logrado |
|-----------|----------|------------|
| Cablea correctamente el potenciómetro | | |
| Cablea correctamente el LED | | |
| Configura ADC correctamente | | |
| Configura PWM correctamente | | |
| Controla el brillo del LED | | |

---

# 15. Prompt optimizado para GitHub Copilot / Cursor

Genera un archivo main.py para una placa ESP32-S3 WROOM utilizando MicroPython.

Conexiones:

- Potenciómetro en GPIO 2 mediante ADC.
- LED en GPIO 1 mediante PWM.
- Frecuencia PWM 1000 Hz.

Requisitos:

- Leer continuamente el ADC.
- Convertir 0-4095 a 0-65535.
- Aplicar PWM al LED.
- Mostrar ADC, PWM y porcentaje por monitor serie.
- Incluir comentarios explicativos.

---

# 16. Resultado esperado

Al girar el potenciómetro, el LED debe variar suavemente su brillo desde apagado hasta brillo máximo.
