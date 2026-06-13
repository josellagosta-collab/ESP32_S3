
# Proyecto 16.1 – Barrido con Servomotor
## Manual Didáctico Completo para ESP32-S3 y MicroPython

# Índice

1. Introducción
2. Objetivos
3. Componentes
4. Teoría de los servomotores
5. Anatomía interna
6. PWM aplicado a servos
7. Relación pulso-ángulo
8. Conexiones detalladas
9. Esquema ASCII
10. Alimentación y seguridad
11. Programación básica
12. Explicación línea a línea
13. Barrido simple
14. Barrido continuo
15. Monitor serie
16. duty() vs duty_u16()
17. Barrido profesional
18. Control de velocidad
19. Posiciones fijas
20. Servo tipo radar
21. Servo tipo barrera
22. Servo tipo brazo robótico
23. Aplicaciones reales
24. Errores frecuentes
25. Resolución de problemas
26. Actividades para alumnado
27. Preguntas tipo examen
28. Respuestas correctas
29. Rúbrica de evaluación
30. Prompt GitHub Copilot

---

# 1. Introducción

Los servomotores son actuadores capaces de posicionarse en un ángulo concreto.

A diferencia de los motores DC tradicionales, los servos permiten controlar:

- Posición
- Velocidad aparente
- Movimiento preciso

Son uno de los elementos fundamentales en robótica educativa e industrial.

---

# 2. Objetivos

Al finalizar este proyecto el alumno será capaz de:

- Comprender el funcionamiento de un servomotor.
- Configurar PWM en MicroPython.
- Posicionar un servo en un ángulo determinado.
- Implementar barridos automáticos.
- Desarrollar aplicaciones robóticas básicas.

---

# 3. Componentes

| Componente | Cantidad |
|------------|-----------|
| ESP32-S3-WROOM | 1 |
| Servo SG90 o compatible | 1 |
| Protoboard | 1 |
| Cables Dupont | 3 |

---

# 4. Teoría de los servomotores

Un servomotor integra:

- Motor DC.
- Reductora mecánica.
- Potenciómetro.
- Electrónica de control.

La electrónica compara constantemente la posición deseada con la posición real.

Esto se conoce como:

Control en lazo cerrado.

---

# 5. Anatomía interna

Motor → Reductora → Eje → Potenciómetro → Controlador

El controlador corrige continuamente la posición.

---

# 6. PWM aplicado a servos

Frecuencia estándar:

50 Hz

Periodo:

20 ms

Los servos interpretan la anchura del pulso para determinar la posición.

---

# 7. Relación pulso-ángulo

0.5 ms → 0°

1.5 ms → 90°

2.5 ms → 180°

---

# 8. Conexiones detalladas

| Servo | ESP32 |
|---------|---------|
| VCC | 3.3V |
| GND | GND |
| SIGNAL | GPIO1 |

---

# 9. Esquema ASCII

ESP32 GPIO1 -------- Servo Signal

ESP32 3.3V -------- Servo VCC

ESP32 GND -------- Servo GND

---

# 10. Alimentación y seguridad

Para pruebas educativas:

3.3V puede funcionar con SG90.

Para aplicaciones reales:

Usar fuente externa de 5V.

Siempre compartir GND.

---

# 11. Programación básica

```python
from machine import Pin, PWM
import time

servo = PWM(Pin(1))
servo.freq(50)
```

---

# 12. Función move_servo()

```python
def move_servo(angle):

    duty = int(angle / 180 * 100 + 25)

    servo.duty(duty)
```

---

# 13. Barrido simple

```python
for angle in range(0,181,2):

    move_servo(angle)
```

---

# 14. Barrido continuo

```python
while True:

    for angle in range(0,181,2):

        move_servo(angle)

    for angle in range(180,-1,-2):

        move_servo(angle)
```

---

# 15. Monitor serie

```python
print(angle)
```

---

# 16. duty() vs duty_u16()

Versiones modernas de MicroPython:

```python
servo.duty_u16(valor)
```

Mayor precisión.

---

# 17. Barrido profesional

Movimientos suaves:

```python
time.sleep_ms(10)
```

---

# 18. Control de velocidad

Más retardo:

Movimiento lento.

Menos retardo:

Movimiento rápido.

---

# 19. Posiciones fijas

0°

45°

90°

135°

180°

---

# 20. Servo tipo radar

Movimiento continuo de exploración.

Aplicación:

Sensores ultrasónicos.

---

# 21. Servo tipo barrera

Abrir:

0° → 90°

Cerrar:

90° → 0°

---

# 22. Servo tipo brazo robótico

Control de articulaciones.

Pick & Place.

---

# 23. Aplicaciones reales

- Robótica.
- Automatización.
- Drones.
- Cámaras PTZ.
- Domótica.

---

# 24. Errores frecuentes

Servo vibra.

Servo no gira.

Servo gira poco.

ESP32 se reinicia.

---

# 25. Resolución de problemas

Verificar:

- Alimentación.
- PWM.
- GND común.
- Cableado.

---

# 26. Actividades para alumnado

Nivel básico:

Mover servo entre 0° y 180°.

Nivel medio:

Añadir posiciones intermedias.

Nivel avanzado:

Control con potenciómetro.

Nivel experto:

Control mediante joystick.

---

# 27. Preguntas tipo examen

1. ¿Qué es un servomotor?
2. ¿Qué frecuencia utiliza?
3. ¿Qué diferencia tiene con un motor DC?
4. ¿Qué es PWM?
5. ¿Para qué sirve duty?

---

# 28. Respuestas

50 Hz.

Control de posición.

PWM.

etc.

---

# 29. Rúbrica

| Criterio | Sí | No |
|-----------|----|----|
| Conecta correctamente | | |
| Configura PWM | | |
| Realiza barrido | | |
| Comprende servo | | |

---

# 30. Prompt para GitHub Copilot

A partir de las especificaciones del archivo .md de este proyecto genera un proyecto MicroPython para ESP32-S3.

GPIO1 controla un servomotor.

Implementa:

- PWM a 50 Hz.
- Función move_servo().
- Barrido 0° → 180° → 0°.
- Comentarios explicativos.
- Versión usando duty_u16().

---

# Código completo final

```python
from machine import Pin, PWM
import time

servo = PWM(Pin(1))
servo.freq(50)

def move_servo(angle):

    duty = int(angle / 180 * 100 + 25)

    servo.duty(duty)

while True:

    for angle in range(0,181,2):

        move_servo(angle)

        time.sleep_ms(20)

    for angle in range(180,-1,-2):

        move_servo(angle)

        time.sleep_ms(20)
```

