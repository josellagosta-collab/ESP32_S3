# Especificación del proyecto: Control web de LED con ESP32-S3 y MicroPython

## 1. Objetivo del proyecto

Crear una aplicación web sencilla ejecutada directamente en un **ESP32-S3 flasheado con MicroPython**.

La aplicación permitirá controlar un LED conectado al **GPIO 2** mediante una página web con dos botones:

- Botón verde circular **ON**: enciende el LED.
- Botón rojo circular **OFF**: apaga el LED.
- Cuadro de texto dinámico que muestra el estado actual del LED: `LED ENCENDIDO` o `LED APAGADO`.

El ESP32-S3 actuará como **servidor web** y permitirá acceder a la página desde un navegador conectado a la misma red WiFi.

---

## 2. Hardware necesario

- Placa ESP32-S3 con MicroPython instalado.
- 1 LED.
- 1 resistencia de 220 Ω.
- Cables Dupont.
- Protoboard.

---

## 3. Conexión del LED

El LED se conecta al pin **GPIO 2** del ESP32-S3 usando una resistencia de protección de **220 Ω**.

### Esquema de conexión

```text
GPIO 2 ─── Resistencia 220 Ω ─── Ánodo LED
Cátodo LED ─── GND
```

### Funcionamiento esperado

- Cuando el GPIO 2 está en nivel alto (`1`), el LED se enciende.
- Cuando el GPIO 2 está en nivel bajo (`0`), el LED se apaga.

---

## 4. Archivos necesarios

El proyecto debe tener los siguientes archivos:

```text
esp32s3_web_led/
│
├── boot.py
├── main.py
└── README.md
```

---

## 5. Descripción de cada archivo

### 5.1. `boot.py`

Archivo que se ejecuta automáticamente al arrancar el ESP32-S3.

Debe encargarse de:

- Importar el módulo `network`.
- Conectarse a una red WiFi en modo estación.
- Usar dos variables configurables:
  - `SSID`
  - `PASSWORD`
- Mostrar por consola:
  - Intento de conexión.
  - Estado de conexión.
  - Dirección IP asignada al ESP32-S3.
- Esperar hasta que la conexión WiFi esté activa.
- No debe contener el servidor web.
- Debe dejar la conexión WiFi preparada para que `main.py` pueda iniciar el servidor.

Ejemplo de variables que deben aparecer en el archivo:

```python
SSID = "NOMBRE_DE_TU_WIFI"
PASSWORD = "CONTRASEÑA_DE_TU_WIFI"
```

---

### 5.2. `main.py`

Archivo principal del proyecto.

Debe encargarse de:

- Importar los módulos necesarios:
  - `socket`
  - `machine.Pin`
  - `network`
  - `time`
- Configurar el GPIO 2 como salida.
- Inicializar el LED apagado.
- Crear un servidor web HTTP en el puerto 80.
- Escuchar peticiones desde un navegador.
- Responder a las rutas:
  - `/`
  - `/on`
  - `/off`
  - `/status`

---

## 6. Funcionamiento del servidor web

El ESP32-S3 debe crear un servidor HTTP sencillo usando sockets.

### Rutas necesarias

| Ruta | Función |
|---|---|
| `/` | Muestra la página web principal |
| `/on` | Enciende el LED |
| `/off` | Apaga el LED |
| `/status` | Devuelve el estado actual del LED en texto plano |

---

## 7. Página web que debe generar el ESP32-S3

La página web debe estar integrada dentro de `main.py` como una cadena HTML.

No se usarán archivos externos `.html`, `.css` ni `.js`, para simplificar el proyecto y facilitar su carga en el ESP32-S3.

La web debe contener:

- Título: `Control LED ESP32-S3`
- Dos botones circulares grandes:
  - Botón verde con texto `ON`
  - Botón rojo con texto `OFF`
- Un cuadro de estado dinámico.
- Diseño centrado en pantalla.
- Estilo CSS integrado dentro del HTML.
- JavaScript integrado dentro del HTML.

---

## 8. Diseño visual de la página

Características del diseño:

- Fondo claro.
- Contenedor centrado.
- Botones circulares de tamaño grande.
- Botón `ON` de color verde.
- Botón `OFF` de color rojo.
- Cuadro de estado con borde visible.
- Texto del estado grande y fácil de leer.

Ejemplo visual aproximado:

```text
┌──────────────────────────────┐
│     Control LED ESP32-S3     │
│                              │
│      🟢 ON       🔴 OFF       │
│                              │
│   Estado: LED APAGADO        │
└──────────────────────────────┘
```

