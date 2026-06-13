# Proyecto 20.1 – Modo Estación WiFi (STA)

## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# 1. Introducción

Hasta ahora hemos trabajado con sensores, actuadores y comunicaciones locales.

En este capítulo aprenderemos a conectar el ESP32-S3 a una red WiFi existente.

Este modo se denomina:

```text
STA
```

abreviatura de:

```text
Station Mode
```

o

```text
Modo Estación
```

---

# 2. Objetivos

Al finalizar esta práctica el alumno será capaz de:

- Comprender el funcionamiento del WiFi en ESP32.
- Conectarse a una red inalámbrica existente.
- Obtener una dirección IP.
- Verificar la conectividad.
- Preparar el ESP32 para aplicaciones IoT.

---

# 3. ¿Qué es el modo STA?

En modo estación el ESP32 actúa como un cliente WiFi.

Es exactamente igual que:

- Un ordenador portátil.
- Un teléfono móvil.
- Una Smart TV.

Arquitectura:

```text
Router WiFi
      ↓
 ESP32-S3
```

---

# 4. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| Cable USB-C | 1 |
| Router WiFi | 1 |

---

# 5. Esquema de funcionamiento

```text
        INTERNET
            │
            │
     ┌────────────┐
     │ Router WiFi│
     └────────────┘
            │
            │
      ESP32-S3
```

---

# 6. Librería WiFi

MicroPython incorpora:

```python
import network
```

---

# 7. Activación del interfaz WiFi

```python
import network

wlan = network.WLAN(network.STA_IF)

wlan.active(True)
```

---

# 8. Conexión a la red

```python
SSID = "MiWiFi"
PASSWORD = "12345678"

wlan.connect(
    SSID,
    PASSWORD
)
```

---

# 9. Esperar conexión

```python
while not wlan.isconnected():
    pass
```

---

# 10. Obtener dirección IP

```python
print(wlan.ifconfig())
```

Ejemplo:

```text
('192.168.1.45',
 '255.255.255.0',
 '192.168.1.1',
 '8.8.8.8')
```

---

# 11. Código completo

```python
import network
import time

ssid = "MiWiFi"
password = "12345678"

wlan = network.WLAN(
    network.STA_IF
)

wlan.active(True)

wlan.connect(
    ssid,
    password
)

while not wlan.isconnected():

    time.sleep(1)

print(
    "Conectado"
)

print(
    wlan.ifconfig()
)
```

---

# 12. Resultado esperado

Terminal:

```text
Conectado

IP:
192.168.1.45
```

---

# 13. Aplicaciones reales

- MQTT
- Node-RED
- Servidores Web
- IoT Industrial
- Domótica

---

# 14. Errores frecuentes

## No conecta

Comprobar:

- SSID correcto.
- Contraseña correcta.

---

## IP = 0.0.0.0

No se ha conectado correctamente.

---

# 15. Actividades

### Básico

Conectarse a WiFi.

### Medio

Mostrar IP.

### Avanzado

Hacer ping a un servidor.

### Experto

Publicar datos MQTT.

---

# 16. Preguntas tipo examen

1. ¿Qué significa STA?
2. ¿Qué hace wlan.connect()?
3. ¿Qué devuelve ifconfig()?
4. ¿Qué es una dirección IP?
5. ¿Qué aplicaciones IoT utilizan STA?

---

# 17. Prompt GitHub Copilot

A partir la la especificaciones .md de este proyecto genera un programa MicroPython para ESP32-S3.

Requisitos:

- Conectar a WiFi.
- Mostrar IP.
- Gestionar errores.
- Reconectar automáticamente.