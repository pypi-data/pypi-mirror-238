

class Block:
    def __init__(self, blockSize) -> None:
        self.blockSize = blockSize
        self.currentIndex = 0
        self.block = [0] * self.blockSize
        self.currentSum = 0

    def add(self, value):
        self.currentSum -= self.block[self.currentIndex]
        self.block[self.currentIndex] = value
        self.currentSum += self.block[self.currentIndex]
        self.currentIndex = (self.currentIndex + 1) % self.blockSize

    def get(self):
        return self.currentSum/self.blockSize


class Debouncer:
    def __init__(self, updatePeriod, addPeriod, blockSize) -> None:
        self.updatePeriod = updatePeriod
        self.lastUpdateTime = 0

        self.addPeriod = addPeriod
        self.lastAddTime = 0

        self.block = Block(blockSize)

    def __eq__(self, deb):
        if self.updatePeriod != deb.updatePeriod:
            return False
        if self.addPeriod != deb.addPeriod:
            return False
        return self.block.blockSize == deb.block.blockSize

    def get(self):
        return self.block.get()

    def updateValueIfNeed(self, currentTime, func):
        if currentTime - self.lastUpdateTime < self.updatePeriod:
            return False
        func()
        self.lastUpdateTime = currentTime
        return True

    def addToBufferIfNeed(self, currentTime, value):
        if currentTime - self.lastAddTime < self.addPeriod:
            return False
        self.block.add(value)
        self.lastAddTime = currentTime
        return True
