

from src.game.solid_shapes import SolidRectangle
from src.common import Position2D



class Raquette:

    def __init__(self, position: Position2D, width: float, height: float, sensibility: float = 10.0) -> None:
        
        self._position: Position2D = position
        self._width: float = width
        self._height: float = height
        self._hitbox: SolidRectangle = SolidRectangle(position=position, height=height, width=width)
        self._sensibility: float = sensibility

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

    def getHitbox(self) -> SolidRectangle:
        return self._hitbox
    
    def getSensibility(self) -> float:
        return self._sensibility
    
    def setSensibility(self, s: float) -> None:
        self._sensibility = s

    def calculateCenterPosition(self) -> Position2D:
        cx: float = self.getPosition().getX() + (self.getWidth() / 2)
        cy: float = self.getPosition().getY() + (self.getHeight() / 2)
        return Position2D(x=cx, y=cy)

    def moveToCoordinates(self, c: Position2D) -> None:
        # On move la raquette avec sa hitbox.
        self.setPosition(p=c)
        self.getHitbox().setPosition(p=c)


