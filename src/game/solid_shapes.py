

from abc import ABC, abstractmethod
from src.common import Position2D


class SolidInterface(ABC):

    @abstractmethod
    def isPointInSolid(self, point: Position2D) -> bool:
        pass


class SolidRectangle(SolidInterface):

    def __init__(self, position: Position2D, height: float, width: float) -> None:
        self._position: Position2D = position
        self._width: float = width
        self._height: float = height

    def getPosition(self) -> Position2D:
        return self._position
    
    def setPosition(self, p: Position2D) -> None:
        self._position = p

    def getHeight(self) -> float:
        return self._height
    
    def getWidth(self) -> float:
        return self._width
    
    def getCorners(self) -> list[Position2D]:
        top_left: Position2D = self.getPosition()
        top_right: Position2D = Position2D(top_left.getX() + self.getWidth(), top_left.getY())
        bottom_left: Position2D = Position2D(top_left.getX(), top_left.getY() + self.getHeight())
        bottom_right: Position2D = Position2D(top_left.getX() + self.getWidth(), top_left.getY() + self.getHeight())
        return [top_left, top_right, bottom_left, bottom_right]

    def isPointInSolid(self, point: Position2D) -> bool:

        top_left: Position2D = self.getPosition()
        return (
            top_left.getX() <= point.getX() <= top_left.getX() + self.getWidth() and
            top_left.getY() <= point.getY() <= top_left.getY() + self.getHeight()
        )


class SolidCircle(SolidInterface):

    def __init__(self, position: Position2D, radius: float) -> None:
        self._position: Position2D = position
        self._radius: float = radius

    def getPosition(self) -> Position2D:
        return self._position
    
    def setPosition(self, p: Position2D) -> None:
        self._position = p

    def getRadius(self) -> float:
        return self._radius
    
    def setRadius(self, r: float) -> None:
        self._radius = r
    
    def isPointInSolid(self, point: Position2D) -> bool:
        center: Position2D = self.getPosition()
        ds_sq: float = (point.getX() - center.getX()) ** 2 + (point.getY() - center.getY()) ** 2
        return ds_sq <= self.getRadius() ** 2

