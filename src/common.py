
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
    _NONE       = 0
    WHITE       = 1
    ORANGE      = 2
    CYAN        = 3
    GREEN       = 4
    RED         = 5
    BLUE        = 6
    MAGENTA     = 7
    YELLOW      = 8
    SILVER      = 9
    GOLD        = 10


class Action(Enum):
    _NONE = 0
    LEFT = 1
    RIGHT = 2

