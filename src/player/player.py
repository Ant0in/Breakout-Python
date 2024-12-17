

from src.player.score import Score
from src.player.controller import GameController

from src.game.bonus import BonusInterface



class Player:

    def __init__(self, hp: int = 3, controller: GameController | None = None, score: Score | None = None,
                 bonus: list[BonusInterface] | None = None):
        
        self._hp: int = hp
        self._controller: GameController = controller if controller else GameController(config=None)
        self._score: Score = score if score else Score(init_val=0)
        self._bonus: list[BonusInterface] = bonus if bonus else list()

    def getHp(self) -> int:
        return self._hp
    
    def setHp(self, nhp: int) -> None:
        self._hp = nhp

    def incrementHp(self, incr: int) -> None:
        self.setHp(self.getHp() + incr)

    def isDead(self) -> bool:
        return (self.getHp() <= 0)

    def getController(self) -> GameController:
        return self._controller
    
    def getScore(self) -> Score:
        return self._score
    
    def getBonus(self) -> list[BonusInterface]:
        return self._bonus
    
    def addBonus(self, b: BonusInterface) -> None:
        self.getBonus().append(b)

    def removeBonus(self, b: BonusInterface) -> None:
        if b in self.getBonus(): self.getBonus().remove(b)

