

from src.game.game_box import GameBox

from src.physics.solid_shapes import SolidRectangle, SolidCircle

from src.common import BRICK_COLORS

import tkinter as tk
import time



class GameGUI(tk.Tk):

    def __init__(self, gamebox: GameBox):
        super().__init__()
        self.title(f"Arkanoid Python")
        self.canvas: tk.Canvas = tk.Canvas(self, width=gamebox.getWidth(), height=gamebox.getHeight())
        self.canvas.pack()
        self.gamebox = gamebox
        self.lastupdate = time.time()

    def update_gui(self):
        self.canvas.delete("all")
        self.draw_rectangle(self.gamebox.getRaquette().getHitbox(), fill="blue")
        for ball in self.gamebox.getBalls(): self.draw_circle(ball.getHitbox(), fill="red")
        for brick in self.gamebox.getBricks(): self.draw_rectangle(brick.getHitbox(), fill=BRICK_COLORS[brick.getBrickType()])
        for bonus in self.gamebox.getBonuses(): self.draw_rectangle(bonus.getHitbox(), fill='black')
        self.update_fps()

    def update_fps(self):
        current = time.time()
        delta = current - self.lastupdate
        fps = 1 / delta if delta > 0 else 0
        self.lastupdate = current
        self.title(f'Arkanoid Python - {round(fps)} FPS')

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

