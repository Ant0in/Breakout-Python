
from src.game.game_box import GameBox
from src.game.ball import Ball
from src.game.raquette import Raquette
from src.game.brick import Brick
from src.game.score import Score
from src.game.bonus import DuplicationBonus

from src.common import Position2D, BrickType
from src.gui.gui import GameGUI
from src.engine import GameEngine
from src.controller import GameController


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
            Brick(Position2D(x, y), 60, 20, BrickType((i % 8) + 1))
            for i in range(12)
            for _, y in enumerate(range(50, 150, 25))
            for x in [50 + i * 62]
        ]
    )

    score: Score = Score(init_val=0)
    controller: GameController = GameController(config=None)
    gui: GameGUI = GameGUI(gamebox)

    def mainloop():
        GameEngine.handle_routine(gamebox=gamebox, controller=controller, score=score)
        gui.update_gui()
        gui.after(16, mainloop)

    mainloop()
    gui.mainloop()
