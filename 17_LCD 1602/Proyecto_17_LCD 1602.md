# Proyecto 17.1 – LCD1602 I2C
## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# Índice

1. Introducción
2. Objetivos
3. Componentes necesarios
4. ¿Qué es una pantalla LCD1602?
5. Funcionamiento interno
6. Comunicación I2C
7. Ventajas del módulo I2C
8. Conexiones del proyecto
9. Tabla completa de conexiones
10. Esquema ASCII
11. Direcciones I2C
12. Escaneo del bus I2C
13. Librería I2C_LCD
14. Código completo
15. Explicación línea por línea
16. Posicionamiento del cursor
17. Escritura de texto
18. Contador automático
19. Caracteres personalizados
20. Aplicaciones reales
21. Errores frecuentes
22. Actividades para alumnado
23. Preguntas tipo examen
24. Rúbrica de evaluación
25. Prompt para GitHub Copilot

---

# 1. Introducción

En este proyecto aprenderemos a utilizar una pantalla LCD1602 con interfaz I2C para mostrar información generada por un ESP32-S3.

Las pantallas LCD1602 son extremadamente populares en:

- Robótica.
- Automatización.
- Domótica.
- Instrumentación.
- Sistemas embebidos.

Gracias al adaptador I2C solamente necesitaremos dos GPIO para controlarla.

---

# 2. Objetivos del proyecto

Al finalizar esta práctica el alumno será capaz de:

- Comprender el funcionamiento de una pantalla LCD1602.
- Utilizar el protocolo I2C.
- Detectar dispositivos I2C conectados.
- Mostrar texto en una pantalla LCD.
- Posicionar el cursor.
- Actualizar información dinámicamente.
- Crear interfaces básicas de usuario.

---

# 3. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| GPIO Extension Board | 1 |
| Protoboard 830 puntos | 1 |
| LCD1602 I2C | 1 |
| Cable Dupont hembra-macho | 4 |

---

# 4. ¿Qué es una pantalla LCD1602?

LCD significa:

```text
Liquid Crystal Display
```

La denominación 1602 indica:

```text
16 columnas
2 filas
```

Por tanto puede mostrar:

```text
16 caracteres × 2 líneas
```

Total:

```text
32 caracteres
```

---

# 5. Aspecto de la pantalla

```text
+----------------+
|                |
|                |
+----------------+
```

Cada línea admite:

```text
16 caracteres
```

---

# 6. Funcionamiento interno

Internamente la LCD1602 utiliza un controlador HD44780 o compatible.

Este controlador:

- Gestiona los caracteres.
- Controla el cursor.
- Gestiona la memoria de pantalla.
- Permite caracteres personalizados.

---

# 7. ¿Qué es I2C?

I2C significa:

```text
Inter-Integrated Circuit
```

Es un protocolo de comunicación serie muy utilizado.

Sólo necesita:

```text
SDA
SCL
```

---

# 8. Ventajas del módulo I2C

Sin adaptador I2C:

```text
6 a 10 GPIO
```

Con adaptador I2C:

```text
2 GPIO
```

Ventajas:

- Menos cableado.
- Más GPIO libres.
- Montaje más sencillo.

---

# 9. Conexiones del proyecto

Según la imagen proporcionada:

| LCD1602 I2C | ESP32-S3 |
|------------|-----------|
| GND | GND |
| VCC | 5V |
| SDA | GPIO14 |
| SCL | GPIO13 |

---

# 10. Tabla detallada de conexiones

| Pin LCD | Función | ESP32 |
|----------|----------|--------|
| GND | Tierra | GND |
| VCC | Alimentación | 5V |
| SDA | Datos I2C | GPIO14 |
| SCL | Reloj I2C | GPIO13 |

---

# 11. Esquema ASCII

```text
                ESP32-S3

                GPIO13
                   |
                   |
                   +------ SCL

                GPIO14
                   |
                   |
                   +------ SDA

                GND
                   |
                   |
                   +------ GND

                 5V
                   |
                   |
                   +------ VCC


                LCD1602 I2C
```

---

# 12. Dirección I2C

Cada dispositivo I2C tiene una dirección única.

Las más habituales son:

```text
0x27
```

o

```text
0x3F
```

Por este motivo el programa realiza primero un escaneo.

---

# 13. Escaneo del bus I2C

Código:

```python
devices = i2c.scan()
```

Permite localizar todos los dispositivos conectados.

---

# 14. Código completo del proyecto

```python
import time
from machine import I2C, Pin
from I2C_LCD import I2cLcd

i2c = I2C(
    scl=Pin(13),
    sda=Pin(14),
    freq=400000
)

devices = i2c.scan()

if len(devices) == 0:

    print("No i2c device !")

else:

    for device in devices:

        print(
            "I2C addr:",
            hex(device)
        )

        lcd = I2cLcd(
            i2c,
            device,
            2,
            16
        )

try:

    lcd.move_to(0,0)

    lcd.putstr("Hello,world!")

    count = 0

    while True:

        lcd.move_to(0,1)

        lcd.putstr(
            "Counter:%d" %(count)
        )

        time.sleep_ms(1000)

        count += 1

except:

    pass
```

