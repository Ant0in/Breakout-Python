

from src.common import Action

import keyboard



class GameController:
    
    DEFAULT: dict = {
        'left': Action.LEFT,
        'right': Action.RIGHT,
    }

    def __init__(self, config: dict | None = None) -> None:
        self._config: dict = config if config else GameController.DEFAULT

    def getConfig(self) -> dict:
        return self._config

    def getUserAction(self) -> Action:
        
        # Pour chaque key, on va vérifier si le player l'appuie (polling)
        for k, a in self.getConfig().items():
            if keyboard.is_pressed(k): return a
        
        # Aucune action
        return Action._NONE

