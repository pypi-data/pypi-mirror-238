from .device import Device
from .parser import Parser


def test_device():  # TODO: test i2c and gpio devices
    parser = Parser()
    sim = parser.getDevice("sim")

    assert isinstance(sim, Device)


def test_pin():
    parser = Parser()
    inp = parser.getPin("input-10,0-0-1,sim")
    out = parser.getPin("output-11,0-0-1,sim")
    #group-vec(input-10,0-0-1,sim|input-11,0-0-1,sim)"
    #group-bin(input-10,0-0-1,sim|input-11,0-0-1,sim)"
    #group-bin-gray(input-10,0-0-1,sim|input-11,0-0-1,sim)"
#    assert isinstance(inp, pin.InputPin) # TODO:Resolve this

#    assert isinstance(out, pin.OutputPin)

    assert inp.id == 10
    assert out.id == 11

    assert out.device == inp.device

    inpDeb = inp.debouncer
    outDeb = out.debouncer

    assert inpDeb == parser.getDebouncer("0-0-1")
    assert outDeb == parser.getDebouncer("0-0-1")


def test_debouncer():
    parser = Parser()
    deb = parser.getDebouncer("0-0-1")

    assert deb.addPeriod == 0
    assert deb.updatePeriod == 0
    assert deb.block.blockSize == 1






