

from src.game.collision_helper import CollisionHelper
from src.game.solid_shapes import SolidInterface, SolidCircle, SolidRectangle
from src.game.ball import Ball
from src.game.raquette import Raquette

from src.common import Position2D
import itertools



class GameBox:

    def __init__(self, position: Position2D, width: float, height: float, balls: list[Ball], raquette: Raquette) -> None:

        self._position: Position2D = position
        self._width: float = width
        self._height: float = height

        self._balls: list[Ball] = balls
        self._raquette: Raquette = raquette
        self._bricks: list[SolidInterface] = list()
        self._entities: list[SolidInterface] = list()

    def getPosition(self) -> Position2D:
        return self._position

    def getWidth(self) -> float:
        return self._width

    def getHeight(self) -> float:
        return self._height

    def getEntities(self) -> list[SolidInterface]:
        return self._entities

    def addEntity(self, entity: SolidInterface) -> None:
        self.getEntities().append(entity)

    def removeEntity(self, entity: SolidInterface) -> None:
        entities: list[SolidInterface] = self.getEntities()
        if entity in entities: entities.remove(entity)

    def getBricks(self) -> list[SolidInterface]:
        return self._bricks
    
    def addBrick(self, brick: SolidInterface) -> None:
        self.getBricks().append(brick)

    def removeBrick(self, brick: SolidInterface) -> None:
        bricks: list[SolidInterface] = self.getBricks()
        if brick in bricks: bricks.remove(brick)

    def getBalls(self) -> list[Ball]:
        return self._balls
    
    def getRaquette(self) -> Raquette:
        return self._raquette

    def isOutOfBounds(self, entity: SolidInterface) -> bool:

        if isinstance(entity, SolidRectangle):
            rect: SolidRectangle = entity
            return (
                rect.getPosition().getX() < self.getPosition().getX() or
                rect.getPosition().getY() < self.getPosition().getY() or
                rect.getPosition().getX() + rect.getWidth() > self.getPosition().getX() + self.getWidth() or
                rect.getPosition().getY() + rect.getHeight() > self.getPosition().getY() + self.getHeight()
            )
        
        elif isinstance(entity, SolidCircle):
            circle = entity
            return (
                circle.getPosition().getX() - circle.getRadius() < self.getPosition().getX() or
                circle.getPosition().getY() - circle.getRadius() < self.getPosition().getY() or
                circle.getPosition().getX() + circle.getRadius() > self.getPosition().getX() + self.getWidth() or
                circle.getPosition().getY() + circle.getRadius() > self.getPosition().getY() + self.getHeight()
            )
        
        else: raise NotImplementedError(f"[e] Unknown entity type for isOutOfBounds. (e={entity})")



    def checkCollisionsWithEntities(self) -> list[SolidInterface]:

        colliding_entities: list[SolidInterface] = []
 
        # On regarde si une entité collide avec la raquette
        for entity in self.getEntities():
            if CollisionHelper.isColliding(self.getRaquette().getHitbox(), entity):
                colliding_entities.append(entity)
        
        return colliding_entities
    
    def checkCollisionsWithBricks(self) -> list[SolidInterface]:

        colliding_bricks: list[SolidInterface] = []
 
        # On regarde si une brique collide avec une balle
        for brick in self.getEntities():
            for ball in self.getBalls():

                if CollisionHelper.isColliding(ball.getHitbox(), brick):
                    colliding_bricks.append(brick)
        
        return colliding_bricks

