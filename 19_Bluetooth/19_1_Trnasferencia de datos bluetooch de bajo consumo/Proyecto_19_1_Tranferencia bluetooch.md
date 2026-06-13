# Proyecto 19.1 – Transferencia de Datos Bluetooth Low Energy (BLE)

## Manual Didáctico Completo para ESP32-S3 y MicroPython

---

# Índice

1. Introducción
2. ¿Qué es Bluetooth Low Energy?
3. Diferencias entre Bluetooth Clásico y BLE
4. Objetivos del proyecto
5. Componentes necesarios
6. Arquitectura del sistema
7. Funcionamiento del proyecto
8. Instalación de la App móvil
9. Código BLE del ESP32-S3
10. Explicación del programa
11. Comunicación ESP32 ↔ Smartphone
12. Aplicaciones reales
13. Errores frecuentes
14. Actividades propuestas
15. Preguntas tipo examen
16. Prompt para GitHub Copilot

---

# 1. Introducción

En este proyecto aprenderemos a utilizar Bluetooth Low Energy (BLE) integrado en el ESP32-S3.

El objetivo será enviar y recibir datos entre:

```text
ESP32-S3
    ↔
Smartphone
```

sin necesidad de cables.

---

# 2. ¿Qué es Bluetooth Low Energy?

BLE significa:

```text
Bluetooth Low Energy
```

Es una versión optimizada de Bluetooth diseñada para:

- Bajo consumo energético.
- Dispositivos IoT.
- Sensores inalámbricos.
- Wearables.
- Domótica.

El ESP32-S3 incorpora BLE de forma nativa. :contentReference[oaicite:1]{index=1}

---

# 3. Bluetooth clásico vs BLE

| Característica | Bluetooth clásico | BLE |
|---------------|------------------|-----|
| Consumo | Alto | Muy bajo |
| IoT | Limitado | Excelente |
| Sensores | No ideal | Ideal |
| Batería | Menor duración | Mayor duración |

---

# 4. Objetivos

- Configurar BLE en el ESP32-S3.
- Crear un dispositivo BLE.
- Conectarlo a un smartphone.
- Enviar datos.
- Recibir datos.
- Mostrar mensajes en el terminal.

---

# 5. Componentes necesarios

| Componente | Cantidad |
|------------|----------|
| ESP32-S3-WROOM | 1 |
| Cable USB-C | 1 |
| Smartphone Android | 1 |

---

# 6. Arquitectura

```text
+------------+
| Smartphone |
+------------+
       |
   BLE 5.0
       |
+------------+
| ESP32-S3   |
+------------+
```

---

# 7. Funcionamiento

1. ESP32 inicia BLE.
2. Smartphone detecta dispositivo.
3. Se establece conexión.
4. Se envían datos.
5. Se reciben datos.

---

# 8. Aplicación móvil recomendada

nRF Connect

Permite:

- Buscar dispositivos BLE.
- Leer características.
- Escribir características.
- Monitorizar tráfico BLE.

---

# 9. Código esperado

El ESP32 crea un servicio BLE.

Posteriormente:

```text
Móvil → ESP32
```

o

```text
ESP32 → Móvil
```

---

# 10. Flujo de comunicación

```text
Usuario escribe mensaje
         ↓
 Smartphone
         ↓
 Bluetooth LE
         ↓
 ESP32-S3
         ↓
 Terminal serie
```

---

# 11. Resultado esperado

Terminal:

```text
BLE Connected

Received:
Hola ESP32
```

---

# 12. Aplicaciones reales

- Sensores IoT.
- Pulseras deportivas.
- Automatización industrial.
- Robots móviles.
- Smart Home.

---

# 13. Errores frecuentes

## No aparece el dispositivo

Verificar:

- Bluetooth activado.
- Programa ejecutándose.

---

## No conecta

Verificar:

- Permisos Bluetooth.
- Distancia.

---

# 14. Actividades

### Básico

Enviar texto.

### Medio

Enviar números.

### Avanzado

Enviar JSON.

### Experto

Controlar un robot.

---

# 15. Preguntas tipo examen

1. ¿Qué significa BLE?
2. ¿Qué ventaja tiene frente a Bluetooth clásico?
3. ¿Qué aplicación se utiliza para pruebas?
4. ¿Qué es una característica BLE?
5. ¿Qué es un servicio BLE?

---

# 16. Prompt para GitHub Copilot

A partir del archivo de especificaciones .md de este proyecto genera un programa MicroPython para ESP32-S3.

Requisitos:

- Activar Bluetooth Low Energy.
- Crear un servicio BLE.
- Permitir recibir texto.
- Mostrar datos recibidos en terminal.
- Permitir enviar mensajes al móvil.
- Añadir comentarios explicativos.