import time
from machine import I2C, Pin

# Configuración de pines I2C para ESP32-S3
SDA_PIN = 14
SCL_PIN = 13
I2C_FREQ = 400000
LCD_COLUMNS = 16
LCD_ROWS = 2

# Constantes del controlador HD44780/I2C PCF8574
LCD_BACKLIGHT = 0x08
LCD_ENABLE = 0x04
LCD_READ_WRITE = 0x02
LCD_REGISTER_SELECT = 0x01

LCD_CMD_CLEAR = 0x01
LCD_CMD_HOME = 0x02
LCD_CMD_ENTRY_MODE = 0x04
LCD_CMD_DISPLAY_CONTROL = 0x08
LCD_CMD_FUNCTION_SET = 0x20
LCD_CMD_SET_DDRAM = 0x80

LCD_ENTRY_LEFT = 0x02
LCD_ENTRY_SHIFT_DECREMENT = 0x00
LCD_DISPLAY_ON = 0x04
LCD_CURSOR_OFF = 0x00
LCD_BLINK_OFF = 0x00
LCD_2LINE = 0x08
LCD_5x8DOTS = 0x00


def create_i2c():
    """Crea el bus I2C en los pines especificados."""
    return I2C(0, scl=Pin(SCL_PIN), sda=Pin(SDA_PIN), freq=I2C_FREQ)


class I2cLcd:
    def __init__(self, i2c, addr, rows, cols):
        self.i2c = i2c
        self.addr = addr
        self.rows = rows
        self.cols = cols
        self.backlight = LCD_BACKLIGHT
        self._init_lcd()

    def _write_byte(self, data):
        self.i2c.writeto(self.addr, bytes([data | self.backlight]))

    def _pulse_enable(self, data):
        self._write_byte(data | LCD_ENABLE)
        time.sleep_us(1)
        self._write_byte(data & ~LCD_ENABLE)
        time.sleep_us(50)

    def _write4bits(self, data):
        self._write_byte(data)
        self._pulse_enable(data)

    def _send(self, value, mode=0):
        high = value & 0xF0
        low = (value << 4) & 0xF0
        self._write4bits(high | mode)
        self._write4bits(low | mode)

    def _init_lcd(self):
        # Inicialización según documentación del módulo I2C
        time.sleep_ms(50)
        self._write4bits(0x30)
        time.sleep_ms(5)
        self._write4bits(0x30)
        time.sleep_us(150)
        self._write4bits(0x30)
        self._write4bits(0x20)

        self._send(LCD_CMD_FUNCTION_SET | LCD_2LINE | LCD_5x8DOTS)
        self._send(LCD_CMD_DISPLAY_CONTROL | LCD_DISPLAY_ON | LCD_CURSOR_OFF | LCD_BLINK_OFF)
        self.clear()
        self._send(LCD_CMD_ENTRY_MODE | LCD_ENTRY_LEFT | LCD_ENTRY_SHIFT_DECREMENT)
        self.home()

    def clear(self):
        self._send(LCD_CMD_CLEAR)
        time.sleep_ms(2)

    def home(self):
        self._send(LCD_CMD_HOME)
        time.sleep_ms(2)

    def move_to(self, col, row):
        row_offsets = [0x00, 0x40, 0x14, 0x54]
        if row >= self.rows:
            row = self.rows - 1
        self._send(LCD_CMD_SET_DDRAM | (col + row_offsets[row]))

    def putstr(self, string):
        for char in string:
            self._send(ord(char), LCD_REGISTER_SELECT)

    def print_line(self, text, row):
        self.move_to(0, row)
        text = text.ljust(self.cols)[: self.cols]
        self.putstr(text)


def scan_i2c_devices(i2c):
    """Escanea el bus I2C y devuelve la lista de direcciones encontradas."""
    try:
        devices = i2c.scan()
        return devices
    except OSError as e:
        print("Error al escanear I2C:", e)
        return []


def main():
    print("Iniciando programa LCD1602 I2C")
    i2c = create_i2c()
    devices = scan_i2c_devices(i2c)

    if not devices:
        print("No se encontró ningún dispositivo I2C.")
        return

    print("Dispositivos I2C detectados:")
    for device in devices:
        print(" -", hex(device))

    lcd_addr = devices[0]
    print("Usando dirección I2C:", hex(lcd_addr))

    try:
        lcd = I2cLcd(i2c, lcd_addr, LCD_ROWS, LCD_COLUMNS)
    except OSError as e:
        print("Error al inicializar la LCD:", e)
        return

    lcd.clear()
    lcd.print_line("Hello World", 0)

    counter = 0
    while True:
        try:
            lcd.print_line("Contador: {:<6}".format(counter), 1)
            counter += 1
            time.sleep(1)
        except OSError as e:
            print("Error de comunicación I2C:", e)
            lcd.clear()
            lcd.print_line("ERROR I2C", 0)
            lcd.print_line("Reinicie board", 1)
            break
        except Exception as e:
            print("Error inesperado:", e)
            lcd.clear()
            lcd.print_line("ERROR", 0)
            lcd.print_line(str(e)[:LCD_COLUMNS], 1)
            break


if __name__ == "__main__":
    main()
