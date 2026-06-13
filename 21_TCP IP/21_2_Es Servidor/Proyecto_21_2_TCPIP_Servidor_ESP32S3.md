# Proyecto 21.2 – Servidor TCP/IP

## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# Índice

1. Introducción
2. Objetivos
3. Concepto de Servidor TCP
4. Arquitectura
5. Componentes
6. Puertos TCP
7. Librería Socket
8. Código completo
9. Explicación del programa
10. Flujo de comunicación
11. Aplicaciones reales
12. Errores frecuentes
13. Actividades
14. Preguntas tipo examen
15. Prompt GitHub Copilot

---

# 1. Introducción

En este proyecto el ESP32-S3 actuará como:

```text
SERVIDOR TCP
```

Es decir:

```text
Esperará conexiones
```

procedentes de otros dispositivos.

---

# 2. Objetivos

- Crear un servidor TCP.
- Escuchar conexiones.
- Aceptar clientes.
- Recibir datos.
- Enviar respuestas.

---

# 3. ¿Qué es un servidor?

Un servidor es un dispositivo que permanece esperando solicitudes.

Ejemplos:

- Web Server.
- FTP Server.
- MQTT Broker.
- Servidor TCP.

---

# 4. Arquitectura

```text
Cliente
(PC)

     TCP

Servidor
(ESP32)
```

---

# 5. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| Cable USB-C | 1 |
| Red WiFi | 1 |

---

# 6. ¿Qué es un puerto?

TCP utiliza puertos.

Ejemplos:

| Servicio | Puerto |
|----------|---------|
| HTTP | 80 |
| HTTPS | 443 |
| MQTT | 1883 |

En este proyecto:

```text
5000
```

---

# 7. Código completo

```python
import socket

HOST = ""
PORT = 5000

server = socket.socket()

server.bind(
    (HOST,PORT)
)

server.listen(1)

print(
    "Esperando cliente..."
)

conn, addr = server.accept()

print(
    "Cliente:",
    addr
)

while True:

    data = conn.recv(1024)

    if not data:
        break

    print(data)

    conn.send(
        b"Mensaje recibido"
    )

conn.close()
```

---

# 8. Explicación

## Crear socket

```python
server = socket.socket()
```

---

## Asociar puerto

```python
server.bind(
    (HOST,PORT)
)
```

---

## Escuchar

```python
server.listen(1)
```

---

## Esperar cliente

```python
conn,addr=
server.accept()
```

---

## Recibir datos

```python
conn.recv(1024)
```

---

## Enviar respuesta

```python
conn.send()
```

---

# 9. Flujo de comunicación

```text
Cliente
   │
connect()
   │
   ▼

ESP32

accept()
   │
   ▼

recv()
   │
   ▼

send()
```

---

# 10. Resultado esperado

Terminal:

```text
Esperando cliente

Cliente:
192.168.1.50

Hola servidor
```

---

# 11. Aplicaciones reales

- Servidor Web.
- Servidor IoT.
- API REST.
- Sistemas industriales.
- Monitorización.

---

# 12. Errores frecuentes

## Address already in use

Puerto ocupado.

---

## No conecta ningún cliente

Firewall.

---

## Cliente desconectado

Problemas de red.

---

# 13. Actividades

### Básico

Aceptar conexión.

### Medio

Enviar respuesta.

### Avanzado

Gestionar múltiples clientes.

### Experto

Crear servidor web.

---

# 14. Preguntas tipo examen

1. ¿Qué es un servidor TCP?
2. ¿Qué hace bind()?
3. ¿Qué hace listen()?
4. ¿Qué hace accept()?
5. ¿Qué hace recv()?

---

# 15. Prompt GitHub Copilot

A partir de las especificaciones que encontrarás en el archivo .md del proyecto 20_2 genera un programa MicroPython para ESP32-S3.

Requisitos:

- Crear servidor TCP.
- Escuchar puerto 5000.
- Aceptar conexiones.
- Recibir mensajes.
- Enviar respuestas.
- Gestionar errores.
- Mostrar información por terminal.