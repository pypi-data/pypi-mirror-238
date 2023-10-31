import smbus2
from . import device

class I2CDevice(device.Device):
    def __init__(self, address) -> None:
        super().__init__()
        self.bus = smbus2.SMBus(1)
        self.address = address

    def _read_pin(self, id):
        return self.bus.read_byte_data(self.address, id)

    def _write_pin(self, id, value):
        self.bus.write_byte_data(self.address, id, value)

    def update(self, id):
        if self.pins[id] == device.INPUT:
            self.data[id] = self._read_pin(id)
        else:
            self._write_pin(id, self.data[id])
