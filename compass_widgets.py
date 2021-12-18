import math
from tkinter import LAST
from config import *


class Compass:
    def __init__(self, canvas, x0, y0, scale) -> None:
        self.canvas = canvas
        self.center = (x0, y0)
        self.clue_vector = {
            "arrow": 0,
            "pivot_point": 0,
            "clue_circle": 0,
            "clue_distance": 0,
        }
        self.create_dial()

    def coords(self, p):
        (x, y) = p
        (x0, y0) = self.center
        x = x + x0
        y = CANVAS_HEIGHT - y - y0
        return (x, y)

    def create_dial(self):
        (x, y) = self.center
        self.bezel_marks = []
        self.bezel_labels = []

        self.canvas.create_oval(
            x - DIAL_OUTER,
            y - DIAL_OUTER,
            x + DIAL_OUTER,
            y + DIAL_OUTER,
            outline=DIAL_COLOR,
            width=3,
        )
        self.canvas.create_oval(
            x - DIAL_INNER,
            y - DIAL_INNER,
            x + DIAL_INNER,
            y + DIAL_INNER,
            outline=DIAL_COLOR,
            width=3,
        )
        self.rotate_bezel(0)
        self.draw_travel_arrow()
        self.create_clue_vector()

    def rotate_bezel(self, angle):
        for l in self.bezel_labels:
            self.canvas.delete(l)
        self.bezel_labels.clear()
        self.bezel_labels.append(self.bezel_text("N", angle + 0))
        self.bezel_labels.append(self.bezel_text("E", angle + 90))
        self.bezel_labels.append(self.bezel_text("S", angle + 180))
        self.bezel_labels.append(self.bezel_text("W", angle + 270))
        for m in self.bezel_marks:
            self.canvas.delete(m)
        self.bezel_marks.clear()
        for m in range(0, 360, 5):
            major_mark = m % 15 == 0
            self.bezel_marks.append(self.bezel_tick(angle + m, major_mark))

    def bezel_text(self, text, angle):
        angle_r = math.radians(angle)
        p = (
            BEZEL_RADIUS * math.sin(angle_r),
            BEZEL_RADIUS * math.cos(angle_r),
        )
        id = self.canvas.create_text(*self.coords(p), text=text, angle=-angle)
        return id

    def bezel_tick(self, angle, major_mark):
        angle_r = math.radians(angle)
        if major_mark:
            longer = 4
        else:
            longer = 0
        p1 = (
            (BEZEL_RADIUS - longer) * math.sin(angle_r),
            (BEZEL_RADIUS - longer) * math.cos(angle_r),
        )
        p2 = (DIAL_OUTER * math.sin(angle_r), DIAL_OUTER * math.cos(angle_r))
        id = self.canvas.create_line(
            *self.coords(p1), *self.coords(p2), fill=DIAL_COLOR
        )
        return id

    def draw_travel_arrow(self):
        tail_right = (
            DIAL_INNER * math.sin(math.radians(TA_TAIL_ANGLE)),
            DIAL_INNER * math.cos(math.radians(TA_TAIL_ANGLE)),
        )
        (x, y) = tail_right
        tail_left = (-x, y)
        self.canvas.create_polygon(
            *self.coords(TRAVEL_ARROW_TIP),
            *self.coords(tail_right),
            *self.center,
            *self.coords(tail_left),
            *self.coords(TRAVEL_ARROW_TIP),
            fill=TRAVEL_ARROW_COLOR,
        )

    def create_clue_vector(self):
        vector_tip = (
            0,
            CLUE_VECTOR_LENGTH,
        )
        self.clue_vector["arrow"] = self.canvas.create_line(
            *self.center,
            self.coords(vector_tip),
            arrow=LAST,
            arrowshape=ARROWSHAPE,
            fill=CLUE_VECTOR_COLOR,
            width=3,
        )
        x, y = self.center
        r = 2
        self.clue_vector["pivot_point"] = self.canvas.create_oval(
            x - r, y - r, x + r, y + r, fill=CLUE_VECTOR_COLOR
        )
        clue_center = (
            0,
            CLUE_VECTOR_LENGTH + CLUE_CIRCLE_RADIUS,
        )

        x, y = self.coords(clue_center)

        self.clue_vector["clue_circle"] = self.canvas.create_oval(
            x - CLUE_CIRCLE_RADIUS,
            y - CLUE_CIRCLE_RADIUS,
            x + CLUE_CIRCLE_RADIUS,
            y + CLUE_CIRCLE_RADIUS,
            outline=CLUE_VECTOR_COLOR,
        )
        self.clue_vector["clue_distance"] = self.canvas.create_text(
            *self.coords(clue_center),
            text=UNSPECIFIED,
            font=(FONT, INFO_TEXT_SIZE),
            fill=CLUE_VECTOR_COLOR,
        )

    def draw_clue_vector(self, angle, dist):
        vector_tip = (
            CLUE_VECTOR_LENGTH * math.sin(math.radians(angle)),
            CLUE_VECTOR_LENGTH * math.cos(math.radians(angle)),
        )
        self.canvas.coords(
            self.clue_vector["arrow"], *self.center, *self.coords(vector_tip)
        )

        clue_center = (
            (CLUE_VECTOR_LENGTH + CLUE_CIRCLE_RADIUS) * math.sin(math.radians(angle)),
            (CLUE_VECTOR_LENGTH + CLUE_CIRCLE_RADIUS) * math.cos(math.radians(angle)),
        )

        x, y = self.coords(clue_center)

        self.canvas.coords(
            self.clue_vector["clue_circle"],
            x - CLUE_CIRCLE_RADIUS,
            y - CLUE_CIRCLE_RADIUS,
            x + CLUE_CIRCLE_RADIUS,
            y + CLUE_CIRCLE_RADIUS,
        )
        self.canvas.itemconfig(self.clue_vector["clue_distance"], text=str(dist))
        self.canvas.coords(self.clue_vector["clue_distance"], self.coords(clue_center))
