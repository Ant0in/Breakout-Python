

from src.player.score import Score
from src.player.controller import GameController
from src.game.bonus import BonusInterface



class Player:

    def __init__(self, controller: GameController | None = None, score: Score | None = None,
                 bonus: list[BonusInterface] | None = None):
        
        self._controller: GameController = controller if controller else GameController(config=None)
        self._score: Score = score if score else Score(init_val=0)
        self._bonus: list[BonusInterface] = bonus if bonus else list()

    def getController(self) -> GameController:
        return self._controller
    
    def getScore(self) -> Score:
        return self._score
    
    def getBonus(self) -> list[BonusInterface]:
        return self._bonus

