import tkinter as tk
import json
from config import *
from info_widgets import *
from helpers import *


class Clue_Data:
    def __init__(self, ws):
        self.ws = ws
        self.data = {}
        with open(HUNT_FILE, "r") as f:
            self.data = json.load(f)
        self.hunt_timer = Timer_Widget(ws, "Hunt Timer", "count_down", TOTAL_HUNT_TIME)
        self.clue_timer = Timer_Widget(ws, "Clue Timer", "count_up", 0)
        self.clue_credits = Number_Widget(ws, "Clue Credits")
        self.emergencies = Number_Widget(ws, "Emergencies")
        self.average_time = Time_Display_Widget(ws, "Average Time")
        self.prev_clue_elapsed_time = 0
        self.first_clue_credit = 0

        self.menu = tk.Menu(
            ws, tearoff=False, background="grey", font=("helvetica", INFO_TEXT_SIZE)
        )
        self.menu.add_command(
            label="Start Next Clue",
            command=lambda: self.assume_solved(),
        )
        self.menu.add_command(
            label="Resume Previous Clue",
            command=lambda: self.resume_clue(),
        )
        self.menu.add_command(
            label="First Clue Credit",
            command=lambda: self.set_first_clue_credit(),
        )
        self.menu.add_command(
            label="Quit",
            command=lambda: self.cancel(),
        )
        self.clue_timer.frame.bind("<Enter>", self.show_site_menu)

    def cancel(self):
        quit()

    def set_first_clue_credit(self):
        if self.first_clue_credit == 0:
            self.first_clue_credit = self.clue_timer.elapsed_time()
            self.clue_timer.reset(0)

    def assume_solved(self):
        self.prev_clue_elapsed_time = self.clue_timer.elapsed_time()
        self.clue_timer.reset(0)

    def resume_clue(self):
        if self.prev_clue_elapsed_time != 0:
            self.clue_timer.reset(
                self.clue_timer.elapsed_time() + self.prev_clue_elapsed_time
            )
            self.prev_clue_elapsed_time = 0

    def get_status(self, clue):
        return self.data[clue]

    def put_status(self, clue, status):
        self.data[clue] = status
        self.update_stats()

    def update_stats(self):
        c = 0
        e = 0
        for clue in CLUE_LETTERS:
            if self.data[clue] == "Solved":
                c += 1
            elif self.data[clue] == "Half Credit":
                c = c + 0.5
            elif self.data[clue] == "Emergency":
                e += 1
                c += 1
        self.clue_credits.set_value(c)
        self.emergencies.set_value(e)
        if c <= 0:
            self.average_time.set_time(0)
        else:
            penalty_time = e * EMERGENCY_PENALTY
            t = int(
                (self.hunt_timer.elapsed_time() - self.first_clue_credit + penalty_time)
                / c
            )
            self.average_time.set_time(t)

    def show_site_menu(self, event):
        geom = self.ws.geometry()
        parse = geom.split("+")
        x_offset = int(parse[1]) + 225
        y_offset = int(parse[2]) + 150
        self.menu.tk_popup(x_offset, y_offset)


class Clue_Widgets:
    def __init__(self, ws, label):
        self.frame = tk.LabelFrame(
            ws,
            text=label,
            font=(FONT, LABEL_TEXT_SIZE),
            bg=MAIN_BG,
            fg=LABEL_COLOR,
            relief=FRAME,
            bd=BD_SIZE,
            labelanchor="n",
        )
        self.ws = ws
        self.data = Clue_Data(ws)
        self.fields = {}
        for c in CLUE_LETTERS:
            self.fields[c] = tk.Label(
                self.frame,
                text=c,
                font=(FONT, INFO_TEXT_SIZE),
                bg=MAIN_BG,
                fg=STATUS_COLORS[self.data.get_status(c)],
            )
            self.fields[c].grid(row=0, column=CLUE_LETTERS.index(c))

            def select(event, self=self, c=c):
                self.__select(event, c)

            self.fields[c].bind("<Enter>", select)

        self.active_clue = "A"
        self.menu = tk.Menu(
            ws,
            tearoff=False,
            background="grey",
        )
        self.menu.add_command(
            label="Solved",
            command=lambda: self.set_clue_status("Solved"),
            font=("helvetica", INFO_TEXT_SIZE),
        )
        self.menu.add_command(
            label="Emergency",
            command=lambda: self.set_clue_status("Emergency"),
            font=("helvetica", INFO_TEXT_SIZE),
        )
        self.menu.add_command(
            label="Half Credit",
            command=lambda: self.set_clue_status("Half Credit"),
            font=("helvetica", INFO_TEXT_SIZE),
        )
        self.menu.add_command(
            label="Not Found",
            command=lambda: self.set_clue_status("Not Found"),
            font=("helvetica", INFO_TEXT_SIZE),
        )

    def refresh_clue_display(self):
        for c in CLUE_LETTERS:
            self.fields[c].config(bg=MAIN_BG, fg=STATUS_COLORS[self.data.get_status(c)])

    def make_active(self, clue):
        self.refresh_clue_display()
        self.fields[clue].config(bg=HIGHLIGHT_BG)
        if self.data.get_status(clue) == "Not Found":
            self.fields[clue].config(fg=MAIN_BG)
        self.active_clue = clue

    def set_clue_status(self, status):
        self.data.put_status(self.active_clue, status)
        self.fields[self.active_clue].config(fg=STATUS_COLORS[status])
        self.refresh_clue_display()

    def __select(self, event, selection):
        self.make_active(selection)
        geom = self.ws.geometry()
        parse = geom.split("+")
        x_offset = int(parse[1]) + 225
        y_offset = int(parse[2]) + 150

        self.menu.tk_popup(x_offset, y_offset)
