from . import device


class Pin:
    def __init__(self, id, debouncer, device) -> None:
        self.id = id
        self.debouncer = debouncer
        self.device = device
        self._oldValue = 0
        self.last_update = 0

    def setup(self, mode=device.NONE):
        self.device.setup(self.id, mode)

    def _updatePinOnDeviceFunction(self):
        self.device.update(self.id)

    def _setPinOnDeviceFunction(self):
        self.device.set(self.id, self.get())

    def _getFromDeviceFunction(self):
        return self.device.get(self.id)

    def update(self, currentTime):
        self.last_update = currentTime
        currentValue = self.get()
        if currentValue == self._oldValue:
            return False
        self._oldValue = currentValue
        return True

    def get(self):
        return self.debouncer.get()

    def set(self, value):
        pass


class InputPin(Pin):
    def __init__(self, id, debouncer, device) -> None:
        super().__init__(id, debouncer, device)

    def setup(self):
        return super().setup(device.INPUT)

    def update(self, currentTime):
        self.debouncer.updateValueIfNeed(currentTime, self._updatePinOnDeviceFunction)  # function is executed inside
        self.debouncer.addToBufferIfNeed(currentTime, self._getFromDeviceFunction())  # get executed here
        return super().update(currentTime)


class OutputPin(Pin):
    def __init__(self, id, debouncer, device) -> None:
        super().__init__(id, debouncer, device)
        self._lastOutValue = 0

    def setup(self):
        return super().setup(device.OUTPUT)

    def update(self, currentTime):
        self.debouncer.addToBufferIfNeed(currentTime, self._lastOutValue)
        self.debouncer.updateValueIfNeed(currentTime, self._setPinOnDeviceFunction)  # function is executed inside
        return super().update(currentTime)

    def set(self, value):
        self._lastOutValue = value

class GroupPin:
    def __init__(self, pins) -> None:
        self.pins = pins

    def setup(self):
        for pin in self.pins:
            pin.setup()

    def update(self, currentTime):
        return any([pin.update(currentTime) for pin in self.pins])

    def get(self):
        pass

    def set(self, value):
        pass

class GroupVecPin(GroupPin):
    def __init__(self, pins) -> None:
        super().__init__(pins)

    def get(self):
        return [pin.get() for pin in self.pins]

    def set(self, value):
        if len(value) > len(self.pins):
            raise Exception("More values than pins")
        for i in range(len(value)):
            self.pins[i].set(value[i])

class GroupBinPin(GroupPin):
    def __init__(self, pins) -> None:
        super().__init__(pins)

    def get(self):
        value = 0
        for pin in self.pins[::-1]:
            value = value*2 + pin.get()
        return value

    def set(self, value):
        i = 0
        while value > 0:
            if i >= len(self.pins):
                raise Exception("More values than pins")
            self.pins[i].set(value&1)
            value = value//2


class GroupBinGrayPin(GroupBinPin):
    def __init__(self, pins) -> None:
        super().__init__(pins)

    @staticmethod
    def intFromGray(value):
        value ^= value >> 16
        value ^= value >> 8
        value ^= value >> 4
        value ^= value >> 2
        value ^= value >> 1
        return value

    @staticmethod
    def intToGray(value):
        value ^= value << 1
        value ^= value << 2
        value ^= value << 4
        value ^= value << 8
        value ^= value << 16
        return value

    def get(self):
        value = super().get()
        return GroupBinGrayPin.intFromGray(value)

    def set(self, value):
        grayValues = GroupBinGrayPin.intToGray(value)
        super().set(grayValues)
