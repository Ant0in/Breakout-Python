

from src.game.raquette import Raquette

from src.physics.solid_shapes import SolidRectangle

from src.common import Position2D, LASER_THICKNESS, LASER_LENGTH



class Laser:
    
    def __init__(self, pos: Position2D) -> None:
        self._hitbox: SolidRectangle = SolidRectangle(position=pos, height=LASER_THICKNESS, width=LASER_LENGTH)

    def getHitbox(self) -> SolidRectangle:
        return self._hitbox
    
    def getPosition(self) -> Position2D:
        return self.getHitbox().getPosition()
    
    def setPosition(self, p: Position2D) -> None:
        self.getHitbox().setPosition(p=p)

    def spawnLaser(self, rq: Raquette) -> None:
        rq_center: Position2D = rq.getCenterPosition()
        offset_center: Position2D = Position2D(x=(rq_center.getX() - LASER_THICKNESS / 2), y=rq.getPosition().getY())
        self.setPosition(p=offset_center)

