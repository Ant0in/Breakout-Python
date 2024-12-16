

from src.engine.solid_shapes import SolidRectangle

from src.common import Position2D, BrickType



class Brick:
    
    def __init__(self, position: Position2D, width: float, height: float, btype: BrickType) -> None:
        
        self._position: Position2D = position
        self._width: float = width
        self._height: float = height
        self._btype: BrickType = btype
        self._hitbox: SolidRectangle = SolidRectangle(position=position, height=height, width=width)
        self._hp: float | int = self._attributeBrickHpByType(btype=btype)

    
    @staticmethod
    def _attributeBrickHpByType(btype: BrickType) -> int | float:
        match btype:
            case BrickType.GOLD: return float('inf')
            case BrickType.SILVER: return 2
            case _: return 1

    def getPosition(self) -> Position2D:
        return self._position
    
    def setPosition(self, p: Position2D) -> None:
        self._position = p

    def getWidth(self) -> float:
        return self._width
    
    def setWidth(self, w: float) -> None:
        self._width = w

    def getHeight(self) -> float:
        return self._height
    
    def setHeight(self, h: float) -> None:
        self._height = h

    def getBrickType(self) -> BrickType:
        return self._btype
    
    def getHP(self) -> int | float:
        return self._hp
    
    def setHP(self, v: int | float) -> None:
        self._hp = v

    def getHitbox(self) -> SolidRectangle:
        return self._hitbox
    
    def moveToCoordinates(self, c: Position2D) -> None:
        # On move la brique avec sa hitbox.
        self.setPosition(p=c)
        self.getHitbox().setPosition(p=c)

    def makeBrickLooseHP(self, loss: int) -> None:
        dhp: int | float = self.getHP() - loss
        self.setHP(v=dhp)

    def isBroken(self) -> bool:
        return self.getHP() <= 0
    
    def getBrickValue(self) -> int:
        match self.getBrickType():
            case BrickType.WHITE: return 50
            case BrickType.ORANGE: return 60
            case BrickType.CYAN: return 70
            case BrickType.GREEN: return 80
            case BrickType.RED: return 90
            case BrickType.BLUE: return 100
            case BrickType.MAGENTA: return 110
            case BrickType.YELLOW: return 120
            case BrickType.SILVER: return 200
            case _: raise NotImplementedError()


