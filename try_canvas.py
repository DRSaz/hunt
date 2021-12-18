import tkinter as tk
from compass_widgets import *
from config import *

root = tk.Tk()
root.config(bg=MAIN_BG)

canvas = tk.Canvas(
    root, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, bg=MAIN_BG, bd=3, relief=FRAME
)
canvas.grid(row=0, column=0)

c = Compass(canvas, CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2, 1)

angle = 0


def spin():
    global angle
    c.rotate_bezel(angle)
    c.draw_clue_vector(360 - angle, angle)
    angle = (angle + 1) % 360
    root.after(200, spin)


spin()

root.mainloop()
