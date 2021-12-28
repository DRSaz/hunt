import tkinter as tk
import time
from config import *
from helpers import select_item


class Info_Widget:
    def __init__(self, ws, label, color, width):
        self.color = color
        self.highlighted = False
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
        self.widget = tk.Label(
            self.frame,
            text=UNSPECIFIED,
            font=(FONT, INFO_TEXT_SIZE),
            bg=MAIN_BG,
            fg=color,
            width=width,
        )
        self.widget.pack(padx=PADX, pady=PADY)


class Time_Display_Widget(Info_Widget):
    def __init__(self, ws, label):
        super().__init__(ws, label, INFO_TEXT_COLOR, INFO_WIDTH)

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

    def start(self):
        self.start_time = time.time()
        self.update()

    def elapsed_time(self):
        return time.time()-self.start_time

    def update(self):
 
        self.set_time(self.start_value + (self.elapsed_time() * self.direction))
        self.widget.after(TIMER_REFRESH, self.update)


class Entry_Widget(Info_Widget):
    def __init__(self, ws, label, color, width):
        super().__init__(ws, label, color, width)

    def highlight(self):
        self.highlighted = True
        self.widget.config(bg=self.color, fg=MAIN_BG)

    def unhighlight(self):
        self.highlighted = False
        self.widget.config(bg=MAIN_BG, fg=self.color)

    def blink_highlight(self):
        if self.highlighted:
            self.unhighlight()
        else:
            self.highlight()
        self.frame.after(BLINK_TIME, self.blink_highlight)


class Number_Widget(Info_Widget):
    def __init__(self, ws, label, color, width):
        super().__init__(ws, label, color, width)

    def set_value(self, value):
        self.widget.config(text=str(value))


class Number_Entry_Widget(Entry_Widget):
    def __init__(self, ws, label, units, color, width):
        super().__init__(ws, label, color, width)
        if units != "":
            self.units = " " + units
        else:
            self.units = ""

    def set_value(self, value):
        self.widget.config(text=str(value) + self.units)


class Option_Selection_Widget(Entry_Widget):
    def __init__(self, ws, label, options, color, width):
        super().__init__(ws, label, color, width)
        self.options = options
        self.current_option = self.options[0]
        self.widget.config(text=self.current_option)

    def next(self):
        self.current_option = select_item(self.current_option, self.options, "next")
        self.widget.config(text=self.options[self.current_option])

    def previous(self):
        self.current_option = select_item(self.current_option, self.options, "previous")
        self.widget.config(text=self.options[self.current_option])


class Null_Widget:
    def highlight(self):
        pass

    def unhighlight(self):
        pass
