from config import *


class Graph:
    def __init__(self, canvas, x0, y0, scale) -> None:
        self.canvas = canvas
        self.origin_x = x0
        self.origin_y = y0
        self.scale = scale

    def set_scale(self, scale):
        self.scale = scale

    def graph_coords(self, p):
        (x, y) = p
        x = x * self.scale + self.origin_x
        y = CANVAS_HEIGHT - (y * self.scale) - self.origin_y
        return (x, y)

    def graph_scale(self, v):
        return self.scale * v

    def create_point(self, p, label):
        return self.canvas.create_text(
            *self.graph_coords(p), text=label, state="hidden"
        )

    def create_line(self, p1, p2):
        return self.canvas.create_line(
            *self.graph_coords(p1), *self.graph_coords(p2), state="hidden"
        )

    def create_circle(self, p, r, outline="grey"):
        x, y = self.graph_coords(p)
        r = self.graph_scale(r)
        return self.canvas.create_oval(
            x - r, y - r, x + r, y + r, outline=outline, dash=(5, 3), state="hidden"
        )

    def plot_point(self, id, p):
        self.canvas.coords(id, *self.graph_coords(p))

    def plot_line(self, id, p1, p2):
        self.canvas.coords(id, *self.graph_coords(p1), *self.graph_coords(p2))

    def plot_circle(self, id, p, r, color="grey"):
        x, y = self.graph_coords(p)
        r = self.graph_scale(r)
        self.canvas.coords(id, x - r, y - r, x + r, y + r)
        self.canvas.itemconfig(id, outline=color)

    def set_color(self, id, color):
        self.canvas.itemconfig(id, fill=color)

    def create_label(self, p, text, color=POINT_LABEL_COLOR, size=LABEL_TEXT_SIZE):
        (x, y) = p
        x = x + self.origin_x
        y = CANVAS_HEIGHT - y - self.origin_y
        return self.canvas.create_text(x, y, text=text, fill=color, font=(FONT, size))

    def set_label(self, id, label):
        self.canvas.itemconfig(id, text=label)

    def move_label(self, id, p):
        (x, y) = p
        x = x + self.origin_x
        y = CANVAS_HEIGHT - y - self.origin_y
        self.canvas.coords(id, x, y)

    def hide(self, id):
        self.canvas.itemconfig(id, state="hidden")

    def show(self, id):
        self.canvas.itemconfig(id, state="normal")
