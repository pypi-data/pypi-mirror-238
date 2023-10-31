from . import device


def test_device():
    dev = device.Device()

    dev.setup(1, device.INPUT)
    dev.setup(2, device.OUTPUT)
    dev.setup(3, device.INPUT)
    dev.setup(4, device.OUTPUT)

    for inp in [1, 3]:
        assert dev.get(inp) == 0
        dev.set(inp, 1)
        assert dev.get(inp) == 0
    for out in [2, 4]:
        assert dev.get(out) == 0
        dev.set(out, 1)
        assert dev.get(out) == 1
