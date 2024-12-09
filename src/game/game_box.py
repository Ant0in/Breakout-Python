

from src.game.collision_helper import CollisionHelper
from src.game.solid_shapes import SolidInterface, SolidCircle, SolidRectangle

from src.common import Position2D
import itertools



class GameBox:

    def __init__(self, position: Position2D, width: float, height: float) -> None:

        self._position: Position2D = position
        self._width: float = width
        self._height: float = height
        self._entities: list[SolidInterface] = list()

    def getPosition(self) -> Position2D:
        return self._position

    def getWidth(self) -> float:
        return self._width

    def getHeight(self) -> float:
        return self._height

    def addEntity(self, entity: SolidInterface) -> None:
        self._entities.append(entity)

    def getEntities(self) -> list[SolidInterface]:
        return self._entities

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

    def checkCollisions(self) -> list[SolidInterface]:

        colliding_entities: list[SolidInterface] = []
        entities: list[SolidInterface] = self.getEntities()
        
        # Si jamais une seule entité (ou aucune), on ne regarde même pas,
        # pas de collision possible.
        if len(entities) < 2:
            return list()

        # On génère toutes les combinasions de deux entitées pour check collisions
        for entity1, entity2 in itertools.combinations(entities, 2):
            
            if CollisionHelper.isColliding(entity1, entity2):
                colliding_entities += [entity1, entity2]
        
        return colliding_entities


