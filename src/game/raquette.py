

from src.physics.solid_shapes import SolidRectangle

from src.common import Position2D, Action



class Raquette:

    def __init__(self, position: Position2D, width: float, height: float, sensibility: float = 10.0) -> None:
        
        self._hitbox: SolidRectangle = SolidRectangle(position=position, height=height, width=width)
        self._sensibility: float = sensibility

    def getHitbox(self) -> SolidRectangle:
        return self._hitbox

    def getPosition(self) -> Position2D:
        return self.getHitbox().getPosition()
    
    def setPosition(self, p: Position2D) -> None:
        self.getHitbox().setPosition(p=p)

    def getWidth(self) -> float:
        return self.getHitbox().getWidth()
    
    def setWidth(self, w: float) -> None:
        self.getHitbox().setWidth(w=w)

    def getHeight(self) -> float:
        return self.getHitbox().getHeight()
    
    def setHeight(self, h: float) -> None:
        self.getHitbox().setHeight(h=h)

    def getSensibility(self) -> float:
        return self._sensibility
    
    def setSensibility(self, s: float) -> None:
        self._sensibility = s

    def calculateNewPosition(self, action: Action) -> Position2D:

        _x: float = self.getPosition().getX()
        _y: float = self.getPosition().getY()
        sensibility: float = self.getSensibility()
        
        match action:
            
            case Action.LEFT: return Position2D(_x - sensibility, _y)
            case Action.RIGHT: return Position2D(_x + sensibility, _y)
            case Action._NONE: return Position2D(_x, _y)
            
            case _: raise NotImplementedError()
    
    def getCenterPosition(self) -> Position2D:
        return self.getHitbox().getCenterPosition()
    
