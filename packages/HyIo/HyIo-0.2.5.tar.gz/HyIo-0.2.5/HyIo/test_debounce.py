from . import debounce


def test_block():
    for window in range(1, 100):
        block = debounce.Block(window)
        for i in range(1, 1000):
            block.add(i)

            currentLen = min(i, window)
            currentSum = ((i - (currentLen-1)) + i)*currentLen/2
            avg = currentSum / window
            assert avg == block.get()


def test_debouncer():
    def functor(*args):
        pass
    debouncer = debounce.Debouncer(10, 10, 1)

    for curTime in range(0, 10):
        assert not debouncer.updateValueIfNeed(curTime, functor)
    assert debouncer.updateValueIfNeed(10, functor)
    for curTime in range(11, 20):
        assert not debouncer.updateValueIfNeed(curTime, functor)

    for curTime in range(0, 10):
        assert not debouncer.addToBufferIfNeed(curTime, curTime)
    assert debouncer.addToBufferIfNeed(10, 10)
    assert debouncer.get() == 10
    for curTime in range(11, 20):
        assert not debouncer.addToBufferIfNeed(curTime, curTime)
        assert debouncer.get() == 10