---

# 15. Explicación línea por línea

## Importar librerías

```python
import time
```

Gestiona tiempos.

---

```python
from machine import I2C, Pin
```

Control del bus I2C.

---

```python
from I2C_LCD import I2cLcd
```

Control de la pantalla.

---

# 16. Crear bus I2C

```python
i2c = I2C(
    scl=Pin(13),
    sda=Pin(14),
    freq=400000
)
```

Configura:

| Parámetro | Valor |
|------------|--------|
| SDA | GPIO14 |
| SCL | GPIO13 |
| Frecuencia | 400 kHz |

---

# 17. Buscar dispositivos

```python
devices = i2c.scan()
```

Ejemplo de salida:

```text
I2C addr: 0x27
```

---

# 18. Inicializar LCD

```python
lcd = I2cLcd(
    i2c,
    device,
    2,
    16
)
```

Parámetros:

| Parámetro | Significado |
|------------|-------------|
| i2c | Bus |
| device | Dirección |
| 2 | Filas |
| 16 | Columnas |

---

# 19. Posicionar cursor

```python
lcd.move_to(0,0)
```

Posición:

```text
Columna 0
Fila 0
```

---

# 20. Escribir texto

```python
lcd.putstr(
    "Hello,world!"
)
```

Resultado:

```text
Hello,world!
```

---

# 21. Crear contador

```python
count = 0
```

---

# 22. Mostrar contador

```python
lcd.move_to(0,1)

lcd.putstr(
    "Counter:%d" %(count)
)
```

Ejemplo:

```text
Counter:15
```

---

# 23. Actualización cada segundo

```python
time.sleep_ms(1000)
```

---

# 24. Resultado esperado

Pantalla:

```text
Hello,world!

Counter:0
```

Después:

```text
Hello,world!

Counter:1
```

Y así sucesivamente.

---

# 25. Mejoras posibles

Mostrar:

- Temperatura.
- Hora.
- Dirección IP.
- Datos MQTT.
- Estado de sensores.

---

# 26. Ejemplo: Mostrar temperatura

```python
lcd.move_to(0,0)

lcd.putstr(
    "Temp:24.5C"
)
```

---

# 27. Ejemplo: Mostrar IP

```python
lcd.putstr(
    "192.168.1.50"
)
```

---

# 28. Aplicaciones reales

- Termómetros.
- Estaciones meteorológicas.
- Robots.
- Cuadros de mando.
- Domótica.
- Automatización industrial.

---

# 29. Errores frecuentes

## Pantalla en blanco

Posibles causas:

- Dirección I2C incorrecta.
- SDA/SCL invertidos.

---

## No encuentra dispositivos

Posibles causas:

- Cableado incorrecto.
- Alimentación ausente.

---

## Caracteres extraños

Posibles causas:

- Librería incorrecta.
- Frecuencia I2C inadecuada.

---

# 30. Actividades para alumnado

## Nivel básico

Mostrar:

```text
Hola Mundo
```

---

## Nivel medio

Mostrar contador.

---

## Nivel avanzado

Mostrar ADC de un potenciómetro.

---

## Nivel experto

Mostrar datos MQTT recibidos desde Node-RED.

---

# 31. Preguntas tipo examen

1. ¿Qué significa LCD1602?
2. ¿Qué es I2C?
3. ¿Cuántos cables utiliza I2C?
4. ¿Qué función realiza SDA?
5. ¿Qué función realiza SCL?
6. ¿Qué hace i2c.scan()?
7. ¿Qué hace lcd.putstr()?
8. ¿Qué hace lcd.move_to()?
9. ¿Qué direcciones I2C suelen utilizar estas pantallas?
10. ¿Qué ventajas tiene I2C?

---

# 32. Rúbrica de evaluación

| Criterio | Logrado | No logrado |
|-----------|----------|------------|
| Cableado correcto | | |
| Detección I2C | | |
| Inicialización LCD | | |
| Mostrar texto | | |
| Actualización dinámica | | |
| Código comentado | | |

---

# 33. Prompt optimizado para GitHub Copilot

A partir la las espicidficaciones del archivo .md de este proyecto genera un programa MicroPython para ESP32-S3.

Conexiones:

- SDA → GPIO14
- SCL → GPIO13

Pantalla:

- LCD1602 I2C
- 16 columnas
- 2 filas

Requisitos:

- Escanear dispositivos I2C.
- Detectar automáticamente la dirección.
- Mostrar "Hello World".
- Mostrar un contador creciente.
- Actualizar cada segundo.
- Comentar el código.
- Gestionar errores de comunicación.

---

# 34. Conclusiones

Este proyecto introduce uno de los periféricos más utilizados en sistemas embebidos:

```text
LCD1602 + I2C
```

Gracias a él podemos mostrar información generada por el ESP32-S3 utilizando únicamente dos GPIO.

Los conocimientos adquiridos serán fundamentales para proyectos posteriores de:

- IoT.
- Robótica.
- Automatización.
- Monitorización industrial.