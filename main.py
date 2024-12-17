
from src.game.game_box import GameBox
from src.game.ball import Ball
from src.game.raquette import Raquette
from src.game.brick import Brick
from src.game.bonus import DuplicationBonus

from src.player.player import Player
from src.player.score import Score
from src.player.controller import GameController

from src.gui.gui import GameGUI

from src.physics.engine import GameEngine

from src.common import Position2D, BrickType



if __name__ == "__main__":

    gamebox: GameBox = GameBox(
        position=Position2D(0, 0),
        width=800,
        height=800,
        balls=[
            Ball(Position2D(400, 350), 10, 15),
            Ball(Position2D(400, 250), 10, 15),
        ],
        raquette=Raquette(Position2D(300, 700), 200, 20, 10),
        bricks=[
            Brick(Position2D(x, y), 60, 20, BrickType((i % 10) + 1), DuplicationBonus())
            for i in range(12)
            for _, y in enumerate(range(50, 150, 25))
            for x in [50 + i * 62]
        ]
    )

    player: Player = Player(controller=None, score=None, bonus=None)
    gui: GameGUI = GameGUI(gamebox)

    def mainloop():
        GameEngine.handle_routine(gamebox=gamebox, player=player)
        gui.update_gui()
        gui.after(16, mainloop)

    mainloop()
    gui.mainloop()
