# Proyecto 7.1 – Serial Print con ESP32-S3 WROOM
## Comunicación serie básica con MicroPython

---

## 1. Objetivo del proyecto

El objetivo de este proyecto es aprender a enviar información desde una placa **ESP32-S3 WROOM** al ordenador utilizando la comunicación serie por USB.

El programa enviará mensajes de texto al ordenador para que puedan visualizarse en la consola de **Thonny**, en el monitor serie de **Visual Studio Code**, o en cualquier otro terminal serie compatible.

Este proyecto es muy importante porque la comunicación serie se utiliza constantemente para:

- Comprobar si un programa se está ejecutando.
- Ver mensajes de depuración.
- Mostrar valores de sensores.
- Comprobar tiempos de ejecución.
- Diagnosticar errores.
- Entender qué está haciendo el microcontrolador.

---

## 2. Descripción general

En este proyecto el ESP32-S3 enviará un mensaje inicial al ordenador indicando que el sistema se ha iniciado correctamente.

Después, cada segundo, mostrará el tiempo que lleva funcionando desde que se ejecutó el programa.

Ejemplo de salida esperada:

```text
ESP32S3 initialization completed!
Running time :  1.0 s
Running time :  2.0 s
Running time :  3.0 s
Running time :  4.0 s
Running time :  5.0 s
```

---

## 3. Componentes necesarios

| Componente | Cantidad |
|-----------|----------|
| ESP32-S3-WROOM | 1 |
| Placa de expansión GPIO | 1 |
| Cable USB tipo C | 1 |
| Ordenador con Thonny o VS Code | 1 |

---

## 4. Conexión

La conexión es directa.

Solo hay que conectar el ESP32-S3 al ordenador mediante el cable USB tipo C.

No se necesitan sensores, LEDs, resistencias ni ningún componente adicional.

```text
+---------------------+
|      ORDENADOR      |
|  Thonny / VS Code   |
+----------+----------+
           |
           |
        USB-C
           |
           |
+----------+----------+
|     ESP32-S3        |
|     WROOM           |
+---------------------+
```

---

## 5. Tabla de conexión

| Elemento | Conexión |
|---------|----------|
| ESP32-S3 | Ordenador mediante cable USB-C |
| Alimentación | A través del USB |
| Comunicación serie | A través del USB |
| Monitor serie | Consola de Thonny o VS Code |

---

## 6. Objetivos de aprendizaje

Al finalizar este proyecto, el alumno debe ser capaz de:

1. Entender qué es la comunicación serie.
2. Ejecutar un programa MicroPython en el ESP32-S3.
3. Utilizar la función `print()`.
4. Visualizar mensajes enviados por el ESP32-S3.
5. Usar `time.ticks_ms()` para conocer el tiempo de ejecución.
6. Convertir milisegundos a segundos.
7. Usar `time.sleep()` para crear retardos.
8. Usar la consola serie como herramienta de depuración.
9. Interpretar mensajes del microcontrolador.
10. Preparar programas más complejos que muestren datos de sensores.

---

## 7. ¿Qué es la comunicación serie?

La comunicación serie es una forma de transmitir datos entre dos dispositivos enviando la información bit a bit.

En este caso, los dos dispositivos son:

```text
ESP32-S3  <---- USB Serie ---->  Ordenador
```

Aunque físicamente usamos un cable USB-C, el ordenador detecta el ESP32-S3 como un dispositivo serie.

Esto permite que el microcontrolador envíe texto al ordenador.

---

## 8. ¿Para qué sirve `print()`?

En MicroPython, la función `print()` sirve para enviar información a la consola.

Ejemplo:

```python
print("Hola desde ESP32-S3")
```

Cuando se ejecuta esa línea, el texto aparece en la consola serie.

`print()` es muy útil para depurar programas.

Por ejemplo:

```python
print("Inicio del programa")
print("Botón pulsado")
print("Valor del sensor:", valor)
```

---

## 9. ¿Qué es `time.ticks_ms()`?

La función:

```python
time.ticks_ms()
```

devuelve el número de milisegundos transcurridos desde que la placa arrancó.

Por ejemplo:

```text
1000 ms = 1 segundo
2000 ms = 2 segundos
5000 ms = 5 segundos
```

Por eso, para convertir milisegundos a segundos, se divide entre 1000:

```python
time.ticks_ms() / 1000
```

---

## 10. ¿Qué hace `time.sleep(1)`?

La instrucción:

```python
time.sleep(1)
```

detiene el programa durante 1 segundo.

En este proyecto se usa para que el mensaje se imprima una vez por segundo.

