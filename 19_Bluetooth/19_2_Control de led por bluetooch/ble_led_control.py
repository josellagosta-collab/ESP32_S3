"""
Control de LED por Bluetooth Low Energy para ESP32-S3 en MicroPython.

Comandos desde el móvil:
ON      -> enciende el LED
OFF     -> apaga el LED
STATUS  -> devuelve el estado del LED
"""

import time
from micropython import const
import bluetooth
from machine import Pin


# UUID Nordic UART Service
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")


# Flags BLE
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)


# Eventos BLE para MicroPython
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)


LED_PIN = 2  # Cambia este GPIO si tu placa usa otro pin para el LED.


class BLELEDController:
    def __init__(self, ble, led_pin=LED_PIN, name="ESP32"):
        self._ble = ble
        self._name = name
        self._led = Pin(led_pin, Pin.OUT)

        self._connections = set()
        self._connected = False

        self._ble.active(True)
        self._ble.irq(self._irq)

        uart_service = (
            _UART_SERVICE_UUID,
            (
                (_UART_TX_UUID, _FLAG_NOTIFY),
                (_UART_RX_UUID, _FLAG_WRITE | _FLAG_WRITE_NO_RESPONSE),
            ),
        )

        ((self._tx_handle, self._rx_handle),) = self._ble.gatts_register_services(
            (uart_service,)
        )

        self._advertise()
        print("[BLE] Servicio LED preparado")

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self._connected = True
            print("[BLE] Conectado. Handle:", conn_handle)
            time.sleep_ms(300)
            self.send("LED controller conectado")

        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.discard(conn_handle)
            self._connected = False
            print("[BLE] Desconectado. Handle:", conn_handle)
            time.sleep_ms(500)
            self._advertise()

        elif event == _IRQ_GATTS_WRITE:
            conn_handle, attr_handle = data
            if attr_handle == self._rx_handle:
                self._handle_rx()

    def _advertise(self):
        payload = advertising_payload(
            name=self._name,
            services=[_UART_SERVICE_UUID]
        )

        print("[BLE] Tamaño payload:", len(payload), "bytes")

        self._ble.gap_advertise(None)
        time.sleep_ms(100)
        self._ble.gap_advertise(100_000, adv_data=payload)

        print("[BLE] Publicidad iniciada con nombre:", self._name)

    def _handle_rx(self):
        data = self._ble.gatts_read(self._rx_handle)

        try:
            command = data.decode("utf-8").strip().upper()
        except UnicodeError:
            command = ""

        if not command:
            return

        print("[BLE] Comando recibido:", command)

        if command == "ON":
            self._led.on()
            print("[LED] Encendido")
            self.send("LED ON")

        elif command == "OFF":
            self._led.off()
            print("[LED] Apagado")
            self.send("LED OFF")

        elif command == "STATUS":
            status = "ON" if self._led.value() else "OFF"
            print("[LED] Estado:", status)
            self.send("STATUS: " + status)

        else:
            print("[BLE] Comando desconocido")
            self.send("Comando no reconocido. Usa ON, OFF o STATUS")

    def send(self, data):
        if not self._connected:
            print("[BLE] Sin conexión activa")
            return

        if isinstance(data, str):
            data = data.encode("utf-8")

        for conn_handle in self._connections:
            try:
                self._ble.gatts_notify(conn_handle, self._tx_handle, data)
                print("[BLE] Enviado:", data)
            except OSError as e:
                print("[BLE] Error enviando notificación:", e)


def advertising_payload(name=None, services=None):
    payload = bytearray()

    # Flags BLE generales
    payload += bytes((2, 0x01, 0x06))

    # Nombre BLE
    if name:
        name_bytes = name.encode("utf-8")
        payload += bytes((len(name_bytes) + 1, 0x09)) + name_bytes

    # Servicios BLE
    if services:
        for uuid in services:
            uuid_bytes = bytes(uuid)

            if len(uuid_bytes) == 16:
                payload += bytes((17, 0x07)) + uuid_bytes
            elif len(uuid_bytes) == 2:
                payload += bytes((3, 0x03)) + uuid_bytes

    if len(payload) > 31:
        raise ValueError("El advertising payload BLE supera los 31 bytes")

    return payload


def main():
    ble = bluetooth.BLE()
    controller = BLELEDController(ble, led_pin=LED_PIN, name="ESP32")

    print("[Sistema] Esperando comandos BLE: ON, OFF o STATUS")

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()