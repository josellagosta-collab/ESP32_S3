# Proyecto 11.1 – Termómetro con Termistor
## ESP32-S3 WROOM + MicroPython

---

# 1. Objetivo del proyecto

En este proyecto aprenderemos a utilizar un termistor NTC para medir temperatura mediante el ADC del ESP32-S3.

El sistema leerá continuamente el valor analógico generado por el divisor de tensión formado por:

- Termistor NTC.
- Resistencia de 10 kΩ.

Los datos se mostrarán en el monitor serie.

---

# 2. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| Resistencia 10 kΩ | 1 |
| Termistor NTC | 1 |
| Cables Dupont | 3 |

---

# 3. Objetivos de aprendizaje

- Comprender el funcionamiento de un termistor.
- Utilizar ADC en ESP32-S3.
- Construir un divisor de tensión.
- Medir temperatura indirectamente.
- Visualizar datos por monitor serie.

---

# 4. Fundamentos teóricos

## ¿Qué es un termistor?

Un termistor es una resistencia cuyo valor cambia con la temperatura.

### NTC

NTC significa:

Negative Temperature Coefficient

Cuando la temperatura aumenta:

- La resistencia disminuye.

Cuando la temperatura disminuye:

- La resistencia aumenta.

---

# 5. Divisor de tensión

```text
3.3V
 |
[NTC]
 |
 +------ GPIO2 (ADC)
 |
[10kΩ]
 |
GND
```

La tensión del punto central cambia según la temperatura.

---

# 6. Conexiones

| Elemento | Conexión |
|----------|----------|
| Termistor NTC | 3.3 V |
| Unión NTC + Resistencia | GPIO2 |
| Resistencia 10 kΩ | GND |

---

# 7. ADC del ESP32-S3

Rango habitual:

```text
0 → 4095
```

El ADC convierte la tensión medida en un número digital.

---

# 8. Funcionamiento esperado

1. Leer ADC.
2. Mostrar valor ADC.
3. Calcular temperatura aproximada.
4. Mostrar datos por serie.
5. Repetir continuamente.

---

# 9. Código básico

```python
from machine import Pin, ADC
import time

sensor = ADC(Pin(2))

while True:

    valor = sensor.read()

    print("ADC:", valor)

    time.sleep(1)
```

---

# 10. Código con temperatura aproximada

```python
from machine import Pin, ADC
import time

sensor = ADC(Pin(2))

while True:

    adc = sensor.read()

    temperatura = 50 - ((adc / 4095) * 50)

    print("ADC:", adc)
    print("Temperatura:", round(temperatura,1), "°C")

    time.sleep(1)
```

---

# 11. Versión con monitor serie mejorado

```python
from machine import Pin, ADC
import time

sensor = ADC(Pin(2))

while True:

    adc = sensor.read()

    temperatura = 50 - ((adc / 4095) * 50)

    print("--------------------")
    print("ADC:", adc)
    print("Temperatura:", round(temperatura,1), "°C")

    time.sleep(1)
```

---

# 12. Aplicaciones reales

- Termómetros digitales.
- Estaciones meteorológicas.
- Sistemas HVAC.
- Automatización industrial.
- Monitorización de baterías.
- Electrónica de potencia.

---

# 13. Errores frecuentes

## Siempre marca la misma temperatura

- Termistor mal conectado.
- ADC incorrecto.

## Valores muy inestables

- Conexiones flojas.
- Ruido eléctrico.

## ADC siempre a cero

- Cortocircuito.
- GPIO incorrecto.

---

# 14. Retos para el alumnado

### Nivel básico

Mostrar solo el valor ADC.

### Nivel medio

Mostrar temperatura estimada.

### Nivel avanzado

Encender un LED cuando la temperatura supere un umbral.

### Nivel experto

Registrar temperaturas en un fichero CSV.

---

# 15. Preguntas para el alumnado

1. ¿Qué es un termistor?
2. ¿Qué significa NTC?
3. ¿Cómo cambia la resistencia con la temperatura?
4. ¿Para qué sirve el ADC?
5. ¿Qué es un divisor de tensión?
6. ¿Dónde se utilizan los termistores?

---

# 16. Criterios de evaluación

| Criterio | Logrado | No logrado |
|-----------|----------|------------|
| Cablea correctamente el termistor | | |
| Configura correctamente el ADC | | |
| Lee valores analógicos | | |
| Interpreta la temperatura | | |
| Utiliza monitor serie | | |
| Código comentado | | |

---

# 17. Prompt optimizado para GitHub Copilot / Cursor

Genera un archivo main.py para ESP32-S3 WROOM usando MicroPython.

Requisitos:

- Utilizar ADC en GPIO2.
- Leer continuamente un termistor NTC conectado mediante divisor de tensión con una resistencia de 10 kΩ.
- Mostrar el valor ADC.
- Calcular una temperatura aproximada.
- Mostrar los datos por monitor serie.
- Incluir comentarios explicativos.

---

# 18. Resultado esperado

Al calentar el termistor con los dedos:

- El valor ADC cambiará.
- La temperatura estimada aumentará.

Al dejarlo enfriar:

- La temperatura disminuirá.

El sistema funcionará como un termómetro básico basado en un termistor NTC.
