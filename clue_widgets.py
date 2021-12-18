import tkinter as tk
import json
from config import *
from info_widgets import *
from helpers import *


class Clue_Data:
    def __init__(self, ws):
        self.data = {}
        with open(HUNT_FILE, "r") as f:
            self.data = json.load(f)
        self.hunt_timer = Timer_Widget(ws, "Hunt Timer", "count_down", TOTAL_HUNT_TIME)
        self.clue_timer = Timer_Widget(ws, "Clue Timer", "count_up", 0)
        self.clue_credits = Number_Widget(ws, "Solved", INFO_TEXT_COLOR, INFO_WIDTH)
        self.emergencies = Number_Widget(ws, "Emergencies", INFO_TEXT_COLOR, INFO_WIDTH)
        self.average_time = Time_Display_Widget(ws, "Average Time")

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
        self.clue_credits.set_value(c)
        self.emergencies.set_value(e)
        if c <= 0:
            self.average_time.set_time(0)
        else:
            elapsed_time = TOTAL_HUNT_TIME - self.hunt_timer.counter
            penalty_time = e * EMERGENCY_PENALTY
            t = int((elapsed_time + penalty_time) / c)
            self.average_time.set_time(t)


class Clue_Widgets:
    def __init__(self, ws, label):
        self.frame = tk.LabelFrame(
            ws,
            text=label,
            font=(FONT, LABEL_TEXT_SIZE),
            bg=MAIN_BG,
            fg=LABEL_TEXT_COLOR,
            relief=FRAME,
            bd=BD_SIZE,
            labelanchor="n",
        )
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
            self.fields[c].grid(row=0, column=CLUE_LETTERS.index(c), pady=PADY)
        self.mode = "selection"
        self.selected = CLUE_LETTERS[0]
        self.highlight_selected()

    def update_status_color(self):
        self.fields[self.selected].config(fg=STATUS_COLORS[self.new_status])

    def select_next(self):
        self.unhighlight_selected()
        self.selected = select_item(self.selected, CLUE_LETTERS, "next")
        self.highlight_selected()

    def select_previous(self):
        self.unhighlight_selected()
        self.selected = select_item(self.selected, CLUE_LETTERS, "previous")
        self.highlight_selected()

    def highlight_selected(self):
        self.highlighted = True
        if self.fields[self.selected].cget("fg") == HIGHLIGHT_BG:
            self.fields[self.selected].config(bg=HIGHLIGHT_BG, fg=MAIN_BG)
        else:
            self.fields[self.selected].config(
                bg=HIGHLIGHT_BG,
            )

    def unhighlight_selected(self):
        self.highlighted = False
        if self.fields[self.selected].cget("fg") == MAIN_BG:
            self.fields[self.selected].config(bg=MAIN_BG, fg=HIGHLIGHT_BG)
        else:
            self.fields[self.selected].config(bg=MAIN_BG)

    def blink_selected(self):
        if self.highlighted:
            self.unhighlight_selected()
        else:
            self.highlight_selected()
        if self.blinking:
            self.frame.after(BLINK_TIME, self.blink_selected)
        else:
            self.highlight_selected()

    def blink(self):
        self.blinking = True
        self.blink_selected()

    def no_blink(self):
        self.blinking = False

    def enter_edit_mode(self):
        self.blink()
        self.mode = "edit"
        self.new_status = self.data.get_status(self.selected)

    def exit_edit_mode(self):
        self.no_blink()
        self.mode = "selection"
        self.data.put_status(self.selected, self.new_status)
        self.unhighlight_selected()
        self.selected = select_item(self.selected, CLUE_LETTERS, "next")
        self.highlight_selected()

    def process_button_event(self):
        if self.mode == "selection":
            self.enter_edit_mode()
        else:
            self.exit_edit_mode()

    def process_cw_event(self):
        if self.mode == "selection":
            self.select_next()
        else:
            self.new_status = select_item(self.new_status, CLUE_STATUS, "next")
            self.update_status_color()

    def process_ccw_event(self):
        if self.mode == "selection":
            self.select_previous()
        else:
            self.new_status = select_item(self.new_status, CLUE_STATUS, "previous")
            self.update_status_color()
