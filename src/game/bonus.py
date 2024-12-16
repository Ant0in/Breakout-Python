

from abc import ABC, abstractmethod
from src.common import *
from src.game.solid_shapes import SolidRectangle


class BonusInterface(ABC):

    def __init__(self, pos: Position2D, size: float, active_duration: int, falling_speed: float,
                 is_active: bool = False, is_spawned: bool = False) -> None:
        
        self._pos: Position2D = pos
        self._size: float = size
        self._activeDuration: int = active_duration
        self._fallingSpeed: float = falling_speed
        
        # let's use a square shape for bonuses (size x size)
        self._hitbox: SolidRectangle = SolidRectangle(position=pos, height=size, width=size)
        
        # and then flags, for some reason
        self._isSpawned: bool = is_spawned
        self._isActive: bool = is_active
        

    def getSize(self) -> float:
        return self._size

    def setSize(self, s: float) -> None:
        self._size = s

    def getPosition(self) -> Position2D:
        return self._pos
    
    def setPosition(self, p: Position2D) -> None:
        self._pos = p

    def getHitbox(self) -> SolidRectangle:
        return self._hitbox

    def isSpawned(self) -> bool:
        return self._isSpawned

    def setSpawned(self, flag: bool) -> None:    
        self._isSpawned = flag

    def isActive(self) -> bool:
        return self._isActive

    def setActive(self, flag: bool) -> None:
        self._isActive = flag

    def getDuration(self) -> int:
        return self._activeDuration
    
    def setDuration(self, d: int) -> None:
        self._activeDuration = d

    def getFallingSpeed(self) -> float:
        return self._fallingSpeed
    
    def setFallingSpeed(self, s: float) -> None:
        self._fallingSpeed = s

    def incrementDuration(self, incr: int) -> None:
        self.setDuration(d=(self.getDuration() + incr))

    def moveToCoords(self, p: Position2D) -> None:
        self.setPosition(p=p)
        self.getHitbox().setPosition(p=p)

    def spawnBonus(self, p: Position2D) -> None:
        self.moveToCoords(p=p)
        self.setSpawned(flag=True)

    def getGravityPosition(self) -> Position2D:
        # using x(t) = x0 + velocity*t, for t=1 (bc calculated each frame)
        tl: Position2D = self.getPosition()
        _x: float = tl.getX() - self.getFallingSpeed()
        _y: float = tl.getY()
        return Position2D(x=_x, y=_y)

    def hasBonusDurationExpired(self) -> bool:
        return (self.getDuration() <= 0)
    
    @abstractmethod
    def applyLogic(self) -> any:
        raise NotImplementedError()


class DuplicationBonus(BonusInterface):
    
    def __init__(self, pos: Position2D) -> None:
        
        super().__init__(pos=pos, size=BONUS_SIZE, active_duration=1,
            falling_speed=BONUS_FALLING_SPEED, is_active=False, is_spawned=False)
        
    def applyLogic(self) -> None:

        # 
        if not self.isActive() or self.hasBonusDurationExpired():
            return
        

