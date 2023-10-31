INPUT = "input"
OUTPUT = "output"
NONE = "none"


class Device:
    def __init__(self) -> None:
        self.data = {}
        self.pins = {}

    def setup(self, id, mode):
        self.pins[id] = mode
        self.data[id] = 0

    def update(self, id):  # set self.data[id] to hardware
        pass

    def set(self, id, value):
        if self.pins[id] == OUTPUT:
            self.data[id] = value

    def get(self, id):
        return self.data[id]