Si no se usara `sleep`, el ESP32-S3 imprimiría mensajes muy rápido y la consola se llenaría de texto continuamente.

---

## 11. Funcionamiento esperado

El programa debe:

1. Importar el módulo `time`.
2. Mostrar un mensaje inicial.
3. Entrar en un bucle infinito.
4. Calcular el tiempo transcurrido desde el arranque.
5. Mostrar ese tiempo en segundos.
6. Esperar 1 segundo.
7. Repetir el proceso indefinidamente.

---

## 12. Código de referencia esperado

Este código debe ser similar al mostrado en la captura de pantalla de la práctica.

```python
import time

print("ESP32S3 initialization completed!")

while True:
    print("Running time : ", time.ticks_ms() / 1000, "s")
    time.sleep(1)
```

---

## 13. Explicación línea por línea

### Importar el módulo time

```python
import time
```

Permite usar funciones relacionadas con el tiempo.

---

### Mensaje inicial

```python
print("ESP32S3 initialization completed!")
```

Muestra un mensaje indicando que el ESP32-S3 ha iniciado correctamente el programa.

---

### Bucle infinito

```python
while True:
```

Hace que el programa se ejecute continuamente.

---

### Mostrar el tiempo

```python
print("Running time : ", time.ticks_ms() / 1000, "s")
```

Muestra el tiempo de funcionamiento en segundos.

---

### Esperar un segundo

```python
time.sleep(1)
```

Espera 1 segundo antes de volver a imprimir el mensaje.

---

## 14. Versión mejorada con segundos enteros

Esta versión evita mostrar decimales.

```python
import time

print("ESP32S3 initialization completed!")

while True:
    segundos = time.ticks_ms() // 1000
    print("Running time :", segundos, "s")
    time.sleep(1)
```

---

## 15. Versión con minutos y segundos

Esta versión muestra el tiempo en formato más claro.

```python
import time

print("ESP32S3 initialization completed!")

while True:
    total_segundos = time.ticks_ms() // 1000

    minutos = total_segundos // 60
    segundos = total_segundos % 60

    print("Running time :", minutos, "min", segundos, "s")

    time.sleep(1)
```

---

## 16. Versión con contador manual

Esta versión no usa `ticks_ms()`, sino una variable contador.

```python
import time

print("ESP32S3 initialization completed!")

contador = 0

while True:
    print("Running time :", contador, "s")
    contador = contador + 1
    time.sleep(1)
```

---

## 17. Uso en Thonny

Para probar el proyecto en Thonny:

1. Conectar el ESP32-S3 al ordenador mediante USB-C.
2. Abrir Thonny.
3. Seleccionar el intérprete MicroPython para ESP32.
4. Elegir el puerto COM correspondiente.
5. Abrir el archivo `main.py`.
6. Ejecutar el programa.
7. Observar la salida en la consola inferior.

---

## 18. Uso en Visual Studio Code

Para usarlo en Visual Studio Code:

1. Instalar una extensión compatible con MicroPython.
2. Conectar el ESP32-S3 por USB-C.
3. Seleccionar el puerto serie correcto.
4. Crear el archivo `main.py`.
5. Copiar el código generado.
6. Subirlo al ESP32-S3.
7. Abrir el monitor serie.
8. Comprobar que aparecen los mensajes cada segundo.

---

## 19. Requisitos obligatorios del archivo `main.py`

El programa generado debe cumplir:

1. Estar escrito en MicroPython.
2. Importar el módulo `time`.
3. Usar `print()`.
4. Mostrar el mensaje inicial:
   ```text
   ESP32S3 initialization completed!
   ```
5. Usar un bucle `while True`.
6. Usar `time.ticks_ms()`.
7. Convertir milisegundos a segundos.
8. Mostrar el texto:
   ```text
   Running time :
   ```
9. Esperar 1 segundo entre mensajes.
10. Ser sencillo y fácil de leer.
11. Incluir comentarios explicativos.

---

## 20. Salida esperada en consola

```text
ESP32S3 initialization completed!
Running time :  0.0 s
Running time :  1.0 s
Running time :  2.0 s
Running time :  3.0 s
Running time :  4.0 s
Running time :  5.0 s
```

---

## 21. Errores frecuentes

### 21.1 No aparece nada en la consola

Posibles causas:

- El ESP32-S3 no está conectado.
- El cable USB solo sirve para carga y no para datos.
- El puerto COM seleccionado no es correcto.
- El programa no se ha ejecutado.
- El firmware MicroPython no está instalado correctamente.

Soluciones:

- Probar otro cable USB-C.
- Cambiar de puerto USB.
- Seleccionar el puerto correcto en Thonny.
- Pulsar el botón de reinicio de la placa.
- Ejecutar de nuevo el programa.

