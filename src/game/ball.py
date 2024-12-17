

from src.physics.solid_shapes import SolidCircle

from src.common import Position2D



class Ball:

    def __init__(self, center: Position2D, radius: float, speed: float = 1.0) -> None:
        
        self._hitbox: SolidCircle = SolidCircle(position=center, radius=radius)

        self._speed: float = speed
        self._x_velocity: float = 0.0
        self._y_velocity: float = 1.0
        self._isAlive: bool = True

    def getHitbox(self) -> SolidCircle:
        return self._hitbox
    
    def getCenterPosition(self) -> Position2D:
        return self.getHitbox().getPosition()
    
    def setCenterPosition(self, p: Position2D) -> None:
        self.getHitbox().setPosition(p=p)

    def getRadius(self) -> float:
        return self.getHitbox().getRadius()
    
    def setRadius(self, r: float) -> None:
        self.getHitbox().setRadius(r=r)

    def getVelocity(self) -> tuple[float, float]:
        return self._x_velocity, self._y_velocity
    
    def setVelocity(self, _xv: float, _yv: float) -> None:
        self._x_velocity = _xv
        self._y_velocity = _yv

    def getSpeed(self) -> float:
        return self._speed
    
    def setSpeed(self, s: float) -> None:
        self._speed = s

    def isAlive(self) -> bool:
        return self._isAlive
    
    def setAlive(self, flag: bool) -> None:
        self._isAlive = flag

    def calculateNewPosition(self) -> Position2D:

        velocity: tuple[float, float] = self.getVelocity()
        x_vel: float = velocity[0]
        y_vel: float = velocity[1]
        speed: float = self.getSpeed()

        dx: float = self.getCenterPosition().getX() + (x_vel * speed)
        dy: float = self.getCenterPosition().getY() + (y_vel * speed)

        return Position2D(x=dx, y=dy)
    

