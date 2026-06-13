# Proyecto 20.3 – Modo AP + STA

## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# 1. Introducción

Este es el modo más potente del ESP32-S3.

Permite funcionar simultáneamente como:

```text
Cliente WiFi
```

y

```text
Punto de Acceso
```

al mismo tiempo.

---

# 2. Objetivos

- Utilizar AP y STA simultáneamente.
- Conectarse a Internet.
- Crear una red propia.
- Comprender arquitecturas IoT avanzadas.

---

# 3. Arquitectura

```text
         Router WiFi
              │
              │
          ESP32-S3
         AP + STA
              │
              │
       Smartphone
```

---

# 4. Ventajas

- Acceso a Internet.
- Acceso local.
- Configuración remota.
- Gran flexibilidad.

---

# 5. Activar STA

```python
sta = network.WLAN(
    network.STA_IF
)

sta.active(True)
```

---

# 6. Activar AP

```python
ap = network.WLAN(
    network.AP_IF
)

ap.active(True)
```

---

# 7. Configurar AP

```python
ap.config(
    essid="ESP32_AP"
)
```

---

# 8. Conectar STA

```python
sta.connect(
    "MiWiFi",
    "12345678"
)
```

---

# 9. Código completo

```python
import network

sta = network.WLAN(
    network.STA_IF
)

ap = network.WLAN(
    network.AP_IF
)

sta.active(True)
ap.active(True)

sta.connect(
    "MiWiFi",
    "12345678"
)

ap.config(
    essid="ESP32_AP"
)

print(
    "STA:",
    sta.ifconfig()
)

print(
    "AP:",
    ap.ifconfig()
)
```

---

# 10. Resultado esperado

```text
STA:
192.168.1.45

AP:
192.168.4.1
```

---

# 11. Aplicaciones industriales

- Gateways IoT.
- Edge Computing.
- Robots colaborativos.
- Sistemas de monitorización.

---

# 12. Aplicaciones educativas

- Servidor Web.
- MQTT.
- Node-RED.
- Wazuh.
- Grafana.

---

# 13. Errores frecuentes

## STA funciona pero AP no

Comprobar:

```python
ap.active(True)
```

---

## AP funciona pero STA no

Comprobar:

- SSID.
- Contraseña.
- Cobertura.

---

# 14. Actividades

### Básico

Configurar AP+STA.

### Medio

Mostrar ambas IP.

### Avanzado

Servidor web.

### Experto

Gateway MQTT.

---

# 15. Preguntas tipo examen

1. ¿Qué es AP+STA?
2. ¿Qué ventajas tiene?
3. ¿Cuántas IP puede tener el ESP32?
4. ¿Qué es un gateway IoT?
5. ¿Qué aplicaciones industriales existen?

---

# 16. Prompt GitHub Copilot

A partir la la especificaciones .md de este proyecto genera un programa MicroPython para ESP32-S3.

Requisitos:

- Conectar a WiFi.
- Mostrar IP.
- Gestionar errores.
- Reconectar automáticamente.

Requisitos:

- Activar STA y AP simultáneamente.
- Conectar a WiFi.
- Crear punto de acceso.
- Mostrar ambas IP.
- Gestionar errores.
- Reconectar automáticamente.