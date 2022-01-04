from config import *
from helpers import *


class Navigation_Data:
    def __init__(self) -> None:

        self.points = {
            "M": (0, -SCALE_REFERENCE / 2),
            "P": (0, SCALE_REFERENCE / 2),
            "C": (SCALE_REFERENCE / 2, SCALE_REFERENCE / 2),
        }
        self.lines = {
            "MP": (self.points["M"], self.points["P"]),
            "MC": (self.points["M"], self.points["C"]),
            "PC": (self.points["P"], self.points["C"]),
        }
        self.modes = ["Waypoint", "Triangulation"]
