from config import *
from helpers import *


class Data:
    def __init__(self) -> None:

        self.points = {
            "M": (0, -SCALE_REFERENCE / 2),
            "W": (0, -SCALE_REFERENCE / 2),
            "P": (0, SCALE_REFERENCE / 2),
            "T": (0, SCALE_REFERENCE / 2),
            "C": (DEF_CLUE_OFFSET, SCALE_REFERENCE / 2),
            "MP_label": (-SCALE_LABEL_OFFSET, 0),
            "WT_label": (-SCALE_LABEL_OFFSET, 0),
        }
        self.lines = {
            "MP": distance(self.points["M"], self.points["P"]),
            "MC": distance(self.points["M"], self.points["C"]),
            "PC": distance(self.points["P"], self.points["C"]),
            "WT": distance(self.points["W"], self.points["T"]),
        }
        self.modes = {
            "line": {
                "scale": 1.0,
                "fields": ["WT"],
                "view": ["WT", "W", "T", "WT_label"],
            },
            "triangle": {
                "scale": 1.0,
                "fields": ["MP", "MC", "PC"],
                "view": ["MP", "MC", "PC", "M", "P", "C", "MP_label"],
            },
        }


d = Data()

print(d.points)
d.points["M"] = (-1000, 999)
for p in d.points:
    print(d.points[p])


print(d.lines)

for l in d.lines:
    p0, p1 = tuple(l)
    print(f"p0:{p0} p1:{p1} len:{str(d.lines[l])}")

print(d.modes)
print(d.modes["line"]["scale"])
print(d.modes["line"]["fields"])
print(d.modes["line"]["view"])

d.modes["line"]["scale"] = 5
print(d.modes["line"]["scale"])
