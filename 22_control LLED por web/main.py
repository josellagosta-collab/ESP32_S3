# main.py
# Servidor web para controlar un LED conectado al GPIO 2.
# Funciona en un ESP32-S3 con MicroPython.

import socket
import time
import network
from machine import Pin

# ----------------------------------------------------
# CONFIGURACIÓN DEL LED
# ----------------------------------------------------
# El LED se conecta al GPIO 2, como indica la especificación.
led = Pin(2, Pin.OUT)
led.value(0)  # Inicialmente apagado

# Variable de estado para mostrar en la página y en /status.
led_state = "LED APAGADO"

# ----------------------------------------------------
# PÁGINA WEB (HTML + CSS + JavaScript)
# ----------------------------------------------------
# Se incluye directamente como una cadena para no necesitar archivos externos.
HTML = """
<!doctype html>
<html lang=\"es\">
<head>
  <meta charset=\"UTF-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
  <title>Control LED ESP32-S3</title>
  <style>
    :root {
      color-scheme: light;
      font-family: Arial, Helvetica, sans-serif;
      background: linear-gradient(135deg, #eef6ff, #f8fbff);
      color: #17324d;
    }

    * { box-sizing: border-box; }

    body {
      margin: 0;
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }

    .panel {
      width: 100%;
      max-width: 420px;
      background: rgba(255, 255, 255, 0.92);
      border-radius: 24px;
      box-shadow: 0 14px 30px rgba(23, 50, 77, 0.18);
      padding: 28px;
      text-align: center;
    }

    h1 {
      margin-top: 0;
      margin-bottom: 10px;
      font-size: 1.5rem;
      color: #17324d;
    }

    p {
      margin-top: 0;
      color: #45607a;
      font-size: 0.95rem;
    }

    .buttons {
      display: flex;
      justify-content: center;
      gap: 18px;
      margin: 24px 0;
    }

    .btn {
      width: 110px;
      height: 110px;
      border: none;
      border-radius: 50%;
      color: white;
      font-size: 1.3rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 8px 18px rgba(0, 0, 0, 0.18);
      transition: transform 0.08s ease, filter 0.2s ease;
    }

    .btn:hover { filter: brightness(1.06); }
    .btn:active { transform: scale(0.96); }

    .btn-on { background: linear-gradient(145deg, #2ecc71, #1c9d52); }
    .btn-off { background: linear-gradient(145deg, #ff5c5c, #d63a3a); }

    .status-box {
      border: 2px solid #cfd9e5;
      border-radius: 16px;
      padding: 14px;
      background: #f7fbff;
      color: #17324d;
      font-size: 1.05rem;
      font-weight: 700;
      min-height: 52px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: inset 0 1px 2px rgba(23, 50, 77, 0.05);
    }

    .badge {
      display: inline-block;
      margin-top: 10px;
      padding: 6px 10px;
      border-radius: 999px;
      background: #eaf4ff;
      color: #3a5f89;
      font-size: 0.85rem;
    }
  </style>
</head>
<body>
  <main class=\"panel\">
    <h1>Control LED ESP32-S3</h1>
    <p>Presiona un botón para cambiar el estado del LED GPIO 2.</p>

    <div class=\"buttons\">
      <button class=\"btn btn-on\" data-action=\"/on\">ON</button>
      <button class=\"btn btn-off\" data-action=\"/off\">OFF</button>
    </div>

    <div class=\"status-box\" id=\"statusBox\">Esperando estado...</div>
    <div class=\"badge\">Actualización automática cada 2 segundos</div>
  </main>

  <script>
    const statusBox = document.getElementById('statusBox');

    function updateStatus() {
      fetch('/status')
        .then(response => response.text())
        .then(text => {
          statusBox.textContent = text;
        })
        .catch(() => {
          statusBox.textContent = 'Error al consultar el estado';
        });
    }

    document.querySelectorAll('.btn').forEach(btn => {
      btn.addEventListener('click', function () {
        fetch(this.getAttribute('data-action'))
          .then(() => updateStatus())
          .catch(() => {
            statusBox.textContent = 'Error al enviar la orden';
          });
      });
    });

    updateStatus();
    setInterval(updateStatus, 2000);
  </script>
</body>
</html>
"""


# ----------------------------------------------------
# FUNCIONES DE RESPUESTA HTTP
# ----------------------------------------------------

def send_response(conn, status, content_type, body):
    """Envía una respuesta HTTP simple al cliente."""
    response = "HTTP/1.1 {}\r\n".format(status)
    response += "Content-Type: {}\r\n".format(content_type)
    response += "Content-Length: {}\r\n".format(len(body))
    response += "Connection: close\r\n\r\n"
    response = response.encode('utf-8') + body
    conn.sendall(response)


def handle_request(conn, addr):
    """Procesa una petición HTTP entrante."""
    try:
        request = conn.recv(1024)
        if not request:
            return

        request_text = request.decode('utf-8', 'ignore')
        print("Cliente conectado desde:", addr)

        # Extraer la línea de petición: GET /on HTTP/1.1
        lines = request_text.splitlines()
        if not lines:
            return

        first_line = lines[0]
        parts = first_line.split()
        if len(parts) < 3:
            send_response(conn, '400 Bad Request', 'text/plain', b'Peticion invalida')
            return

        method = parts[0]
        path = parts[1].split('?')[0]  # Ignora parámetros de consulta

        # Rutas soportadas.
        if path == '/':
            print("Página principal solicitada")
            send_response(conn, '200 OK', 'text/html', HTML.encode('utf-8'))

        elif path == '/on':
            led.value(1)
            global led_state
            led_state = 'LED ENCENDIDO'
            print("LED encendido")
            send_response(conn, '200 OK', 'text/plain', led_state.encode('utf-8'))

        elif path == '/off':
            led.value(0)
            global led_state
            led_state = 'LED APAGADO'
            print("LED apagado")
            send_response(conn, '200 OK', 'text/plain', led_state.encode('utf-8'))

        elif path == '/status':
            print("Estado consultado")
            send_response(conn, '200 OK', 'text/plain', led_state.encode('utf-8'))

        else:
            print("Ruta no encontrada:", path)
            send_response(conn, '404 Not Found', 'text/plain', b'404 Not Found')

    except Exception as exc:
        print("Error al atender al cliente:", exc)
        try:
            send_response(conn, '500 Internal Server Error', 'text/plain', b'Error interno')
        except Exception:
            pass
    finally:
        conn.close()


# ----------------------------------------------------
# ARRANQUE DEL SERVIDOR WEB
# ----------------------------------------------------

# Crear el socket TCP en el puerto 80.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 80))
server.listen(5)

# Obtener la IP de la interfaz WiFi.
wlan = network.WLAN(network.STA_IF)
if wlan.isconnected():
    ip_address = wlan.ifconfig()[0]
    print("Servidor web iniciado en http://{}".format(ip_address))
else:
    print("Servidor web iniciado, pero WiFi no está conectado.")

print("Esperando conexiones...")

try:
    while True:
        conn, addr = server.accept()
        handle_request(conn, addr)
except KeyboardInterrupt:
    print("Servidor detenido manualmente.")
finally:
    server.close()
