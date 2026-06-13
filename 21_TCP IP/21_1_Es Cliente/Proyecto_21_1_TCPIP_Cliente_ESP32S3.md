# Proyecto 21.1 – Cliente TCP/IP

## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# Índice

1. Introducción
2. Objetivos
3. ¿Qué es TCP/IP?
4. Cliente y Servidor
5. Arquitectura del proyecto
6. Componentes necesarios
7. Funcionamiento del Cliente TCP
8. Librería Socket
9. Código completo
10. Explicación línea por línea
11. Flujo de comunicación
12. Aplicaciones reales
13. Errores frecuentes
14. Actividades
15. Preguntas tipo examen
16. Prompt GitHub Copilot

---

# 1. Introducción

En este capítulo aprenderemos a utilizar el protocolo TCP/IP para intercambiar información entre dispositivos conectados a una red.

TCP/IP es la base de Internet y de prácticamente todas las comunicaciones de red modernas.

En este primer proyecto el ESP32-S3 actuará como:

```text
CLIENTE TCP
```

---

# 2. Objetivos

Al finalizar esta práctica el alumno será capaz de:

- Comprender el modelo Cliente-Servidor.
- Utilizar sockets TCP.
- Conectarse a un servidor remoto.
- Enviar datos.
- Recibir datos.
- Analizar una conexión TCP.

---

# 3. ¿Qué es TCP/IP?

TCP/IP significa:

```text
Transmission Control Protocol

Internet Protocol
```

Es el conjunto de protocolos utilizado por:

- Internet.
- Redes locales.
- Sistemas industriales.
- IoT.

---

# 4. Modelo Cliente-Servidor

En TCP/IP existen dos roles:

## Cliente

Solicita información.

Ejemplos:

- Navegador web.
- Aplicación móvil.
- ESP32 cliente.

---

## Servidor

Proporciona información.

Ejemplos:

- Página web.
- Broker MQTT.
- Servidor industrial.

---

# 5. Arquitectura del proyecto

```text
ESP32-S3
(Cliente)
      │
      │ TCP
      ▼
Servidor
(PC)
```

---

# 6. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| Cable USB-C | 1 |
| Red WiFi | 1 |
| Ordenador servidor | 1 |

---

# 7. Librería Socket

MicroPython incorpora:

```python
import socket
```

Esta librería permite crear conexiones TCP.

---

# 8. Código completo

```python
import socket

HOST = "192.168.1.100"
PORT = 5000

client = socket.socket()

client.connect(
    (HOST, PORT)
)

client.send(
    b"Hola servidor"
)

data = client.recv(1024)

print(data)

client.close()
```

---

# 9. Explicación del código

## Crear socket

```python
client = socket.socket()
```

Crea un cliente TCP.

---

## Conectar

```python
client.connect(
    (HOST,PORT)
)
```

Establece conexión con el servidor.

---

## Enviar datos

```python
client.send(
    b"Hola servidor"
)
```

---

## Recibir datos

```python
data = client.recv(1024)
```

---

## Cerrar conexión

```python
client.close()
```

---

# 10. Flujo de comunicación

```text
ESP32
   │
connect()
   │
   ▼
Servidor

send()
   │
   ▼
Servidor

recv()
   │
   ▼
ESP32
```

---

# 11. Resultado esperado

Terminal:

```text
Conectado

Hola cliente
```

---

# 12. Aplicaciones reales

- MQTT.
- HTTP.
- Node-RED.
- Grafana.
- Wazuh.
- Bases de datos.

---

# 13. Errores frecuentes

## Connection Refused

El servidor no está escuchando.

---

## Timeout

Servidor inaccesible.

---

## Host unreachable

IP incorrecta.

---

# 14. Actividades

### Básico

Enviar texto.

### Medio

Enviar números.

### Avanzado

Enviar JSON.

### Experto

Enviar datos de sensores.

---

# 15. Preguntas tipo examen

1. ¿Qué significa TCP?
2. ¿Qué es un socket?
3. ¿Qué hace connect()?
4. ¿Qué hace send()?
5. ¿Qué hace recv()?

---

# 16. Prompt GitHub Copilot

A partir de las especificaciones que encontrarás en el archivo .md del proyecto 20_1 genera un programa MicroPython para ESP32-S3.

Requisitos:

- Crear cliente TCP.
- Conectarse a un servidor.
- Enviar texto.
- Recibir respuesta.
- Gestionar errores.
- Mostrar información por terminal.