from . import ioManager
from . import device
from . import pin
from . import debounce
import time


def test_manager():
    manager = ioManager.IoManager(10)

    dev = device.Device()

    out = pin.OutputPin(1, debounce.Debouncer(0, 0, 1), dev)
    out.setup()

    global currentValue
    currentValue = 0

    def notify_me(value):
        global currentValue
        currentValue = value
        if value > 10:
            currentValue = (15/0)

    manager.registerPin(out, notify_me)

    manager.startThread()
    time.sleep(0.02)
    out.set(1)
    time.sleep(0.02)
    assert currentValue == 1
    out.set(0)
    time.sleep(0.02)
    assert currentValue == 0

    assert manager.lastError == ""

    out.set(11)
    time.sleep(0.02)
    assert len(manager.lastError) > 0

    manager.stopThread()
