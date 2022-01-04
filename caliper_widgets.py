import tkinter as tk
from config import *
from info_widgets import *


class Caliper_Input:
    def __init__(self, ws, callback):
        self.callback = callback
        self.buffer = ""
        ws.bind("<Key>", self.process_key)

    def process_key(self, event):
        if event.keysym == "Return":
            if self.valid_input(self.buffer):
                self.callback(self.buffer)
            self.buffer = ""
        else:
            self.buffer = self.buffer + event.char

    def valid_input(self, input):
        try:
            test = float(input)
            return True
        except:
            return False


class Caliper_Widgets:
    def __init__(self, ws, callback) -> None:
        self.ws = ws
        self.callback = callback
        self.fields = ["MP", "MC", "PC", "Waypoint"]
        self.widgets = {}
        for w in self.fields:
            self.widgets[w] = Number_Widget(ws, w, color=LABEL_COLOR)

            def select(event, self=self, w=w):
                self.__select(event, w)

            self.widgets[w].frame.bind("<Enter>", select)
        self.focus = self.fields[0]
        self.widgets[self.focus].set_focus()
        self.caliper_input = Caliper_Input(ws, self.input_callback)

    def __select(self, event, widget):
        self.widgets[self.focus].remove_focus()
        self.focus = widget
        self.widgets[self.focus].set_focus()

    def input_callback(self, input_value):
        yards = lambda v: float(v) * 1760.0 / 2.0
        self.widgets[self.focus].set_value(int(yards(input_value)))
        self.callback(self.focus, yards(input_value))
