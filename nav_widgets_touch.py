import tkinter as tk
from config import *
from graph_widgets_touch import *
from compass_widgets import Compass


class Navigation_Widgets:
    def __init__(self, ws):
        self.ws = ws
        self.points = {
            "M": (0, -SCALE_REFERENCE / 2),
            "P": (0, SCALE_REFERENCE / 2),
            "C": (SCALE_REFERENCE / 2, SCALE_REFERENCE / 2),
            "W": (SCALE_REFERENCE / 2, -SCALE_REFERENCE / 2),
        }
        self.data = {"MP": 0.0, "MC": 0.0, "PC": 0.0, "Waypoint": 0.0}
        self.toggle = 1
        self.canvas = tk.Canvas(
            ws,
            height=CANVAS_HEIGHT,
            width=CANVAS_WIDTH,
            bg=MAIN_BG,
            bd=0,
            relief=FRAME,
            highlightbackground="grey",
            highlightthickness=0,
        )
        self.compass = Compass(self.canvas, COMPASS_CENTER_X, COMPASS_CENTER_Y, 1)
        self.graph = Graph(self.canvas, GRAPH_CENTER_X, GRAPH_CENTER_Y, 1)
        self.graph.create_line("MP", self.points["M"], self.points["P"], self.callback)
        self.graph.create_line("MC", self.points["M"], self.points["C"], self.callback)
        self.graph.create_line("PC", self.points["P"], self.points["C"], self.callback)
        self.graph.create_point("M", self.points["M"], self.callback)
        self.graph.create_point("P", self.points["P"], self.callback)
        self.graph.create_point("C", self.points["C"], self.toggle_side)
        self.graph.create_point("W", self.points["W"], self.callback)

    def toggle_side(self):
        self.toggle = self.toggle * -1
        (x, y) = self.points["C"]
        x = x * -1
        self.points["C"] = (x, y)
        self.graph.update_point("C", self.points["C"])
        self.graph.update_line("MC", self.points["M"], self.points["C"])
        self.graph.update_line("PC", self.points["P"], self.points["C"])

    def process_input(self, field, length):
        self.data[field] = length
        print(self.data)

    def check_triangle():
        pass

    def check_waypoint():
        pass

    def callback(self):
        print("Callback")

    def callback2(self):
        print("Callback2")
