import tkinter as tk
import time
from config import *
from helpers import select_item


class Info_Widget:
    def __init__(self, ws, label, text=UNSPECIFIED, color=INFO_COLOR, width=INFO_WIDTH):
        self.color = color
        self.focus = False
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
        self.widget = tk.Label(
            self.frame,
            text=text,
            font=(FONT, INFO_TEXT_SIZE),
            bg=MAIN_BG,
            fg=color,
            width=width,
        )
        self.widget.pack(padx=PADX, pady=PADY)

    def set_focus(self):
        self.focus = True
        self.widget.config(bg=self.color, fg=MAIN_BG)

    def remove_focus(self):
        self.focus = False
        self.widget.config(bg=MAIN_BG, fg=self.color)


class Time_Display_Widget(Info_Widget):
    def __init__(self, ws, label):
        super().__init__(ws, label)

    def set_time(self, time):
        time = round(time)
        if time // HOUR == 0:
            hours = ""
        else:
            hours = str(time // HOUR) + ":"
        minutes = str((time % HOUR) // MINUTE).rjust(2, "0") + ":"
        seconds = str(time % MINUTE).rjust(2, "0").rjust(2, "0")
        self.widget.config(text=hours + minutes + seconds)


class Timer_Widget(Time_Display_Widget):
    def __init__(self, ws, label, direction, start_value):
        super().__init__(ws, label)
        if direction == "count_down":
            self.direction = -1
        else:
            self.direction = 1
        self.start_value = start_value
        self.set_time(self.start_value)

    def reset(self, offset):
        self.start_time = time.time() - offset

    def start(self):
        self.start_time = time.time()
        self.update()

    def elapsed_time(self):
        return time.time() - self.start_time

    def update(self):
        self.set_time(self.start_value + (self.elapsed_time() * self.direction))
        self.widget.after(TIMER_REFRESH, self.update)


class Number_Widget(Info_Widget):
    def __init__(self, ws, label, text=UNSPECIFIED, color=INFO_COLOR, width=INFO_WIDTH):
        super().__init__(ws, label, text, color, width)

    def set_value(self, value):
        if value == 0:
            self.widget.config(text=UNSPECIFIED)
        else:
            self.widget.config(text=str(value))
