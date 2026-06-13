# Proyecto 19.2 – Control de LED mediante Bluetooth Low Energy

## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# Índice

1. Introducción
2. Objetivos
3. Componentes necesarios
4. Esquema de funcionamiento
5. Montaje
6. Comunicación BLE
7. Comandos de control
8. Código esperado
9. Explicación del funcionamiento
10. Aplicaciones reales
11. Errores frecuentes
12. Actividades
13. Preguntas tipo examen
14. Prompt GitHub Copilot

---

# 1. Introducción

En este proyecto ampliaremos el anterior.

Ahora utilizaremos Bluetooth Low Energy para controlar un LED conectado al ESP32-S3.

Desde el teléfono podremos:

```text
ON
```

Encender LED.

```text
OFF
```

Apagar LED.

---

# 2. Objetivos

- Recibir comandos BLE.
- Interpretar cadenas de texto.
- Controlar GPIO.
- Crear una aplicación IoT básica.

---

# 3. Componentes

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| LED | 1 |
| Resistencia 220Ω | 1 |
| Cable USB-C | 1 |
| Smartphone | 1 |

---

# 4. Arquitectura

```text
Smartphone
      ↓
Bluetooth LE
      ↓
ESP32-S3
      ↓
GPIO
      ↓
LED
```

---

# 5. Conexiones

| LED | ESP32 |
|------|--------|
| Ánodo | GPIO2 |
| Cátodo | GND mediante 220Ω |

---

# 6. Funcionamiento

El móvil enviará:

```text
ON
```

o

```text
OFF
```

El ESP32 interpretará el mensaje.

---

# 7. Tabla de comandos

| Comando | Acción |
|----------|---------|
| ON | Encender LED |
| OFF | Apagar LED |
| STATUS | Estado LED |

---

# 8. Lógica del programa

```text
Esperar mensaje BLE
        ↓
Recibir texto
        ↓
¿ON?
    ↓
 Encender LED

¿OFF?
    ↓
 Apagar LED
```

---

# 9. Resultado esperado

Terminal:

```text
Received: ON

LED ON
```

Posteriormente:

```text
Received: OFF

LED OFF
```

---

# 10. Aplicaciones reales

- Domótica.
- Iluminación inteligente.
- Control industrial.
- Robots.
- Sistemas de alarma.

---

# 11. Ampliaciones

Controlar:

- Relés.
- Servos.
- Motores.
- Tiras LED RGB.

---

# 12. Errores frecuentes

## El LED no responde

Comprobar:

- GPIO correcto.
- Resistencia.
- Conexión BLE.

---

## El móvil conecta pero no funciona

Verificar:

- Característica correcta.
- Formato del comando.

---

# 13. Actividades

### Básico

Controlar un LED.

### Medio

Controlar dos LEDs.

### Avanzado

Controlar una barra LED.

### Experto

Controlar un servomotor.

---

# 14. Preguntas tipo examen

1. ¿Qué es BLE?
2. ¿Qué comando enciende el LED?
3. ¿Qué GPIO controla el LED?
4. ¿Qué ventajas aporta BLE?
5. ¿Qué aplicaciones industriales existen?

---

# 15. Prompt GitHub Copilot

A partir de las especificaciones del archivo .md de este proyecto genera un programa MicroPython para ESP32-S3.

Requisitos:

- Activar Bluetooth Low Energy.
- Crear servicio BLE.
- Recibir comandos de texto.
- Encender LED con comando ON.
- Apagar LED con comando OFF.
- Mostrar eventos en terminal.
- Código comentado.