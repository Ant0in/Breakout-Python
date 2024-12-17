

from src.physics.solid_shapes import SolidCircle

from src.common import Position2D



class Ball:

    def __init__(self, center: Position2D, radius: float, speed: float = 1.0) -> None:
        
        self._center: Position2D = center
        self._radius: float = radius
        self._hitbox: SolidCircle = SolidCircle(position=center, radius=radius)

        self._speed: float = speed
        self._x_velocity: float = 0.0
        self._y_velocity: float = 1.0

    def getCenterPosition(self) -> Position2D:
        return self._center
    
    def setCenterPosition(self, p: Position2D) -> None:
        self._center = p

    def getRadius(self) -> float:
        return self._radius
    
    def setRadius(self, r: float) -> None:
        self._radius = r

    def getHitbox(self) -> SolidCircle:
        return self._hitbox
    
    def getVelocity(self) -> tuple[float, float]:
        return self._x_velocity, self._y_velocity
    
    def setVelocity(self, _xv: float, _yv: float) -> None:
        self._x_velocity = _xv
        self._y_velocity = _yv

    def getSpeed(self) -> float:
        return self._speed
    
    def setSpeed(self, s: float) -> None:
        self._speed = s

    def moveToCoordinates(self, c: Position2D) -> None:
        # On move la ball avec sa hitbox.
        self.setCenterPosition(p=c)
        self.getHitbox().setPosition(p=c)

    def calculateNewPosition(self) -> Position2D:

        velocity: tuple[float, float] = self.getVelocity()
        x_vel: float = velocity[0]
        y_vel: float = velocity[1]
        speed: float = self.getSpeed()

        dx: float = self.getCenterPosition().getX() + (x_vel * speed)
        dy: float = self.getCenterPosition().getY() + (y_vel * speed)

        return Position2D(x=dx, y=dy)
    

