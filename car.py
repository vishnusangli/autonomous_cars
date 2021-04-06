class Thing: #Most basic controllable car, a rectangle without wheels
    def __init__(self) -> None:
        pass

class Car(Thing):
    def __init__(self) -> None:
        super().__init__()

class Wheel:
    def __init__(self) -> None:
        pass
