

from src.game.bonus import BonusInterface

from src.physics.solid_shapes import SolidRectangle

from src.common import Position2D, BrickType, BRICK_HP, BRICK_VALUE



class Brick:
    
    def __init__(self, position: Position2D, width: float, height: float,
                 btype: BrickType, bonus: BonusInterface | None = None) -> None:
        
        self._position: Position2D = position
        self._width: float = width
        self._height: float = height
        self._btype: BrickType = btype
        self._bonus: BonusInterface | None = bonus

        self._hitbox: SolidRectangle = SolidRectangle(position=position, height=height, width=width)
        self._hp: float | int = self._attributeBrickHpByType(btype=btype)


    @staticmethod
    def _attributeBrickHpByType(btype: BrickType) -> int | float:
        hp: float | int | None = BRICK_HP.get(btype, None)
        if hp is not None: return hp
        else: raise NotImplementedError(f'[E] Error for brick type : {btype}')

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
    
    def getBonus(self) -> None | BonusInterface:
        return self._bonus
    
    def setBonus(self, b: BonusInterface) -> None:
        self._bonus = b

    def doesBrickContainsBonus(self) -> bool:
        return (self.getBonus() is not None)

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
        return (self.getHP() <= 0)
    
    def getBrickValue(self) -> int:
        btype: BrickType = self.getBrickType()
        val: int | None = BRICK_VALUE.get(btype, None)
        if val is not None: return val
        else: raise NotImplementedError(f'[E] Unknown brick value for brick type : {val}')

