
from enum import Enum



class Position2D:

    def __init__(self, x: float, y: float) -> None:
       
        self._x: float = x
        self._y: float = y

    def getX(self) -> float:
        return self._x
    
    def getY(self) -> float:
        return self._y
    
    def coords(self) -> tuple[float, float]:
        return self.x, self.y

    def __repr__(self) -> str:
        return f'{self.coords}'
    

class BrickType(Enum):
    BLANC = 1
    ORANGE = 2
    CYAN = 3
    VERT = 4
    ROUGE = 5
    BLEU = 6
    MAGENTA = 7
    JAUNE = 8
    ARGENT = 9
    OR = 10

