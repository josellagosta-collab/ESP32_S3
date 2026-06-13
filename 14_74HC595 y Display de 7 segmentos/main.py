"""
Proyecto 14.1 - Pantalla de 7 segmentos con 74HC595
ESP32-S3 WROOM + MicroPython

Descripción:
Controla una pantalla de 7 segmentos usando un registro de desplazamiento 74HC595.
Muestra los números del 0 al 9 de forma cíclica.

Conexiones:
- GPIO12 <-> STCP del 74HC595 (Latch)
- GPIO13 <-> SHCP del 74HC595 (Clock)
- GPIO14 <-> DS del 74HC595 (Data)
- GND <-> OE del 74HC595
- Q0-Q7 <-> Segmentos A-G y DP mediante resistencias 220Ω
- Pantalla de 7 segmentos de cátodo común
"""

from machine import Pin
import time

# ============================================================================
# CONFIGURACIÓN DE PINES
# ============================================================================

# Pines conectados al 74HC595
STCP = Pin(12, Pin.OUT)   # Storage Clock / Latch (pin 12)
SHCP = Pin(13, Pin.OUT)   # Shift Clock (pin 13)
DS = Pin(14, Pin.OUT)     # Data (pin 14)

# Inicializar pines en estado bajo
STCP.value(0)
SHCP.value(0)
DS.value(0)

# ============================================================================
# TABLA DE PATRONES HEXADECIMALES
# ============================================================================

"""
Relación entre salidas del 74HC595 y segmentos:
- Q0 -> Segmento A
- Q1 -> Segmento B
- Q2 -> Segmento C
- Q3 -> Segmento D
- Q4 -> Segmento E
- Q5 -> Segmento F
- Q6 -> Segmento G
- Q7 -> Punto Decimal (DP)

Tabla de segmentos por número:
Número | Segmentos encendidos | Binario    | Hexadecimal
0      | A B C D E F          | 00111111   | 0x3F
1      | B C                  | 00000110   | 0x06
2      | A B D E G            | 01011011   | 0x5B
3      | A B C D G            | 01001111   | 0x4F
4      | B C F G              | 01100110   | 0x66
5      | A C D F G            | 01101101   | 0x6D
6      | A C D E F G          | 01111101   | 0x7D
7      | A B C                | 00000111   | 0x07
8      | A B C D E F G        | 01111111   | 0x7F
9      | A B C D F G          | 01101111   | 0x6F
"""

# Tabla con los patrones para cada número (0-9)
numeros = [
    0x3F,  # 0 - A B C D E F
    0x06,  # 1 - B C
    0x5B,  # 2 - A B D E G
    0x4F,  # 3 - A B C D G
    0x66,  # 4 - B C F G
    0x6D,  # 5 - A C D F G
    0x7D,  # 6 - A C D E F G
    0x07,  # 7 - A B C
    0x7F,  # 8 - A B C D E F G
    0x6F   # 9 - A B C D F G
]

# ============================================================================
# FUNCIÓN PARA ENVIAR BYTE AL 74HC595
# ============================================================================

def enviar_byte(valor):
    """
    Envía un byte al 74HC595 de forma serie.
    
    Funcionamiento:
    1. Poner STCP en bajo para mantener el latch inactivo
    2. Enviar 8 bits (de MSB a LSB)
    3. Para cada bit:
       - Establecer el bit en DS
       - Pulsar SHCP para desplazar
    4. Poner STCP en alto para actualizar las salidas Q0-Q7
    
    Argumentos:
        valor: Byte a enviar (0-255)
    """
    # Mantener el latch inactivo durante el envío
    STCP.value(0)
    
    # Enviar 8 bits, comenzando por el más significativo (MSB)
    for i in range(8):
        # Extraer el bit i (de izquierda a derecha)
        # Desplazamos (7 - i) posiciones y hacemos AND con 1
        bit = (valor >> (7 - i)) & 1
        
        # Establecer el bit en la línea de datos
        DS.value(bit)
        
        # Pulsar el reloj de desplazamiento
        SHCP.value(1)
        time.sleep_us(1)  # Pequeño retardo para estabilidad
        SHCP.value(0)
    
    # Activar el latch para actualizar las salidas Q0-Q7
    STCP.value(1)
    time.sleep_us(1)
    STCP.value(0)


# ============================================================================
# PROGRAMA PRINCIPAL - MOSTRAR NÚMEROS 0-9
# ============================================================================

def modo_contador_ascendente():
    """
    Modo simple: muestra números del 0 al 9 de forma cíclica.
    Cada número se muestra durante 1 segundo.
    """
    print("Modo: Contador ascendente (0-9)")
    
    while True:
        for numero in numeros:
            enviar_byte(numero)
            time.sleep(1)  # Esperar 1 segundo


