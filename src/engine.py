


from src.game.collision_helper import CollisionHelper
from src.game.solid_shapes import SolidInterface, SolidCircle, SolidRectangle
from src.game.ball import Ball
from src.game.raquette import Raquette
from src.game.game_box import GameBox

from src.common import Position2D, Action


class GameEngine:
    

    @staticmethod
    def _handle_inputs() -> Action:
        ...

    @staticmethod
    def _handle_actions(gamebox: GameBox, action: Action) -> bool:
        
        rq: Raquette = gamebox.getRaquette()
        rq_x: float = rq.getPosition().getX()
        rq_y: float = rq.getPosition().getY()
        rq_sensibility: float = rq.getSensibility()
        
        match action:

            case Action.LEFT: new_position: Position2D = Position2D(rq_x - rq_sensibility, rq_y)
            case Action.RIGHT: new_position: Position2D = Position2D(rq_x + rq_sensibility, rq_y)
            case Action._NONE: new_position: Position2D = Position2D(rq_x, rq_y)
            case _: raise NotImplementedError()

        could_move: bool = gamebox.tryMoveRaquette(p=new_position)
        return could_move

    @staticmethod
    def _calculate_balls_positions(gamebox: GameBox) -> list[Position2D]:

        pvec: list[Position2D] = list()

        for ball in gamebox.getBalls():
            x_vel, y_vel = ball.getVelocity()
            speed: float = ball.getSpeed()
            dx: float = ball.getCenterPosition().getX() + (x_vel * speed)
            dy: float = ball.getCenterPosition().getY() + (y_vel * speed)
            pvec.append(Position2D(dx, dy))

        return pvec
    
    @staticmethod
    def _handle_balls(gamebox: GameBox) -> list[SolidRectangle]:

        # On va calculer les nouvelles positions des balles puis tenter de les déplacer.
        pvec: list[Position2D] = GameEngine._calculate_balls_positions(gamebox=gamebox)
        could_move: list[bool] = gamebox.tryMoveBalls(p_vec=pvec)

        # Puis on applique les collisions avec les murs / briques
        gamebox.checkCollisionsWithWalls()
        bricks_hit: list[SolidRectangle] = gamebox.checkCollisionsWithRaquetteAndBricks()
        return bricks_hit
    
