from . import device

import wiringpi as wp


class GPIODevice(device.Device):
    def __init__(self) -> None:
        super().__init__()
        wp.wiringPiSetupGpio()

    def update(self, id):
        if self.pins[id] == device.INPUT:
            self.data[id] = wp.digitalRead(id)
        else:
            wp.digitalWrite(id, self.data[id])

    def setup(self, id, mode):
        if mode == device.INPUT:
            wp.pinMode(id, 0)
        else:
            wp.pinMode(id, 1)
        return super().setup(id, mode)
