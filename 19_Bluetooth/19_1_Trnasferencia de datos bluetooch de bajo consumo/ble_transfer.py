"""
Programa MicroPython BLE para ESP32-S3.
Permite recibir texto desde un móvil y enviar mensajes al móvil.
Compatible con Nordic UART Service.
"""

import time
from micropython import const
import bluetooth


# UUID del servicio Nordic UART Service
_UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
_UART_TX_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")  # Notify ESP32 -> móvil
_UART_RX_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")  # Write móvil -> ESP32


# Flags BLE
_FLAG_READ = const(0x0002)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)


# Eventos BLE
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)


class BLEUART:
    def __init__(self, ble, name="ESP32"):
        self._ble = ble
        self._name = name

        self._ble.active(True)
        self._ble.irq(self._irq)

        self._connections = set()
        self._connected = False

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

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            self._connected = True
            print("[BLE] Conectado. Handle:", conn_handle)

            time.sleep_ms(300)
            self.send("ESP32-S3 BLE conectado")

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
                self._on_rx(conn_handle)

    def _advertise(self):
        payload = self._advertising_payload(
            name=self._name,
            services=[_UART_SERVICE_UUID]
        )

        print("[BLE] Tamaño payload:", len(payload), "bytes")

        self._ble.gap_advertise(None)
        time.sleep_ms(100)

        self._ble.gap_advertise(100_000, adv_data=payload)

        print("[BLE] Publicidad iniciada. Nombre:", self._name)

    def _advertising_payload(self, name=None, services=None):
        payload = bytearray()

        # Flags BLE generales
        payload += bytes((2, 0x01, 0x06))

        # Nombre del dispositivo
        if name:
            name_bytes = name.encode("utf-8")
            payload += bytes((len(name_bytes) + 1, 0x09)) + name_bytes

        # UUIDs de servicios
        if services:
            for uuid in services:
                uuid_bytes = bytes(uuid)

                if len(uuid_bytes) == 16:
                    payload += bytes((17, 0x07)) + uuid_bytes
                elif len(uuid_bytes) == 2:
                    payload += bytes((3, 0x03)) + uuid_bytes

        if len(payload) > 31:
            print("[BLE] Aviso: payload demasiado grande:", len(payload), "bytes")
            print("[BLE] Prueba con un nombre más corto.")
            raise ValueError("El advertising payload supera 31 bytes")

        return payload

    def _on_rx(self, conn_handle):
        data = self._ble.gatts_read(self._rx_handle)

        try:
            text = data.decode("utf-8").strip()
        except UnicodeError:
            text = repr(data)

        print("[BLE] Recibido:", text)

        if text:
            respuesta = "Eco: " + text
            self.send(respuesta)

    def send(self, data):
        if not self._connected:
            print("[BLE] No hay conexión activa")
            return

        if isinstance(data, str):
            data = data.encode("utf-8")

        for conn_handle in self._connections:
            try:
                self._ble.gatts_notify(conn_handle, self._tx_handle, data)
                print("[BLE] Enviado:", data)
            except OSError as e:
                print("[BLE] Error enviando notificación:", e)


def main():
    ble = bluetooth.BLE()

    # Nombre corto para evitar OSError -18
    uart = BLEUART(ble, name="ESP32")

    contador = 0

    while True:
        if uart._connected:
            contador += 1
            uart.send("Mensaje ESP32-S3 nº " + str(contador))

        time.sleep(10)


if __name__ == "__main__":
    main()