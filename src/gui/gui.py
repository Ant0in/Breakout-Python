

import tkinter as tk
from src.common import Position2D
from src.game.ball import Ball
from src.game.raquette import Raquette
from src.game.solid_shapes import SolidRectangle, SolidCircle
from src.game.game_box import GameBox



class GameGUI(tk.Tk):

    def __init__(self, gamebox: GameBox):
        super().__init__()
        self.title("Arkanoid Python")
        self.canvas: tk.Canvas = tk.Canvas(self, width=gamebox.getWidth(), height=gamebox.getHeight())
        self.canvas.pack()
        self.gamebox = gamebox

    def update_gui(self):

        self.canvas.delete("all")

        # dessiner les raquettes
        self.draw_rectangle(self.gamebox.getRaquette().getHitbox(), fill="blue")
        # dessiner les balls
        for ball in self.gamebox.getBalls(): self.draw_circle(ball.getHitbox(), fill="red")
        # dessiner les bricks
        for brick in self.gamebox.getBricks(): self.draw_rectangle(brick, fill="green")
    
    def draw_rectangle(self, rect: SolidRectangle, fill: str) -> None:
        x1: float = rect.getPosition().getX()
        y1: float = rect.getPosition().getY()
        x2: float = rect.getPosition().getX() + rect.getWidth()
        y2: float = rect.getPosition().getY() + rect.getHeight()
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill)

    def draw_circle(self, circle: SolidCircle, fill: str) -> None:
        x: float = circle.getPosition().getX()
        y: float = circle.getPosition().getY()
        r: float = circle.getRadius()
        self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=fill)


