


from src.game.ball import Ball
from src.game.raquette import Raquette
from src.game.game_box import GameBox
from src.game.brick import Brick

from src.common import Position2D, BrickType
from src.gui.gui import GameGUI
from src.engine import GameEngine






if __name__ == "__main__":

    gamebox: GameBox = GameBox(
        position=Position2D(0, 0),
        width=800,
        height=800,
        balls=[
            Ball(Position2D(200, 200), 10, 10),
            Ball(Position2D(10, 10), 10, 20)
        ],
        raquette=Raquette(Position2D(150, 400), 300, 20, 10),
        bricks=[Brick(Position2D(50, 50), 60, 20, BrickType.CYAN), Brick(Position2D(200, 50), 60, 20, BrickType.SILVER)]
    )

    gui: GameGUI = GameGUI(gamebox)

    def mainloop():
        GameEngine.handle_routine(gamebox=gamebox)
        gui.update_gui()
        gui.after(16, mainloop)

    mainloop()
    gui.mainloop()
