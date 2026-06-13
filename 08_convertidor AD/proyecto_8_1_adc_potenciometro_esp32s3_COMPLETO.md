# Proyecto 8.1 – Lectura del voltaje del potenciómetro
## ESP32-S3 WROOM + MicroPython

# 1. Objetivo del proyecto
Aprender a utilizar el convertidor analógico-digital (ADC) integrado en el ESP32-S3 para medir una tensión variable procedente de un potenciómetro.

El ESP32-S3 leerá continuamente:
- Valor ADC bruto.
- Porcentaje de recorrido.
- Voltaje aproximado.
- Información de diagnóstico.

# 2. Descripción general
Un potenciómetro funciona como un divisor de tensión. Al girarlo obtenemos una tensión variable entre 0 V y 3.3 V que será convertida por el ADC en un valor digital.

# 3. Componentes necesarios
| Componente | Cantidad |
|-----------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| Potenciómetro 10 kΩ | 1 |
| Cable Dupont | 3 |

# 4. Tabla de conexiones
| Terminal del potenciómetro | Conexión |
|---------------------------|----------|
| Extremo izquierdo | 3.3 V |
| Terminal central (cursor) | GPIO 2 |
| Extremo derecho | GND |

# 5. Esquema ASCII
```text
                ESP32-S3

               +---------+
3.3V ----------|         |
               |         |
GPIO2 ---------|  ADC    |
               |         |
GND -----------|         |
               +---------+

3.3V ----/\/\/\/\/\/\/\/\---- GND
                    |
                    |
                 GPIO2
```

# 6. ¿Qué es un ADC?
ADC significa Analog to Digital Converter (Convertidor Analógico Digital).
Transforma una tensión eléctrica en un valor numérico.

# 7. Resolución del ADC
El ESP32-S3 trabaja normalmente con 12 bits.

2^12 = 4096 niveles

Rango:
- 0 → 0 V
- 4095 → 3.3 V

# 8. Funcionamiento esperado
1. Configurar GPIO2 como ADC.
2. Leer continuamente el valor analógico.
3. Mostrar valor ADC.
4. Calcular porcentaje.
5. Calcular voltaje.
6. Mostrar resultados por serie.

# 9. Código de referencia esperado
```python
from machine import Pin, ADC
import time

pot = ADC(Pin(2))

while True:

    valor_adc = pot.read()

    porcentaje = (valor_adc / 4095) * 100

    voltaje = (valor_adc / 4095) * 3.3

    print("---------------------")
    print("ADC:", valor_adc)
    print("Porcentaje:", round(porcentaje, 1), "%")
    print("Voltaje:", round(voltaje, 2), "V")

    time.sleep(0.5)
```

# 10. Explicación línea por línea
- ADC(Pin(2)): configura el GPIO2 como entrada analógica.
- read(): obtiene un valor entre 0 y 4095.
- Conversión a porcentaje.
- Conversión a voltaje.
- Visualización por monitor serie.

# 11. Versión mejorada con barra gráfica
```python
from machine import Pin, ADC
import time

pot = ADC(Pin(2))

while True:
    valor = pot.read()
    porcentaje = int((valor / 4095) * 100)
    barras = int(porcentaje / 5)

    print("[" + "#" * barras + "-" * (20 - barras) + "]", porcentaje, "%")

    time.sleep(0.2)
```

# 12. Aplicaciones reales
- Potenciómetros
- Joysticks
- Sensores de luz
- Sensores de temperatura
- Sensores de presión
- Instrumentación electrónica

# 13. Errores frecuentes
## El valor siempre es 0
- Potenciómetro mal cableado.
- Cursor no conectado.

## El valor siempre es máximo
- Cursor conectado a 3.3 V.

## Los valores saltan mucho
- Potenciómetro defectuoso.
- Conexiones flojas.

# 14. Retos para el alumnado
### Nivel básico
Mostrar únicamente el porcentaje.

### Nivel medio
Mostrar únicamente el voltaje.

### Nivel avanzado
Controlar el brillo de un LED mediante PWM.

### Nivel experto
Controlar un LED RGB utilizando varios potenciómetros.

# 15. Preguntas para el alumnado
1. ¿Qué significa ADC?
2. ¿Qué hace un ADC?
3. ¿Por qué el potenciómetro genera una señal analógica?
4. ¿Qué resolución utiliza el ESP32-S3?
5. ¿Qué valor ADC corresponde a 1.65 V aproximadamente?

# 16. Criterios de evaluación
| Criterio | Logrado | No logrado |
|----------|---------|------------|
| Cablea correctamente el potenciómetro | | |
| Configura correctamente el ADC | | |
| Lee valores analógicos | | |
| Calcula porcentaje | | |
| Calcula voltaje | | |
| Muestra datos por serie | | |

# 17. Prompt optimizado para GitHub Copilot / Cursor
Genera un archivo main.py para una placa ESP32-S3 WROOM utilizando MicroPython.

Requisitos:
- Utilizar ADC en GPIO 2.
- Leer continuamente el valor analógico.
- Mostrar el valor ADC.
- Calcular el porcentaje.
- Calcular el voltaje aproximado.
- Mostrar la información por monitor serie.
- Actualizar cada 500 ms.
- Incluir comentarios explicativos.
- Generar una segunda versión con barra gráfica ASCII.

# 18. Resultado esperado
Al girar el potenciómetro:

ADC: 2048
Porcentaje: 50.0 %
Voltaje: 1.65 V

Los valores deben cambiar suavemente a medida que se gira el mando.
