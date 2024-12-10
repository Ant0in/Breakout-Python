

class Score:

    def __init__(self, init_val: float = 0.0) -> None:
        self._value: float = init_val

    def getValue(self) -> float:
        return self._value
    
    def setValue(self, v: float) -> None:
        self._value = v

    def addScore(self, increment: float | int) -> None:
        new_value: float = self.getValue() + increment
        self.setValue(v=new_value)

    def __repr__(self):
        return f'[i] Score : {self.getValue()}'
    
