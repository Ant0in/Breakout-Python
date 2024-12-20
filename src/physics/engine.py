

from src.game.game_box import GameBox
from src.game.brick import Brick
from src.game.bonus import BonusInterface
from src.game.ball import Ball

from src.player.player import Player
from src.player.controller import GameController

from src.physics.collision_helper import CollisionHelper

from src.common import Position2D, Action, BALL_RADIUS, BALL_SPEED
import math
import sys


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
                x: float = ball.getCenterPosition().getX() - gamebox.getRaquette().getCenterPosition().getX()
                alpha: float = (math.pi / 6) + ((5 * math.pi) / 6) * (1 - (x / L))  # modifiée pour 30->150
                dvx: float = total_velocity * math.sin(alpha)
                dvy: float = total_velocity * math.cos(alpha)

                ball.setVelocity(dvx, dvy)
                ball.setCenterPosition(p=Position2D(ball.getCenterPosition().getX(), gamebox.getRaquette().getPosition().getY() - ball.getRadius()))

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
    def _calculateBonusSpawnPosition(brick: Brick, bonus: BonusInterface) -> Position2D:
        brick_center: Position2D = brick.getCenterPosition()
        offset_center: Position2D = Position2D(brick_center.getX() - bonus.getSize() / 2, brick_center.getY() - bonus.getSize() / 2)
        return offset_center

    @staticmethod
    def _handleBricks(gamebox: GameBox, player: Player, bricks: list[Brick]) -> None:
        
        for brick in bricks:

            brick.makeBrickLooseHP(loss=1)
            # Si la brique casse, on la remove
            if brick.isBroken():
                gamebox.removeBrick(brick=brick)

                # Si la brique contient un bonus ET que le joueur n'a qu'une seule balle, on le fait spawn
                if brick.doesBrickContainsBonus() and not gamebox.doesPlayerHaveMutlipleBalls():
                    bonus: BonusInterface = brick.getBonus()
                    gamebox.addBonus(bonus=bonus)
                    bonus.spawnBonus(p=GameEngine._calculateBonusSpawnPosition(brick=brick, bonus=bonus))

                # Puis on ajoute le score obtenu
                player.getScore().addScore(increment=brick.getBrickValue())

            else:
                ... # TODO : changer le sprite de la brique si nécessaire

    @staticmethod
    def _handleDeadBalls(gamebox: GameBox) -> None:
        for ball in gamebox.getBalls():
            if not ball.isAlive():
                gamebox.removeBall(b=ball)

    @staticmethod
    def _handleBalls(gamebox: GameBox, player: Player) -> None:
        # Step 1: Move les balls dans la gamebox
        gamebox.tryMoveBalls()
        # Step 2: Vérifier les collisions
        GameEngine._handleCollisionsWithRaquette(gamebox=gamebox)
        b = GameEngine._handleCollisionWithBricks(gamebox=gamebox)
        # Step 3: Gérer les briques
        GameEngine._handleBricks(gamebox=gamebox, player=player, bricks=b)
        # Step 4: Dégager les balls qui sont mortes
        GameEngine._handleDeadBalls(gamebox=gamebox)

    @staticmethod
    def _handleCollisionWithEntities(gamebox: GameBox, player: Player) -> None:

        for bonus in gamebox.getBonuses():
            
            # on move l'entité, puis on check si elle est en collision avec la raquette
            falling_pos: Position2D = bonus.getGravityPosition()
            bonus.setPosition(p=falling_pos)

            # On vérifie si tu récupères 
            if CollisionHelper.isColliding(bonus.getHitbox(), gamebox.getRaquette().getHitbox()):
                player.addBonus(b=bonus)
                bonus.setActive(flag=True)
                gamebox.removeBonus(bonus=bonus)

            # Sinon, on vérifie si elle ne sort pas de l'écran. Auquel cas, on peut la détruire.
            elif gamebox.isObjectOutOfBounds(object=bonus):
                gamebox.removeBonus(bonus=bonus)

    @staticmethod
    def _handleBonusLogic(gamebox: GameBox, player: Player) -> None:
        
        for bonus in player.getBonus():
            # On exécute la logique, puis si expired alors on le remove.
            bonus.applyLogic(gb=gamebox, player=player)
            if bonus.hasBonusDurationExpired():
                player.removeBonus(b=bonus)

    @staticmethod
    def _handleBonus(gamebox: GameBox, player: Player) -> None:
        GameEngine._handleCollisionWithEntities(gamebox=gamebox, player=player)
        GameEngine._handleBonusLogic(gamebox=gamebox, player=player)

    @staticmethod
    def _handleBallSpawn(gamebox: GameBox) -> None:
        
        # TODO : Faire une belle fonction de spawn fonctionnelle
        # TODO : qui gère proprement la remise de la balle en jeu.
        center: Position2D = gamebox.getCenterPosition()
        b: Ball = Ball(center=center, radius=BALL_RADIUS, speed=BALL_SPEED)
        gamebox.addBall(b=b)

    @staticmethod
    def _handleGameOver(gamebox: GameBox, player: Player) -> None:

        # TODO : Gameover handling.
        print('loose')
        sys.exit(0)

    @staticmethod
    def _handleWin(gamebox: GameBox, player: Player) -> None:

        # TODO : Win handling.
        print('win')
        sys.exit(0)

    @staticmethod
    def _handleGameState(gamebox: GameBox, player: Player) -> None:
        
        # Step 1: Vérifier si la game est en état "win"
        if gamebox.isWin():
            GameEngine._handleWin(gamebox=gamebox, player=player)

        # Step 2: Vérifier si le vecteur de ball est vide (état: perte de vie)
        if gamebox.isBallVectorEmpty():
            player.incrementHp(incr=-1)
            # Puis vérifier si le player est en vie
            if player.isDead(): GameEngine._handleGameOver(gamebox=gamebox, player=player)
            else: GameEngine._handleBallSpawn(gamebox=gamebox)

    @staticmethod
    def handle_routine(gamebox: GameBox, player: Player) -> None:
        a: Action = GameEngine._handleInputs(controller=player.getController())
        GameEngine._handleActions(gamebox=gamebox, action=a)
        GameEngine._handleBalls(gamebox=gamebox, player=player)
        GameEngine._handleBonus(gamebox=gamebox, player=player)
        GameEngine._handleGameState(gamebox=gamebox, player=player)

