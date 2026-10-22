import bluetooth
import struct
from machine import Pin

rele = Pin(22, Pin.OUT)
rele.value(0)
in1 = Pin(12, Pin.OUT)
in2 = Pin(13, Pin.OUT)


in1.value(1)
in2.value(1)
rele.value(1)

SERVICE_UUID = bluetooth.UUID(
    "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
)

RX_UUID = bluetooth.UUID(
    "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
)

TX_UUID = bluetooth.UUID(
    "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"
)

RX_FLAGS = bluetooth.FLAG_WRITE
TX_FLAGS = bluetooth.FLAG_NOTIFY

_IRQ_CENTRAL_CONNECT = 1
_IRQ_CENTRAL_DISCONNECT = 2
_IRQ_GATTS_WRITE = 3

class LightControlBLE:

    def __init__(self):

        self.ble = bluetooth.BLE()

        self.ble.active(True)

        self.connections = set()

        services = (
            (
                SERVICE_UUID,
                (
                    (TX_UUID, TX_FLAGS),
                    (RX_UUID, RX_FLAGS),
                ),
            ),
        )

        (
            (
                self.tx_handle,
                self.rx_handle,
            ),
        ) = self.ble.gatts_register_services(services)

        print("BLE service registered")

        print("TX handle:", self.tx_handle)
        print("RX handle:", self.rx_handle)

        self.ble.irq(self.irq)

        self.advertise()

    def irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:

            conn_handle, addr_type, addr = data

            self.connections.add(conn_handle)

            print()
            print("==============================")
            print("BLE CONNECTED")
            print("Connection:", conn_handle)
            print("==============================")
            print()

        elif event == _IRQ_CENTRAL_DISCONNECT:

            conn_handle, addr_type, addr = data

            if conn_handle in self.connections:
                self.connections.remove(conn_handle)

            print()
            print("==============================")
            print("BLE DISCONNECTED")
            print("==============================")
            print()

            self.advertise()

        elif event == _IRQ_GATTS_WRITE:

            conn_handle, attr_handle = data

            if attr_handle == self.rx_handle:

                try:

                    data = self.ble.gatts_read(
                        self.rx_handle
                    )

                    command = data.decode("utf-8").strip().lower()

                    print("Received:", command)

                    self.process_command(command)

                except Exception as e:

                    print("BLE receive error:", e)

    def process_command(self, command):

        if command == "1on":

            in1.value(0)

            print("Lamp 1 -> ON")

            self.notify("lamp1_on")

        elif command == "1off":

            in1.value(1)

            print("Lamp 1 -> OFF")

            self.notify("lamp1_off")

        elif command == "2on":

            in2.value(0)

            print("Lamp 2 -> ON")

            self.notify("lamp2_on")

        elif command == "2off":

            in2.value(1)

            print("Lamp 2 -> OFF")

            self.notify("lamp2_off")

        elif command == "0on":

            in1.value(0)
            in2.value(0)

            print("Both lamps -> ON")

            self.notify("both_on")

        elif command == "0off":

            in1.value(1)
            in2.value(1)

            print("Both lamps -> OFF")

            self.notify("both_off")

        elif command == "status":

            lamp1 = in1.value() == 0
            lamp2 = in2.value() == 0

            status = "L1=" + str(lamp1) + ",L2=" + str(lamp2)

            print("Status:", status)

            self.notify(status)

        else:

            print("Unknown command:", command)

            self.notify("unknown_command")

    def notify(self, message):

        data = message.encode("utf-8")

        for conn_handle in self.connections:

            try:

                self.ble.gatts_notify(
                    conn_handle,
                    self.tx_handle,
                    data
                )

                print("Notification:", message)

            except Exception as e:

                print("Notify error:", e)

    def advertise(self):

        name = b"LightControl"

        payload = bytearray()

        payload += struct.pack(
            "BB",
            2,
            0x01
        )

        payload += b"\x06"

        payload += struct.pack(
            "BB",
            len(name) + 1,
            0x09
        )

        payload += name

        service_uuid = bytes(SERVICE_UUID)

        payload += struct.pack(
            "BB",
            len(service_uuid) + 1,
            0x07
        )

        payload += service_uuid

        self.ble.gap_advertise(
            100000,
            adv_data=payload
        )

        print("BLE advertising...")
        print("Device name: LightControl")

ble = LightControlBLE()

print()
print("==============================")
print("LightControl BLE Started")
print("==============================")
print("use these commands in nRF app:")
print("  keyoneon")
print("  keyoneoff")
print("  keytwoon")
print("  keytwooff")
print("  bothon")
print("  bothoff")
print("  status")
print()

while True:
    pass