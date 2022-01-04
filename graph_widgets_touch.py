from config import *


class Graph_Widget:
    def __init__(self, graph, point, label, callback) -> None:
        self.graph = graph
        self.callback = callback
        self.color = DEFOCUS_COLOR
        self.label = self.graph.canvas.create_text(
            self.graph.canvas_coords(point),
            text=label,
            font=(FONT, GRAPH_WIDGET_TEXT_SIZE),
            fill=self.color,
        )
        self.set_touch_point(point)

    def set_touch_point(self, point):
        (x, y) = self.graph.canvas_coords(point)
        self.touch_box_x_min = x - TOUCH_BOX_SIZE / 2
        self.touch_box_x_max = x + TOUCH_BOX_SIZE / 2
        self.touch_box_y_min = y - TOUCH_BOX_SIZE / 2
        self.touch_box_y_max = y + TOUCH_BOX_SIZE / 2


class Point_Widget(Graph_Widget):
    def __init__(self, graph, point, label, callback) -> None:
        (x, y) = graph.canvas_coords(point)
        self.circle = graph.canvas.create_oval(
            x - MARKER_RADIUS,
            y - MARKER_RADIUS,
            x + MARKER_RADIUS,
            y + MARKER_RADIUS,
            fill=MAIN_BG,
            outline=DEFOCUS_COLOR,
        )
        super().__init__(graph, point, label, callback)

    def update(self, point):
        (x, y) = self.graph.canvas_coords(point)
        self.graph.canvas.coords(self.label, x, y)
        self.graph.canvas.itemconfig(self.label, fill=self.color)
        self.graph.canvas.coords(
            self.circle,
            x - MARKER_RADIUS,
            y - MARKER_RADIUS,
            x + MARKER_RADIUS,
            y + MARKER_RADIUS,
        )
        self.graph.canvas.itemconfig(self.circle, outline=self.color)
        self.set_touch_point(point)


class Line_Widget(Graph_Widget):
    def __init__(self, graph, p1, p2, callback) -> None:
        self.graph = graph
        self.line = self.graph.canvas.create_line(
            *self.graph.canvas_coords(p1),
            *self.graph.canvas_coords(p2),
            fill=INVALID_LINE_COLOR
        )
        super().__init__(graph, self.mid_point(p1, p2), "", callback)

    def mid_point(self, p1, p2):
        (x1, y1) = p1
        (x2, y2) = p2
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2
        return (x, y)

    def update(self, p1, p2, color):
        self.graph.canvas.coords(
            self.line, *self.graph.canvas_coords(p1), *self.graph.canvas_coords(p2)
        )
        self.graph.canvas.itemconfig(self.line, fill=color)
        self.graph.canvas.itemconfig(self.label, fill=self.color)
        self.set_touch_point(self.mid_point(p1, p2))


class Text_Widget(Graph_Widget):
    def __init__(self, graph, point, text, callback) -> None:
        super().__init__(graph, point, text, callback)

    def update(self, point, text):
        self.graph.canvas.coords(self.label, self.graph.canvas_coords(point))
        self.graph.canvas.itemconfig(self.label, text=text)
        self.set_touch_point(point)


class Graph:
    def __init__(self, canvas, x0, y0, scale) -> None:
        self.canvas = canvas
        self.origin_x = x0
        self.origin_y = y0
        self.scale = scale
        self.widgets = {}
        self.canvas.bind("<Button-1>", self.process_canvas_touch)

    def create_point(self, label, point, callback):
        self.widgets[label] = Point_Widget(self, point, label, callback)

    def update_point(self, label, point):
        self.widgets[label].update(point)

    def create_line(self, label, p1, p2, callback):
        self.widgets[label] = Line_Widget(self, p1, p2, callback)

    def update_line(self, label, p1, p2):
        self.widgets[label].update(p1, p2)

    def create_text(self, label, p1, text, callback):
        self.widgets[label] = Text_Widget(self, p1, text, callback)

    def update_text(self, label, point, text):
        self.widgets[label].update(point, text)

    def set_scale(self, scale):
        self.scale = scale

    def canvas_coords(self, p):
        (x, y) = p
        x = x * self.scale + self.origin_x
        y = CANVAS_HEIGHT - (y * self.scale) - self.origin_y
        return (x, y)

    def process_canvas_touch(self, event):
        for w in self.widgets:
            if (
                self.widgets[w].touch_box_x_min
                <= event.x
                <= self.widgets[w].touch_box_x_max
            ) and (
                self.widgets[w].touch_box_y_min
                <= event.y
                <= self.widgets[w].touch_box_y_max
            ):
                self.widgets[w].callback()
