import tkinter as tk
from config import *
from info_widgets import *
from clue_widgets import *
from nav_widgets import *


root = tk.Tk()
root.config(bg=MAIN_BG)
# root.geometry("800x480")
# root.overrideredirect(1)
# root.config(cursor="none")


clues = Clue_Widgets(root, "Clue Status")
nav = Navigation_Widgets(root)

# Arrange the widgets on the grid
# Hunt Status Row
clues.data.hunt_timer.frame.grid(row=0, column=0, padx=PADX, pady=PADY, sticky="w")
clues.data.clue_credits.frame.grid(row=0, column=1, padx=PADX, pady=PADY)
clues.data.emergencies.frame.grid(row=0, column=2, padx=PADX, pady=PADY)
clues.data.average_time.frame.grid(row=0, column=3, padx=PADX, pady=PADY)
clues.data.clue_timer.frame.grid(row=0, column=4, padx=PADX, pady=PADY, sticky="e")

# Navigation Info Layout
nav.fields["MP"].frame.grid(row=1, column=4, padx=PADX, pady=PADY, sticky="e")
nav.fields["MC"].frame.grid(row=2, column=4, padx=PADX, pady=PADY, sticky="e")
nav.fields["PC"].frame.grid(row=3, column=4, padx=PADX, pady=PADY, sticky="e")
nav.fields["WT"].frame.grid(row=4, column=4, padx=PADX, pady=PADY, sticky="e")

# canvas
nav.canvas.grid(row=1, column=0, columnspan=4, rowspan=4, padx=PADX, pady=PADY)

# Clue Status Row
clues.frame.grid(row=5, column=0, columnspan=5, padx=PADX, pady=PADY)

# Setup the rotoray encoders for menu selection input.
clue_encoder = Encoder(
    root, clues.process_cw_event, clues.process_ccw_event, clues.process_button_event
)
nav_encoder = Encoder(
    root, nav.process_cw_event, nav.process_ccw_event, nav.process_button_event
)
toggle = Encoder_Toggle(root, [clue_encoder, nav_encoder])

angle = 0

clues.data.hunt_timer.start()
clues.data.clue_timer.start()


def spin():
    global angle
    nav.c.rotate_bezel(angle)
    nav.c.draw_clue_vector(360 - angle, angle)
    angle = (angle + 1) % 360
    root.after(200, spin)


spin()

root.mainloop()
