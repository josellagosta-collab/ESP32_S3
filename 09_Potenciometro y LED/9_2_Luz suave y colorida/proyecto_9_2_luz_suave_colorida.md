# Proyecto 9.2 Luz Suave y Colorida - Parte 1

## Objetivo del proyecto
Controlar un LED RGB mediante tres potenciómetros usando ADC y PWM.

## Componentes
- ESP32-S3-WROOM
- GPIO Extension Board
- Protoboard
- 3 Potenciómetros 10k
- LED RGB
- 3 Resistencias 220Ω

## Conexiones

### LED RGB
- Rojo -> GPIO38
- Verde -> GPIO39
- Azul -> GPIO40

### Potenciómetros
- Rojo -> GPIO14
- Verde -> GPIO13
- Azul -> GPIO12

## Fundamentos RGB
La mezcla aditiva RGB permite generar millones de colores variando la intensidad de los canales Rojo, Verde y Azul.

## ADC del ESP32-S3
Rango de lectura: 0 a 4095.

## PWM
Rango duty_u16: 0 a 65535.

## Conversión ADC -> PWM

```python
pwm = int((adc / 4095) * 65535)
```

## Código base

```python
from machine import Pin, ADC, PWM
import time
```
## Monitor Serie
Mostrar valores ADC y PWM de cada color.

## Filtrado

```python
valor = (adc.read()+adc.read()+adc.read()) // 3
```

## Aplicaciones
- Domótica
- Gaming
- Iluminación RGB
- Robótica

## Errores frecuentes
- GPIO incorrecto
- LED RGB mal conectado
- Potenciómetros mal cableados

## Retos
- Mostrar porcentajes RGB.
- Crear colores predefinidos.
- Crear mezclas automáticas.

## Evaluación
- Configuración ADC.
- Configuración PWM.
- Control independiente RGB.

## Prompt Copilot

Genera un main.py para ESP32-S3 con:
- ADC en GPIO14, 13 y 12.
- PWM en GPIO38, 39 y 40.
- Conversión ADC->PWM.
- Control de LED RGB.
