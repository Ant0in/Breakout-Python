

from src.game.collision_helper import CollisionHelper
from src.game.solid_shapes import SolidInterface, SolidCircle, SolidRectangle
from src.game.ball import Ball
from src.game.raquette import Raquette
from src.game.brick import Brick

from src.common import Position2D


class GameBox:

    def __init__(self, position: Position2D, width: float, height: float,
                 balls: list[Ball], raquette: Raquette, bricks: list[Brick] | None = None, entities: list[SolidInterface] | None = None) -> None:
        self._position: Position2D = position
        self._width: float = width
        self._height: float = height

        self._balls: list[Ball] = balls
        self._raquette: Raquette = raquette
        self._bricks: list[Brick] = bricks if bricks else list()
        self._entities: list[SolidInterface] = entities if entities else list()

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

    def getBricks(self) -> list[Brick]:
        return self._bricks
    
    def addBrick(self, brick: Brick) -> None:
        self.getBricks().append(brick)

    def removeBrick(self, brick: Brick) -> None:
        bricks: list[Brick] = self.getBricks()
        if brick in bricks: bricks.remove(brick)

    def getBalls(self) -> list[Ball]:
        return self._balls
    
    def getRaquette(self) -> Raquette:
        return self._raquette


    def tryMoveRaquette(self, p: Position2D) -> bool:
        rq: Raquette = self.getRaquette()

        # Si la raquette n'est pas out of bound ;
        can_move: bool = (
            self.getPosition().getX() <= p.getX() and \
            self.getPosition().getY() <= p.getY() and \
            self.getPosition().getX() + self.getWidth() >= p.getX() + rq.getWidth() and \
            self.getPosition().getY() + self.getHeight() >= p.getY() + rq.getHeight()
        )

        # On déplace la raquette si possible
        if can_move: rq.moveToCoordinates(c=p)
        return can_move

    def tryMoveBalls(self, p_vec: list[Position2D]) -> list[bool]:
        balls: list[Ball] = self.getBalls()

        can_move: list[bool] = [
            (
                self.getPosition().getX() <= p.getX() - ball.getRadius() and \
                self.getPosition().getY() <= p.getY() - ball.getRadius() and \
                self.getPosition().getX() + self.getWidth() >= p.getX() + ball.getRadius() and \
                self.getPosition().getY() + self.getHeight() >= p.getY() + ball.getRadius()
            )
            for p, ball in zip(p_vec, balls)
        ]

        # Déplacer les balles si possible
        for p, flag, ball in zip(p_vec, can_move, balls):
            if flag: ball.moveToCoordinates(c=p)

        return can_move

    def checkCollisionsWithWalls(self) -> None:
        
        # Pour chacune des balls, on applique un check de collision.
        for ball in self.getBalls():
            
            ball_pos: Position2D = ball.getCenterPosition()
            ball_radius: float = ball.getRadius()
            vx, vy = ball.getVelocity()

            # Mur gauche
            if ball_pos.getX() - ball_radius <= self.getPosition().getX() and vx < 0: ball.setVelocity(-vx, vy)
            # Mur droit
            elif ball_pos.getX() + ball_radius >= self.getPosition().getX() + self.getWidth() and vx > 0: ball.setVelocity(-vx, vy)
            # Mur haut
            if ball_pos.getY() - ball_radius <= self.getPosition().getY() and vy < 0: ball.setVelocity(vx, -vy)
            # Mur bas
            elif ball_pos.getY() + ball_radius >= self.getPosition().getY() + self.getHeight() and vy > 0: ball.setVelocity(vx, -vy)

            else: pass

    def checkCollisionsWithRaquetteAndBricks(self) -> list[Brick]:
        
        bricks_hit: list[Brick] = list()

        for ball in self.getBalls():
    
            vx, vy = ball.getVelocity()

            # Collision avec la raquette
            if CollisionHelper.isColliding(ball.getHitbox(), self.getRaquette().getHitbox()):
                ball.setVelocity(vx, -vy)

            # Collision avec les briques
            for brick in self.getBricks():
                if CollisionHelper.isColliding(ball.getHitbox(), brick.getHitbox()) and brick not in bricks_hit:
                    ball.setVelocity(-vx, -vy)
                    bricks_hit.append(brick)

        return bricks_hit
                    
                    