---

## 9. Comportamiento dinámico de la web

La página debe usar JavaScript con `fetch()`.

### Botón ON

Al pulsar el botón `ON`:

- Se envía una petición HTTP a `/on`.
- El ESP32-S3 enciende el LED.
- El cuadro de estado se actualiza mostrando `LED ENCENDIDO`.

### Botón OFF

Al pulsar el botón `OFF`:

- Se envía una petición HTTP a `/off`.
- El ESP32-S3 apaga el LED.
- El cuadro de estado se actualiza mostrando `LED APAGADO`.

### Estado dinámico

El cuadro de estado debe actualizarse:

- Al pulsar cualquier botón.
- Automáticamente cada 2 segundos consultando `/status`.

---

## 10. Requisitos técnicos de MicroPython

El código debe ser compatible con MicroPython para ESP32-S3.

No debe usar librerías externas.

Debe usar únicamente módulos estándar de MicroPython:

```python
import network
import socket
import time
from machine import Pin
```

---

## 11. Gestión del LED

En `main.py`, el LED debe declararse así:

```python
led = Pin(2, Pin.OUT)
led.value(0)
```

Se debe mantener una variable de estado:

```python
led_state = "LED APAGADO"
```

Cuando se reciba `/on`:

```python
led.value(1)
led_state = "LED ENCENDIDO"
```

Cuando se reciba `/off`:

```python
led.value(0)
led_state = "LED APAGADO"
```

---

## 12. Respuestas HTTP

El servidor debe devolver respuestas HTTP válidas.

Para la página principal `/`:

- Código HTTP: `200 OK`
- Tipo de contenido: `text/html`

Para `/on`, `/off` y `/status`:

- Código HTTP: `200 OK`
- Tipo de contenido: `text/plain`

---

## 13. Control de errores

El programa debe incluir control básico de errores:

- Si llega una ruta desconocida, devolver `404 Not Found`.
- Si ocurre un error con un cliente, cerrar correctamente la conexión.
- El servidor debe seguir funcionando después de atender cada petición.

---

## 14. Mensajes por consola

El programa debe mostrar mensajes útiles por consola:

- IP del ESP32-S3.
- Inicio del servidor web.
- Cliente conectado.
- Acción realizada:
  - LED encendido.
  - LED apagado.
  - Consulta de estado.

Ejemplo:

```text
Servidor web iniciado en http://192.168.1.45
Cliente conectado desde: ('192.168.1.20', 52344)
LED encendido
LED apagado
Estado consultado
```

---

## 15. Instrucciones para generar el código con GitHub Copilot

GitHub Copilot debe generar el código completo de los siguientes archivos:

- `boot.py`
- `main.py`
- `README.md`

A partir de esta especificación, Copilot debe crear un proyecto MicroPython funcional para ESP32-S3.

El código debe estar comentado y ser didáctico, pensado para alumnos que están aprendiendo MicroPython, redes WiFi y servidores web embebidos.

---

## 16. Resultado esperado

Después de cargar `boot.py` y `main.py` en el ESP32-S3:

1. El ESP32-S3 se conecta a la red WiFi.
2. Muestra por consola la IP asignada.
3. El usuario abre esa IP en un navegador.
4. Aparece una página web con dos botones circulares.
5. Al pulsar `ON`, el LED conectado al GPIO 2 se enciende.
6. Al pulsar `OFF`, el LED se apaga.
7. El cuadro de estado muestra siempre el estado real del LED.

---

## 17. Prompt recomendado para Copilot Chat

Usa este prompt en GitHub Copilot Chat dentro de VS Code:

```text
A partir del archivo de especificaciones README.md de este proyecto, genera todo el código necesario para un ESP32-S3 con MicroPython.

Necesito los archivos boot.py y main.py.

El ESP32-S3 debe conectarse a una red WiFi, iniciar un servidor web en el puerto 80 y mostrar una página HTML con dos botones circulares: ON verde y OFF rojo.

El botón ON debe encender un LED conectado al GPIO 2 y el botón OFF debe apagarlo.

La página debe tener un cuadro de texto dinámico que muestre el estado actual del LED.

Usa solo módulos estándar de MicroPython y escribe el código de forma didáctica y comentada.
```

---

## 18. Nota importante

Antes de ejecutar el proyecto, hay que modificar en `boot.py` los datos reales de la red WiFi:

```python
SSID = "TU_WIFI"
PASSWORD = "TU_PASSWORD"
```

