

from enum import Enum


INFINITY: float = float('inf')


class Position2D:

    def __init__(self, x: float, y: float) -> None:
       
        self._x: float = x
        self._y: float = y

    def getX(self) -> float:
        return self._x
    
    def getY(self) -> float:
        return self._y
    
    def coords(self) -> tuple[float, float]:
        return self.getX(), self.getY()

    def __repr__(self) -> str:
        return f'{self.coords()}'
    
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

class WallType(Enum):
    _NONE = 0
    LEFT = 1
    RIGHT = 2
    BOTTOM = 3
    TOP = 4


BRICK_COLORS: dict = {
    BrickType._NONE: "#000000",         # - filler -
    BrickType.WHITE: "#FFFFFF",         # Blanc
    BrickType.ORANGE: "#FFA500",        # Orange
    BrickType.CYAN: "#00FFFF",          # Cyan
    BrickType.GREEN: "#008000",         # Vert
    BrickType.RED: "#FF0000",           # Rouge
    BrickType.BLUE: "#0000FF",          # Bleu
    BrickType.MAGENTA: "#FF00FF",       # Magenta
    BrickType.YELLOW: "#FFFF00",        # Jaune
    BrickType.SILVER: "#C0C0C0",        # Argent
    BrickType.GOLD: "#FFD700",          # Or
}
BRICK_HP: dict = {
    BrickType._NONE: None,
    BrickType.WHITE: 1,
    BrickType.ORANGE: 1,
    BrickType.CYAN: 1,
    BrickType.GREEN: 1,
    BrickType.RED: 1,
    BrickType.BLUE: 1,
    BrickType.MAGENTA: 1,
    BrickType.YELLOW: 1,
    BrickType.SILVER: 2,
    BrickType.GOLD: INFINITY
}
BRICK_VALUE: dict = {
    BrickType.WHITE: 50,
    BrickType.ORANGE: 60,
    BrickType.CYAN: 70,
    BrickType.GREEN: 80,
    BrickType.RED: 90,
    BrickType.BLUE: 100,
    BrickType.MAGENTA: 110,
    BrickType.YELLOW: 120,
    BrickType.SILVER: 200,
}

GAME_FRAMERATE: int = 60

BOX_WALLS_THICKNESS: float = 10.0

BALL_RADIUS: float = 10.0
BALL_SPEED: float = 15.0

BONUS_SIZE: float = 25.0
BONUS_DEFAULT_POS: Position2D = Position2D(x=0, y=0)
BONUS_FALLING_SPEED: float = 10.0
BONUS_RESIZE_FACTOR: float = 1.5
