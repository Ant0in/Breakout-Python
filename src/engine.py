


from src.game.collision_helper import CollisionHelper
from src.game.ball import Ball
from src.game.raquette import Raquette
from src.game.game_box import GameBox
from src.game.brick import Brick

from src.controller import GameController
from src.common import Position2D, Action


class GameEngine:
    
    @staticmethod
    def _handle_inputs(controller: GameController) -> Action:
        return controller.getUserAction()

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
    def _handle_balls(gamebox: GameBox) -> list[Brick]:

        # On va calculer les nouvelles positions des balles puis tenter de les déplacer.
        pvec: list[Position2D] = GameEngine._calculate_balls_positions(gamebox=gamebox)
        could_move: list[bool] = gamebox.tryMoveBalls(p_vec=pvec)

        # Puis on applique les collisions avec les murs / briques
        gamebox.checkCollisionsWithWalls()
        bricks_hit: list[Brick] = gamebox.checkCollisionsWithRaquetteAndBricks()
        return bricks_hit
    
    @staticmethod
    def _handle_brick_destruction(gamebox: GameBox, bricks: list[Brick]) -> int:
        
        total_reward: int = 0

        for b in bricks:

            b.makeBrickLooseHP(loss=1)

            if b.isBroken():

                # TODO : spawn des bonus ici

                gamebox.removeBrick(brick=b)
                total_reward += b.getBrickValue()

        return total_reward

    @staticmethod
    def handle_routine(gamebox: GameBox, controller: GameController) -> None:

        # Gestion des actions
        player_action: Action = GameEngine._handle_inputs(controller=controller)
        GameEngine._handle_actions(gamebox=gamebox, action=player_action)

        # Gestion des collisions (briques / balles / raquette)
        bricks_hit: list[Brick] = GameEngine._handle_balls(gamebox=gamebox)
        reward: int = GameEngine._handle_brick_destruction(gamebox=gamebox, bricks=bricks_hit)

        # TODO : Gestion des bonus (utilisation bonus / collision bonus (pickup) / fin d'un bonus actif)
        ...

        # TODO : Gestion du score (via 'reward')
        ...

        # TODO : Gestion 'fin de niveau'
        ...
