from machine import Pin, PWM
import time

# Configuración de los canales PWM del LED RGB
# GPIO 42 para rojo, GPIO 41 para verde, GPIO 40 para azul
rojo = PWM(Pin(42))
verde = PWM(Pin(41))
azul = PWM(Pin(40))

# Frecuencia PWM en Hz
rojo.freq(1000)
verde.freq(1000)
azul.freq(1000)


def convertir_8bits_a_pwm(valor):
    """Convierte un valor de color de 0-255 a 0-65535 para MicroPython."""
    return int(valor) * 257


def aplicar_color(r, g, b):
    """Aplica un color RGB al LED usando duty_u16()."""
    rojo.duty_u16(convertir_8bits_a_pwm(r))
    verde.duty_u16(convertir_8bits_a_pwm(g))
    azul.duty_u16(convertir_8bits_a_pwm(b))


def rueda_color(posicion):
    """Convierte un valor entre 0 y 255 en un color RGB suave."""
    posicion = int(posicion) % 256

    if posicion < 43:
        # De rojo a amarillo: rojo 255, verde sube de 0 a 255
        r = 255
        g = posicion * 6
        b = 0
    elif posicion < 86:
        # De amarillo a verde: rojo baja de 255 a 0, verde 255
        posicion -= 43
        r = 255 - posicion * 6
        g = 255
        b = 0
    elif posicion < 129:
        # De verde a cian: verde 255, azul sube de 0 a 255
        posicion -= 86
        r = 0
        g = 255
        b = posicion * 6
    elif posicion < 172:
        # De cian a azul: verde baja de 255 a 0, azul 255
        posicion -= 129
        r = 0
        g = 255 - posicion * 6
        b = 255
    elif posicion < 215:
        # De azul a magenta: azul 255, rojo sube de 0 a 255
        posicion -= 172
        r = posicion * 6
        g = 0
        b = 255
    else:
        # De magenta a rojo: rojo 255, azul baja de 255 a 0
        posicion -= 215
        r = 255
        g = 0
        b = 255 - posicion * 6

    # Asegura que los valores queden dentro de 0-255
    return max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))


def main():
    """Bucle principal que recorre la rueda de color sin fin."""
    while True:
        for posicion in range(256):
            r, g, b = rueda_color(posicion)
            aplicar_color(r, g, b)
            time.sleep(0.02)


if __name__ == "__main__":
    main()
