


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
    def _handle_actions() -> None:
        ...

    @staticmethod
    def handle_velocity() -> None:
        ...