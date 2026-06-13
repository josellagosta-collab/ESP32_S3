# Proyecto 20.2 – Modo Punto de Acceso (AP)

## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# 1. Introducción

En este proyecto el ESP32-S3 dejará de ser un cliente WiFi.

Ahora se convertirá en un:

```text
Access Point
```

o

```text
Punto de Acceso WiFi
```

Es decir:

```text
ESP32 crea su propia red WiFi
```

---

# 2. Objetivos

- Crear una red WiFi propia.
- Permitir conexiones de dispositivos externos.
- Configurar SSID y contraseña.
- Comprender el modo AP.

---

# 3. Arquitectura

```text
 Smartphone
      │
      │
 Portátil
      │
      │
  ESP32-S3
   (AP)
```

---

# 4. Componentes

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| Cable USB-C | 1 |

---

# 5. Activar modo AP

```python
import network

ap = network.WLAN(
    network.AP_IF
)

ap.active(True)
```

---

# 6. Configurar SSID

```python
ap.config(
    essid="ESP32_AP"
)
```

---

# 7. Configurar contraseña

```python
ap.config(
    password="12345678"
)
```

---

# 8. Obtener IP

```python
print(
    ap.ifconfig()
)
```

---

# 9. Código completo

```python
import network

ap = network.WLAN(
    network.AP_IF
)

ap.active(True)

ap.config(
    essid="ESP32_AP",
    password="12345678"
)

print(
    ap.ifconfig()
)
```

---

# 10. Resultado esperado

Desde el móvil aparecerá:

```text
ESP32_AP
```

---

# 11. Aplicaciones reales

- Configuración inicial de dispositivos.
- Equipos IoT.
- Sensores remotos.
- Robots.

---

# 12. Errores frecuentes

## No aparece la red

Verificar:

```python
ap.active(True)
```

---

## No conecta

Verificar contraseña.

---

# 13. Actividades

### Básico

Crear red WiFi.

### Medio

Cambiar SSID.

### Avanzado

Crear portal web.

### Experto

Controlar un LED vía navegador.

---

# 14. Preguntas tipo examen

1. ¿Qué significa AP?
2. ¿Qué es un SSID?
3. ¿Qué hace AP_IF?
4. ¿Qué dispositivos pueden conectarse?
5. ¿Qué aplicaciones industriales existen?

---

# 15. Prompt GitHub Copilot

A partir la la especificaciones .md de este proyecto genera un programa MicroPython para ESP32-S3.

Requisitos:

- Conectar a WiFi.
- Mostrar IP.
- Gestionar errores.
- Reconectar automáticamente.

Requisitos:

- Crear punto de acceso.
- Configurar SSID.
- Configurar contraseña.
- Mostrar IP.
- Permitir futuras conexiones web.