# ============================================================================
# VERSIÓN ALTERNATIVA - CUENTA REGRESIVA (9 A 0)
# ============================================================================

def modo_contador_descendente():
    """
    Modo alternativo: cuenta regresiva de 9 a 0.
    Cada número se muestra durante 1 segundo.
    """
    print("Modo: Contador descendente (9-0)")
    
    while True:
        # Recorrer los números en orden inverso
        for i in range(9, -1, -1):
            enviar_byte(numeros[i])
            time.sleep(1)  # Esperar 1 segundo


# ============================================================================
# NOTA SOBRE PANTALLAS DE ÁNODO COMÚN
# ============================================================================

"""
ADAPTACIÓN PARA PANTALLAS DE ÁNODO COMÚN:

Si tu pantalla de 7 segmentos es de ÁNODO COMÚN en lugar de cátodo común,
necesitas invertir los bits. Esto se hace restando el valor de 255 (0xFF).

En una pantalla de ánodo común:
- 1 lógico = segmento APAGADO
- 0 lógico = segmento ENCENDIDO

Modificación necesaria:
    enviar_byte(255 - numero)  # Invertir los bits

Ejemplo para modo ascendente con ánodo común:
    for numero in numeros:
        enviar_byte(255 - numero)  # Invertir bits
        time.sleep(1)

Ejemplo para modo descendente con ánodo común:
    for i in range(9, -1, -1):
        enviar_byte(255 - numeros[i])  # Invertir bits
        time.sleep(1)
"""


# ============================================================================
# EJECUCIÓN DEL PROGRAMA
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("Proyecto 14.1 - Pantalla de 7 segmentos con 74HC595")
    print("ESP32-S3 WROOM + MicroPython")
    print("=" * 60)
    print()
    
    try:
        # Ejecutar el modo contador ascendente
        # Para cambiar a contador descendente, comentar la línea siguiente
        # y descomentar la siguiente
        
        modo_contador_ascendente()
        
        # modo_contador_descendente()  # Descomenta para contador descendente
        
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
        # Limpiar: apagar todos los segmentos
        enviar_byte(0x00)
    except Exception as e:
        print(f"Error: {e}")
        enviar_byte(0x00)


# ============================================================================
# FUNCIONES ADICIONALES
# ============================================================================

def mostrar_numero_especifico(numero):
    """
    Muestra un número específico (0-9) en la pantalla.
    
    Argumentos:
        numero: Número a mostrar (0-9)
    """
    if 0 <= numero <= 9:
        enviar_byte(numeros[numero])
    else:
        print(f"Error: el número debe estar entre 0 y 9")


def apagar_display():
    """
    Apaga todos los segmentos del display.
    """
    enviar_byte(0x00)


def test_display():
    """
    Función de prueba: enciende todos los segmentos durante 2 segundos.
    """
    print("Prueba: encendiendo todos los segmentos...")
    enviar_byte(0xFF)  # Todos los bits a 1
    time.sleep(2)
    enviar_byte(0x00)  # Todos los bits a 0
    print("Prueba completada.")


# ============================================================================
# NOTAS TÉCNICAS
# ============================================================================

"""
FUNCIONAMIENTO DEL 74HC595:

El 74HC595 es un registro de desplazamiento de 8 bits. Funciona así:

1. Los datos se envían bit a bit por la línea DS (Data)
2. SHCP (Shift Clock) desplaza los bits dentro del registro
3. Después de enviar 8 bits, STCP (Storage Clock/Latch) actualiza Q0-Q7
4. OE debe estar a GND para habilitar las salidas

Secuencia de envío:
- STCP = 0 (latch inactivo)
- Para cada uno de los 8 bits:
  - Colocar bit en DS
  - Pulsar SHCP (0->1->0)
- STCP = 1 (latch activo, actualiza salidas)
- STCP = 0 (vuelve a inactivo)

CÁLCULO DE PATRONES:

Los patrones se calculan encendiendo los segmentos necesarios.
Ejemplo para el número 0 (A B C D E F encendidos):

   A=Q0  B=Q1  C=Q2  D=Q3  E=Q4  F=Q5  G=Q6  DP=Q7
    1     1     1     1     1     1     0     0
    
Binario: 00111111 = 0x3F en hexadecimal

RESISTENCIAS:

Cada segmento lleva una resistencia de 220Ω en serie.
Esto limita la corriente a aproximadamente:
I = (3.3V - Vled) / 220Ω ≈ 10 mA por segmento

Total máximo: 80 mA (con todos los segmentos encendidos)
"""
