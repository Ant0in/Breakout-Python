

from src.engine.solid_shapes import SolidInterface, SolidCircle, SolidRectangle

from src.common import Position2D



class CollisionHelper:

    @staticmethod
    def isColliding(solid1: SolidInterface, solid2: SolidInterface) -> bool:
 
        if isinstance(solid1, SolidRectangle) and isinstance(solid2, SolidRectangle):
            return CollisionHelper._rect_vs_rect(solid1, solid2)
        
        elif isinstance(solid1, SolidRectangle) and isinstance(solid2, SolidCircle):
            return CollisionHelper._rect_vs_circle(solid1, solid2)
        
        elif isinstance(solid1, SolidCircle) and isinstance(solid2, SolidRectangle):
            return CollisionHelper._rect_vs_circle(solid2, solid1)
        
        elif isinstance(solid1, SolidCircle) and isinstance(solid2, SolidCircle):
            return CollisionHelper._circle_vs_circle(solid1, solid2)
        
        else: raise NotImplementedError(f"Collision non supportée avec {solid1} & {solid2}.")

    @staticmethod
    def _rect_vs_rect(rect1: SolidRectangle, rect2: SolidRectangle) -> bool:

        return not (
            rect1.getPosition().getX() + rect1.getWidth() <= rect2.getPosition().getX() or
            rect2.getPosition().getX() + rect2.getWidth() <= rect1.getPosition().getX() or
            rect1.getPosition().getY() + rect1.getHeight() <= rect2.getPosition().getY() or
            rect2.getPosition().getY() + rect2.getHeight() <= rect1.getPosition().getY()
        )

    @staticmethod
    def _rect_vs_circle(rect: SolidRectangle, circle: SolidCircle) -> bool:
 
        circle_center: Position2D = circle.getPosition()
        rect_x: float = rect.getPosition().getX()
        rect_y: float = rect.getPosition().getY()

        closest_x: float = max(rect_x, min(circle_center.getX(), rect_x + rect.getWidth()))
        closest_y: float = max(rect_y, min(circle_center.getY(), rect_y + rect.getHeight()))

        dx: float = circle_center.getX() - closest_x
        dy: float = circle_center.getY() - closest_y

        return (dx ** 2 + dy ** 2) <= (circle.getRadius() ** 2)

    @staticmethod
    def _circle_vs_circle(circle1: SolidCircle, circle2: SolidCircle) -> bool:

        center1: Position2D = circle1.getPosition()
        center2: Position2D = circle2.getPosition()
        ds_sq: float = (center1.getX() - center2.getX())**2 + (center1.getY() - center2.getY())**2
        return ds_sq <= ((circle1.getRadius() + circle2.getRadius()) ** 2)

