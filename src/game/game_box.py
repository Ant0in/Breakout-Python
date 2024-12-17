

from src.game.ball import Ball
from src.game.raquette import Raquette
from src.game.brick import Brick
from src.game.bonus import BonusInterface

from src.physics.collision_helper import CollisionHelper
from src.physics.solid_shapes import SolidInterface, SolidRectangle

from src.common import Position2D, WallType, BrickType, BOX_WALLS_THICKNESS



class GameBox:

    def __init__(self, position: Position2D, width: float, height: float,
                 balls: list[Ball], raquette: Raquette, bricks: list[Brick] | None = None, entities: list[BonusInterface] | None = None) -> None:
        
        self._position: Position2D = position
        self._width: float = width
        self._height: float = height
        self._hitbox: SolidRectangle = SolidRectangle(position=position, height=height, width=width)
        
        self._balls: list[Ball] = balls
        self._raquette: Raquette = raquette
        self._bricks: list[Brick] = bricks if bricks else list()
        self._entities: list[BonusInterface] = entities if entities else list()

        self._initializeWalls()

    def _initializeWalls(self) -> None:

        p: Position2D = self.getPosition()
        w: float = self.getWidth()
        h: float = self.getHeight()
        
        self._leftWall: SolidRectangle = SolidRectangle(position=Position2D(p.getX() - BOX_WALLS_THICKNESS, p.getY()), height=h, width=BOX_WALLS_THICKNESS)
        self._rightWall: SolidRectangle = SolidRectangle(position=Position2D(p.getX() + w, p.getY()), height=h, width=BOX_WALLS_THICKNESS)
        self._topWall: SolidRectangle = SolidRectangle(position=Position2D(p.getX(), p.getY() - BOX_WALLS_THICKNESS), height=BOX_WALLS_THICKNESS, width=w)
        self._bottomWall: SolidRectangle = SolidRectangle(position=Position2D(p.getX(), p.getY() + h), height=BOX_WALLS_THICKNESS, width=w)

    def getPosition(self) -> Position2D:
        return self._position

    def getWidth(self) -> float:
        return self._width

    def getHeight(self) -> float:
        return self._height

    def getHitbox(self) -> SolidRectangle:
        return self._hitbox

    def getEntities(self) -> list[BonusInterface]:
        return self._entities

    def addEntity(self, entity: BonusInterface) -> None:
        self.getEntities().append(entity)

    def removeEntity(self, entity: BonusInterface) -> None:
        entities: list[BonusInterface] = self.getEntities()
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
    
    def isBallVectorEmpty(self) -> bool:
        return (len(self.getBalls()) == 0)

    def doesPlayerHaveMutlipleBalls(self) -> bool:
        return (len(self.getBalls()) > 1)

    def addBall(self, b: Ball) -> None:
        self.getBalls().append(b)

    def removeBall(self, b: Ball) -> None:
        if b in self.getBalls(): self.getBalls().remove(b)
    
    def getRaquette(self) -> Raquette:
        return self._raquette

    def getLeftWall(self) -> SolidRectangle:
        return self._leftWall
    
    def getRightWall(self) -> SolidInterface:
        return self._rightWall
    
    def getBottomWall(self) -> SolidInterface:
        return self._bottomWall
    
    def getTopWall(self) -> SolidInterface:
        return self._topWall

    def isPositionOutOfBounds(self, pos: Position2D) -> bool:
        # Checks if a position is contained within the GameBox.
        # If it isn't the case, then the position is out of bounds. -> returns True
        isPointContainedInGameBox: bool = self.getHitbox().isPointInSolid(point=pos)
        return (not isPointContainedInGameBox)

    def isObjectOutOfBounds(self, object: Raquette | Ball | BonusInterface) -> bool:
        
        # Checks if an 'object' (which has a SolidInterface) is colliding with the GameBox.
        # If it isn't the case, then the 'object' is out of bounds. -> returns True
        outOfBounds: bool = (not CollisionHelper.isColliding(self.getHitbox(), object.getHitbox()))
        return outOfBounds

    def isObjectCollidingWithWalls(self, object: Raquette | Ball | BonusInterface) -> None | WallType:
        
        # On fait une méthode qui vérifira si un objet collide avec un mur. Si c'est le cas, on return le mur.
        # Sinon, on ne return rien.
        if   CollisionHelper.isColliding(object.getHitbox(), self.getLeftWall()):   return WallType.LEFT
        elif CollisionHelper.isColliding(object.getHitbox(), self.getRightWall()):  return WallType.RIGHT
        elif CollisionHelper.isColliding(object.getHitbox(), self.getTopWall()):    return WallType.TOP
        elif CollisionHelper.isColliding(object.getHitbox(), self.getBottomWall()): return WallType.BOTTOM
        
        else: return None

    def tryMoveRaquette(self, pos: Position2D) -> bool:
        
        # On essaye de move la raquette en regardant si collision avec les murs.
        rq: Raquette = self.getRaquette()
        temp: Raquette = Raquette(position=pos, width=rq.getWidth(), height=rq.getHeight(), sensibility=rq.getSensibility())

        # None -> Pas de collision.
        if self.isObjectCollidingWithWalls(object=temp) is None:
            self.getRaquette().moveToCoordinates(c=pos)
            del temp
            return True
        
        # WallType -> Collision.
        else: return False

    def tryMoveBalls(self) -> list[bool]:
        
        balls: list[Ball] = self.getBalls()
        could_move: bool = [False for _ in range(len(balls))]

        for idx, ball in enumerate(balls):
            
            np: Position2D = ball.calculateNewPosition()
            temp: Ball = Ball(center=np, radius=ball.getRadius(), speed=ball.getSpeed())
            
            wallCollision: WallType | None = self.isObjectCollidingWithWalls(object=temp)
            
            # Si aucune wall collision alors on peut move la vraie balle
            if wallCollision is None:
                ball.moveToCoordinates(c=np)
                could_move[idx] = True

            # Sinon, on va modifier le vecteur de vélocité de la balle selon
            # le mur touché.
            else:
                could_move[idx] = False
                vx, vy = ball.getVelocity()

                match wallCollision:
                    case WallType.LEFT: ball.setVelocity(-vx, vy)
                    case WallType.RIGHT: ball.setVelocity(-vx, vy)
                    case WallType.TOP: ball.setVelocity(vx, -vy)
                    case WallType.BOTTOM: ball.setAlive(flag=False)  # Ball is unusable

            del temp

        return could_move

    def isWin(self) -> bool:
        # On va parcourir les bricks restantes. Si il existe une brique (non détruite)
        # autre que des dorées, alors on a pas encore win.
        for b in self.getBricks():
            if (not b.isBroken()) and (b.getBrickType() is not BrickType.GOLD):
                return False
        return True
    
