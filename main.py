

from src.game.solid_shapes import SolidRectangle, SolidCircle
from src.game.collision_helper import CollisionHelper

from src.common import Position2D






if __name__ == '__main__':
    
    ball: SolidCircle = SolidCircle(position=Position2D(2, 2), radius=1.42)
    brick: SolidRectangle = SolidRectangle(position=Position2D(3, 3), height=5, width=5)

    print(CollisionHelper.isColliding(solid1=ball, solid2=brick))

