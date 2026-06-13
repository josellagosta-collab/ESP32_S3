# Proyecto 7.2 – Lectura y escritura serial con ESP32-S3 WROOM
## Comunicación bidireccional mediante MicroPython

---

## 1. Objetivo del proyecto

En el proyecto 7.1 aprendimos a enviar datos desde el ESP32-S3 al ordenador utilizando la comunicación serie.

En este proyecto aprenderemos a realizar comunicación bidireccional:

- El ordenador enviará datos al ESP32-S3.
- El ESP32-S3 recibirá esos datos.
- El ESP32-S3 procesará la información recibida.
- El ESP32-S3 responderá enviando información al ordenador.

Este proyecto es la base para crear menús interactivos, configurar dispositivos, controlar actuadores y enviar órdenes desde un PC al microcontrolador.

---

## 2. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3-WROOM | 1 |
| Placa de expansión GPIO | 1 |
| Cable USB Tipo C | 1 |
| Ordenador con Thonny o VS Code | 1 |

---

## 3. Conexión

La conexión es exactamente la misma que en el proyecto 7.1.

```text
+---------------------+
|      ORDENADOR      |
|  Thonny / VS Code   |
+----------+----------+
           |
         USB-C
           |
+----------+----------+
|      ESP32-S3       |
+---------------------+
```

---

## 4. Objetivos de aprendizaje

Al finalizar esta práctica el alumno será capaz de:

1. Enviar datos desde el ordenador al ESP32-S3.
2. Recibir datos mediante la consola serie.
3. Utilizar la función input().
4. Procesar cadenas de texto.
5. Responder a órdenes enviadas por el usuario.
6. Crear programas interactivos.
7. Comprender la comunicación bidireccional.

---

## 5. Comunicación serie bidireccional

En el proyecto anterior:

```text
ESP32-S3 ----> ORDENADOR
```

En este proyecto:

```text
ESP32-S3 <----> ORDENADOR
```

Ahora el ordenador puede enviar información al microcontrolador.

---

## 6. Función input()

La función principal será:

```python
comando = input()
```

Esta instrucción:

1. Espera texto desde el ordenador.
2. Guarda el texto recibido.
3. Continúa la ejecución cuando el usuario pulsa ENTER.

Ejemplo:

```text
Usuario escribe:
hola

ESP32 recibe:
hola
```

---

## 7. Funcionamiento esperado

1. El ESP32 muestra un mensaje de bienvenida.
2. Espera texto del usuario.
3. El usuario escribe un mensaje.
4. El ESP32 muestra el mensaje recibido.
5. El proceso se repite indefinidamente.

Ejemplo:

```text
ESP32-S3 ready

hola
Recibido: hola

prueba
Recibido: prueba

123
Recibido: 123
```

---

## 8. Requisitos obligatorios

El archivo main.py debe:

1. Utilizar MicroPython.
2. Mostrar un mensaje inicial.
3. Esperar texto desde el ordenador.
4. Leer el texto usando input().
5. Mostrar el texto recibido.
6. Ejecutarse continuamente.
7. Incluir comentarios explicativos.

---

## 9. Código de referencia esperado

```python
print("ESP32-S3 ready")

while True:

    mensaje = input()

    print("Recibido:", mensaje)
```

---

## 10. Versión mejorada

```python
print("ESP32-S3 serial terminal")
print("Escribe un mensaje y pulsa ENTER")

while True:

    mensaje = input("> ")

    print("Has escrito:", mensaje)
```

---

## 11. Versión con comandos

```python
print("ESP32-S3 command console")

while True:

    comando = input("> ")

    if comando == "hola":
        print("Hola usuario")

    elif comando == "estado":
        print("Sistema operativo")

    elif comando == "salir":
        print("Comando recibido")

    else:
        print("Comando desconocido")
```

---

## 12. Aplicaciones reales

- Control de robots.
- Configuración WiFi.
- Configuración MQTT.
- Envío de órdenes.
- Pruebas de sensores.
- Menús interactivos.
- Sistemas IoT.

---

## 13. Errores frecuentes

### No responde al escribir

Posibles causas:

- No se ha pulsado ENTER.
- La consola no está conectada al ESP32.
- El programa no está ejecutándose.

### Aparece EOFError

Posibles causas:

- La conexión serie se ha cerrado.
- Reinicio del ESP32.

### No aparece el mensaje recibido

Posibles causas:

- Error de indentación.
- Error en la variable utilizada.

---

## 14. Retos para el alumnado

### Nivel básico

Convertir todo el texto recibido a mayúsculas.

### Nivel medio

Responder de forma distinta según el comando.

### Nivel avanzado

Crear un menú interactivo.

### Nivel experto

Controlar LEDs mediante comandos:

```text
led on
led off
```

---

## 15. Preguntas para el alumnado

1. ¿Para qué sirve input()?
2. ¿Qué diferencia hay entre print() e input()?
3. ¿Qué ocurre cuando se pulsa ENTER?
4. ¿Qué tipo de dato devuelve input()?
5. ¿Cómo podríamos crear un menú interactivo?
6. ¿Qué aplicaciones reales tiene este sistema?

---

## 16. Criterios de evaluación

| Criterio | Logrado | No logrado |
|----------|----------|------------|
| Conecta correctamente el ESP32-S3 | | |
| Utiliza print() correctamente | | |
| Utiliza input() correctamente | | |
| Recibe datos desde el ordenador | | |
| Responde correctamente | | |
| Código comentado | | |
| Comprende la comunicación bidireccional | | |

---

## 17. Prompt optimizado para GitHub Copilot / Cursor

Genera un archivo main.py para una placa ESP32-S3 WROOM utilizando MicroPython.

Requisitos:

- Mostrar un mensaje inicial indicando que el sistema está preparado.
- Esperar texto desde el ordenador mediante input().
- Guardar el texto recibido en una variable.
- Mostrar el texto recibido usando print().
- Ejecutarse en un bucle infinito.
- Incluir comentarios explicativos.
- Código sencillo para alumnado principiante.

El resultado debe permitir escribir mensajes desde Thonny o VS Code y ver la respuesta del ESP32-S3.

---

## 18. Resultado esperado

Al ejecutar el programa:

```text
ESP32-S3 ready

hola
Recibido: hola

prueba
Recibido: prueba
```

El usuario podrá enviar mensajes al ESP32-S3 y comprobar cómo el microcontrolador recibe y procesa la información enviada mediante la comunicación serie.
