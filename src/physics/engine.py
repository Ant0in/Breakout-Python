

from src.game.game_box import GameBox
from src.game.brick import Brick
from src.game.bonus import BonusInterface

from src.player.player import Player
from src.player.controller import GameController

from src.physics.collision_helper import CollisionHelper

from src.common import Position2D, Action
import math


class GameEngine:
    
    @staticmethod
    def _handleInputs(controller: GameController) -> Action:
        return controller.getUserAction()

    @staticmethod
    def _handleActions(gamebox: GameBox, action: Action) -> None:
        gamebox.tryMoveRaquette(pos=gamebox.getRaquette().calculateNewPosition(action=action))

    @staticmethod
    def _handleCollisionsWithRaquette(gamebox: GameBox) -> None:
        
        for ball in gamebox.getBalls():

            # Si une collision arrive entre la balle et la raquette, on utilise la formule dans
            # les consignes. voir ./pdf/consignes.pdf
            if CollisionHelper.isColliding(ball.getHitbox(), gamebox.getRaquette().getHitbox()):
                vx, vy = ball.getVelocity()
                total_velocity: float = math.sqrt((vx**2 + vy**2))
                L: float = gamebox.getRaquette().getWidth()
                x: float = ball.getCenterPosition().getX() - gamebox.getRaquette().calculateCenterPosition().getX()
                alpha: float = (math.pi / 6) + ((5 * math.pi) / 6) * (1 - (x / L))  # modifiée pour 30->150
                dvx: float = total_velocity * math.sin(alpha)
                dvy: float = total_velocity * math.cos(alpha)
                ball.setVelocity(dvx, dvy)
                ball.moveToCoordinates(Position2D(ball.getCenterPosition().getX(), gamebox.getRaquette().getPosition().getY() - ball.getRadius()))

            else: ...

    @staticmethod
    def _handleCollisionWithBricks(gamebox: GameBox) -> list[Brick]:

        bricks_hit: list[Brick] = list()

        for ball in gamebox.getBalls():
    
            vx, vy = ball.getVelocity()
            for brick in gamebox.getBricks():

                # Si la brique est déjà touchée, on l'ignore.
                # Sinon, si il y'a une collision, alors on inverse la vélocité, puis on l'ajoute.
                if brick not in bricks_hit and CollisionHelper.isColliding(ball.getHitbox(), brick.getHitbox()):
                    ball.setVelocity(-vx, -vy)
                    bricks_hit.append(brick)

        return bricks_hit

    @staticmethod
    def _handleBricks(gamebox: GameBox, player: Player, bricks: list[Brick]) -> None:
        
        for brick in bricks:
            brick.makeBrickLooseHP(loss=1)
            if brick.isBroken():
                gamebox.removeBrick(brick=brick)
                ...  # TODO : spawn bonus si bonus
                player.getScore().addScore(increment=brick.getBrickValue())
            ... # TODO : changer le sprite de la brique si nécessaire

    @staticmethod
    def _handleBalls(gamebox: GameBox, player: Player) -> None:
        # Step 1: Move les balls dans la gamebox
        gamebox.tryMoveBalls()
        # Step 2: Vérifier les collisions
        GameEngine._handleCollisionsWithRaquette(gamebox=gamebox)
        b = GameEngine._handleCollisionWithBricks(gamebox=gamebox)
        # Step 3: Gérer les briques
        GameEngine._handleBricks(gamebox=gamebox, player=player, bricks=b)

    @staticmethod
    def _handleCollisionWithEntities(gamebox: GameBox, player: Player) -> None:

        for entity in gamebox.getEntities():
            
            # on move l'entité, puis on check si elle est en collision avec la raquette
            falling_pos: Position2D = entity.getGravityPosition()
            entity.moveToCoords(p=falling_pos)

            # On vérifie si tu récupères 
            if CollisionHelper.isColliding(entity.getHitbox(), gamebox.getRaquette().getHitbox()):
                player.addBonus(b=entity)
                gamebox.removeEntity(entity=entity)

            # Sinon, on vérifie si elle ne sort pas de l'écran. Auquel cas, on peut la détruire.
            elif gamebox.isObjectOutOfBounds(object=entity):
                gamebox.removeEntity(entity=entity)

            else: ...

    @staticmethod
    def _handleBonusLogic(gamebox: GameBox, player: Player) -> None:
        ...

    @staticmethod
    def _handleBonus(gamebox: GameBox, player: Player) -> None:
        GameEngine._handleCollisionWithEntities(gamebox=gamebox, player=player)
        GameEngine._handleBonusLogic(gamebox=gamebox, player=player)

    @staticmethod
    def handle_routine(gamebox: GameBox, player: Player) -> None:
        a = GameEngine._handleInputs(controller=player.getController())
        GameEngine._handleActions(gamebox=gamebox, action=a)
        GameEngine._handleBalls(gamebox=gamebox, player=player)
        GameEngine._handleBonus(gamebox=gamebox, player=player)