---

### 21.2 Aparecen símbolos extraños

Posibles causas:

- Problema de velocidad del puerto serie.
- Consola mal configurada.
- Reinicio de la placa durante la comunicación.

Soluciones:

- Cerrar y abrir el puerto serie.
- Reiniciar Thonny.
- Desconectar y volver a conectar la placa.

---

### 21.3 El programa imprime demasiado rápido

Causa probable:

- Falta la línea:

```python
time.sleep(1)
```

Solución:

- Añadir una pausa dentro del bucle.

---

### 21.4 El tiempo aparece con muchos decimales

Causa:

```python
time.ticks_ms() / 1000
```

produce un número decimal.

Solución:

Usar división entera:

```python
time.ticks_ms() // 1000
```

---

### 21.5 El programa se reinicia continuamente

Posibles causas:

- Error en el código.
- Alimentación inestable.
- Fallo del cable USB.
- El ESP32-S3 se está reseteando.

---

## 22. Retos para el alumnado

### Nivel básico

Cambiar el mensaje inicial por otro personalizado.

---

### Nivel medio

Mostrar el tiempo en minutos y segundos.

---

### Nivel avanzado

Mostrar una tabla con el número de segundos transcurridos.

Ejemplo:

```text
Segundo actual: 1
Segundo actual: 2
Segundo actual: 3
```

---

### Nivel avanzado 2

Simular el envío de datos de un sensor.

Ejemplo:

```text
Temperatura simulada: 25 C
Temperatura simulada: 26 C
Temperatura simulada: 27 C
```

---

### Nivel experto

Enviar los datos en formato CSV:

```text
tiempo_s,valor
1,25
2,26
3,27
```

---

## 23. Preguntas para el alumnado

1. ¿Qué función se utiliza para enviar texto al ordenador?
2. ¿Qué es la comunicación serie?
3. ¿Para qué sirve `time.ticks_ms()`?
4. ¿Por qué se divide entre 1000?
5. ¿Qué hace `time.sleep(1)`?
6. ¿Qué ocurriría si eliminamos la pausa?
7. ¿Dónde se visualiza la salida del programa?
8. ¿Qué diferencia hay entre `/` y `//` en Python?
9. ¿Para qué sirve imprimir mensajes durante el desarrollo?
10. ¿Qué puede estar pasando si no aparece nada en la consola?

---

## 24. Criterios de evaluación

| Criterio | Logrado | No logrado |
|----------|---------|------------|
| Conecta correctamente el ESP32-S3 al ordenador | | |
| Ejecuta el programa en MicroPython | | |
| Utiliza correctamente `print()` | | |
| Utiliza correctamente `time.ticks_ms()` | | |
| Muestra el tiempo transcurrido | | |
| Usa un bucle infinito | | |
| Incluye una pausa de 1 segundo | | |
| Interpreta correctamente la salida serie | | |
| Resuelve errores básicos de conexión | | |
| Comprende la utilidad de la depuración serie | | |

---

## 25. Prompt optimizado para GitHub Copilot / Cursor / IA de VS Code

Genera un archivo `main.py` para una placa ESP32-S3 WROOM usando MicroPython.

El proyecto se llama **Proyecto 7.1 Serial Print**.

Objetivo:

Crear un programa que envíe mensajes al ordenador mediante la comunicación serie USB.

Requisitos:

- Importar el módulo `time`.
- Mostrar al iniciar el mensaje:
  `ESP32S3 initialization completed!`
- Entrar en un bucle infinito.
- Usar `time.ticks_ms()` para calcular el tiempo transcurrido desde el arranque.
- Convertir los milisegundos a segundos.
- Imprimir cada segundo un mensaje con el formato:
  `Running time : X s`
- Usar `time.sleep(1)` para esperar un segundo entre mensajes.
- El código debe estar comentado.
- El código debe ser sencillo y adecuado para alumnado principiante de Formación Profesional.
- El resultado debe poder visualizarse en la consola de Thonny o en el monitor serie de VS Code.

Código esperado de referencia:

```python
import time

print("ESP32S3 initialization completed!")

while True:
    print("Running time : ", time.ticks_ms() / 1000, "s")
    time.sleep(1)
```

---

## 26. Resultado esperado

Cuando el alumno ejecute el programa en el ESP32-S3, deberá observar en la consola serie un mensaje inicial y después una línea nueva cada segundo mostrando el tiempo de ejecución.

Este proyecto servirá como base para futuras prácticas en las que se mostrarán datos de sensores, estados de botones, valores analógicos y mensajes de depuración.
