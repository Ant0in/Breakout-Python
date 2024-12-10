

from src.game.collision_helper import CollisionHelper
from src.game.solid_shapes import SolidInterface, SolidCircle, SolidRectangle
from src.game.ball import Ball
from src.game.raquette import Raquette
from src.game.game_box import GameBox

from src.common import Position2D
from src.gui.gui import GameGUI
from src.engine import GameEngine



if __name__ == "__main__":

    gamebox: GameBox = GameBox(
        position=Position2D(0, 0),
        width=800,
        height=800,
        balls=[
            Ball(Position2D(200, 200), 10, 10),
            Ball(Position2D(600, 400), 50, 5)
        ],
        raquette=Raquette(Position2D(150, 400), 300, 20, 10)
    )

    bricks: list[SolidRectangle] = [SolidRectangle(Position2D(50, 50), 60, 20), SolidRectangle(Position2D(200, 50), 60, 20)] 
    for brick in bricks: gamebox.addBrick(brick)

    gui: GameGUI = GameGUI(gamebox)
    def game_loop():
        GameEngine._handle_balls(gamebox=gamebox)
        gui.update_gui()
        gui.after(16, game_loop)

    game_loop()
    gui.mainloop()
