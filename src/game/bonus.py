

from src.game.ball import Ball

from src.physics.solid_shapes import SolidRectangle

from src.common import *

from abc import ABC, abstractmethod
import math



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
        _x: float = tl.getX() 
        _y: float = tl.getY() + self.getFallingSpeed()
        return Position2D(x=_x, y=_y)

    def hasBonusDurationExpired(self) -> bool:
        return (self.getDuration() <= 0)
    
    @abstractmethod
    def applyLogic(self, gb) -> any:
        # TODO : Implement logic for each bonuses that inherits from the interface
        raise NotImplementedError()


class DuplicationBonus(BonusInterface):
    
    def __init__(self) -> None:
        
        # super init from interface for duplication bonus
        super().__init__(pos=BONUS_DEFAULT_POS,
            size=BONUS_SIZE, active_duration=1,
            falling_speed=BONUS_FALLING_SPEED,
            is_active=False, is_spawned=False)
    
    @staticmethod
    def rotate_velocity(vx: float, vy: float, alpha: float):
        alpha_rad = math.radians(alpha)
        nvx: float = vx * math.cos(alpha_rad) - vy * math.sin(alpha_rad)
        nvy: float = vx * math.sin(alpha_rad) + vy * math.cos(alpha_rad)
        return nvx, nvy
        
    def applyLogic(self, gb) -> None:

        # is bonus is not active or has expired, we skip logic
        if not self.isActive() or self.hasBonusDurationExpired():
            return
        
        # if bonus is active and not expired, we will proceed to apply logic for 
        # a frame (usually making the bonus vanish) and then decrement TTL.
        ref: Ball = gb.getBalls()[0]  # lets grab the first ball of the bunch to do that
        vx, vy = ref.getVelocity()

        b1: Ball = Ball(center=ref.getCenterPosition(), radius=ref.getRadius(), speed=ref.getSpeed())
        b2: Ball = Ball(center=ref.getCenterPosition(), radius=ref.getRadius(), speed=ref.getSpeed())
        
        vx1, vy1 = self.rotate_velocity(vx, vy, 120)
        vx2, vy2 = self.rotate_velocity(vx, vy, -120)
        b1.setVelocity(_xv=vx1, _yx=vy1)
        b2.setVelocity(_xv=vx2, _yx=vy2)

        gb.addBall(b=b1)
        gb.addBall(b=b2)

        # decrement TTL (for dupe, 1 logic cycle will be applied since it has TTL of 1)
        self.incrementDuration(incr=-1)


