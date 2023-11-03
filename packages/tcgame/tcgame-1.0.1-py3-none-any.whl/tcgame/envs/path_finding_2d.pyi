import tkinter as tk
from _typeshed import Incomplete

UNIT: int
MAZE_H: int
MAZE_W: int
DISTANCE: Incomplete

class Maze(tk.Tk):
    actions: Incomplete
    n_actions: Incomplete
    def __init__(self) -> None: ...
    rect: Incomplete
    def reset(self): ...
    def step(self, action): ...
    def render(self) -> None: ...
