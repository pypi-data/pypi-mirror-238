from . import pin
from . import device
from . import debounce


def test_pin():
    dev = device.Device()

    inp = pin.InputPin(1, debounce.Debouncer(0, 0, 1), dev)
    inp.setup()

    out = pin.OutputPin(2, debounce.Debouncer(0, 0, 1), dev)
    out.setup()

    inp.update(1)
    assert inp.get() == 0
    dev.set(inp.id, 1)
    inp.update(2)
    assert inp.get() == 0

    out.update(1)
    assert out.get() == 0
    out.set(1)
    out.update(2)
    assert out.get() == 1
