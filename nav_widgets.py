from config import *
from info_widgets import *
from graph_widgets import *
from compass_widgets import *
from helpers import *


class Navigation_Widgets:
    def __init__(self, ws):
        self.canvas = tk.Canvas(
            ws, height=CANVAS_HEIGHT, width=CANVAS_WIDTH, bg=MAIN_BG, bd=3, relief=FRAME
        )
        self.g = Graph(self.canvas, GRAPH_CENTER_X, GRAPH_CENTER_Y, 1)
        self.c = Compass(self.canvas, COMPASS_CENTER_X, COMPASS_CENTER_Y, 1)
        self.points = {
            "M": (0, -SCALE_REFERENCE / 2),
            "W": (0, -SCALE_REFERENCE / 2),
            "P": (0, SCALE_REFERENCE / 2),
            "T": (0, SCALE_REFERENCE / 2),
            "C": (0, 0),
        }
        self.labels = {
            "MP_label": (-SCALE_LABEL_OFFSET, 0),
            "WT_label": (-SCALE_LABEL_OFFSET, 0),
            "Info_Line": (0, -GRAPH_INFO_OFFSET),
        }

        self.lines = {
            "MP": 0,
            "MC": 0,
            "PC": 0,
            "WT": 0,
        }
        self.circles = ("MC_circle", "PC_circle")

        self.modes = {
            "WT_mode": {
                "scale": 1.0,
                "fields": ["WT"],
                "view": ["WT", "W", "T", "WT_label"],
                "states": {
                    "Data_Entry": "",
                    "Ready": "Press to MARK",
                    "Tracking": "Tracking....",
                },
                "state": "Data_Entry",
            },
            "MPC_mode": {
                "scale": 1.0,
                "fields": ["MP", "MC", "PC"],
                "view": [
                    "MP",
                    "MC",
                    "PC",
                    "C",
                    "M",
                    "P",
                    "MP_label",
                    "MC_circle",
                    "PC_circle",
                ],
                "states": {
                    "Data_Entry": "",
                    "Side_Entry": "Select SIDE",
                    "Ready": "Press to MARK",
                    "Tracking": "Tracking....",
                },
                "state": "Data_Entry",
            },
        }

        self.all_fields = (
            self.modes["WT_mode"]["fields"] + self.modes["MPC_mode"]["fields"]
        )

        self.fields = {}
        self.objects = {}
        self.objects_visible = {}
        for l in self.lines:
            p0, p1 = tuple(l)
            self.objects[l] = self.g.create_line(self.points[p0], self.points[p1])
            self.objects_visible[l] = False
            self.g.set_color(self.objects[l], DEFAULT_LINE_COLOR)
            self.fields[l] = Number_Entry_Widget(
                ws, l, "yd", SELECTABLE_COLOR, INFO_WIDTH
            )
            self.fields[l].widget.config(text=UNSPECIFIED)
        for p in self.points:
            self.objects[p] = self.g.create_point(self.points[p], p)
            self.objects_visible[p] = False
        for c in self.circles:
            p = c[0]
            self.objects[c] = self.g.create_circle(self.points[p], 0)
            self.objects_visible[c] = False
        for l in self.labels:
            self.objects[l] = self.g.create_label(self.labels[l], UNSPECIFIED)
            self.objects_visible[p] = False

        for o in ["MP", "WT", "M", "P", "W", "T", "MP_label", "WT_label"]:
            self.objects_visible[o] = True

        self.active_fields = self.all_fields
        self.focus_field = "MP"
        self.select_field(self.focus_field, "current")

        self.input = Input_Buffer(ws, self.process_input_value, self.dump)

    def set_graph_view(self):
        if self.focus_field == "WT":
            self.set_mode("WT_mode")
            for o in self.modes["MPC_mode"]["view"]:
                self.g.hide(self.objects[o])
            for o in self.modes["WT_mode"]["view"]:
                if self.objects_visible[o]:
                    self.g.show(self.objects[o])
        else:
            self.set_mode("MPC_mode")
            for o in self.modes["WT_mode"]["view"]:
                self.g.hide(self.objects[o])
            for o in self.modes["MPC_mode"]["view"]:
                if self.objects_visible[o]:
                    self.g.show(self.objects[o])

    def select_field(self, field, direction):
        self.fields[self.focus_field].unhighlight()
        self.focus_field = select_item(field, self.active_fields, direction)
        self.fields[self.focus_field].highlight()
        self.set_graph_view()

    def process_encoder_move_event(self,value,direction):
        if direction == "L":
            if self.modes[self.mode]["state"] == "Side_Entry":
                self.toggle_side()
            else:
                self.active_fields = self.all_fields
                self.select_field(self.focus_field, "next")
        else:
            if self.modes[self.mode]["state"] == "Side_Entry":
                self.toggle_side()
            else:
                self.active_fields = self.all_fields
                self.select_field(self.focus_field, "previous")

    def process_button_event(self,event):
        if self.modes[self.mode]["state"] == "Side_Entry":
            self.clear_circles()
            self.modes[self.mode]["state"] = "Ready"
            self.update_info_line()
        elif self.modes[self.mode]["state"] == "Ready":
            self.modes[self.mode]["state"] = "Tracking"
            self.update_info_line()
        elif self.modes[self.mode]["state"] == "Tracking":
            self.reset_measurements()
            self.modes[self.mode]["state"] = "Data_Entry"
            self.update_info_line()

    def update_info_line(self):
        info_line = self.modes[self.mode]["states"][self.modes[self.mode]["state"]]
        self.g.set_label(self.objects["Info_Line"], info_line)

    def reset_measurements(self):
        for l in self.modes[self.mode]["fields"]:
            self.lines[l] = 0
            self.fields[l].widget.config(text=UNSPECIFIED)
            self.g.set_color(self.objects[l], DEFAULT_LINE_COLOR)
        for o in self.modes[self.mode]["view"]:
            self.objects_visible[o] = False
            self.g.hide(self.objects[o])
        if self.mode == "MPC_mode":
            self.g.set_label(self.objects["MP_label"], UNSPECIFIED)
            self.g.set_color(self.objects["MP_label"], DEFAULT_LINE_COLOR)
            self.g.show(self.objects["MP"])
            self.g.show(self.objects["M"])
            self.g.show(self.objects["P"])
            self.g.show(self.objects["MP_label"])
            self.objects_visible["MP"] = True
            self.objects_visible["M"] = True
            self.objects_visible["P"] = True
            self.objects_visible["MP_label"] = True
        else:
            self.g.set_label(self.objects["WT_label"], UNSPECIFIED)
            self.g.set_color(self.objects["WT_label"], DEFAULT_LINE_COLOR)
            self.g.show(self.objects["WT"])
            self.g.show(self.objects["W"])
            self.g.show(self.objects["T"])
            self.g.show(self.objects["WT_label"])
            self.objects_visible["WT"] = True
            self.objects_visible["W"] = True
            self.objects_visible["T"] = True
            self.objects_visible["WT_label"] = True
        self.select_field(self.modes[self.mode]["fields"][0], "current")

    def set_mode(self, mode):
        self.mode = mode
        self.g.set_scale(self.modes[self.mode]["scale"])
        self.active_fields = self.modes[self.mode]["fields"]
        info_line = self.modes[self.mode]["states"][self.modes[self.mode]["state"]]
        self.g.set_label(self.objects["Info_Line"], info_line)

    def process_input_value(self, value):
        if self.modes[self.mode]["state"] == "Data_Entry":
            if self.valid_input(value):
                value_yds = to_yds(value)
                self.fields[self.focus_field].set_value(str(int(value_yds)))
                self.lines[self.focus_field] = value_yds
                if self.focus_field == "WT":
                    self.update_scale_line(value_yds, "WT_label")
                    self.g.set_color(self.objects["WT"], INITIALIZED_LINE_COLOR)
                    self.g.set_color(self.objects["WT_label"], INITIALIZED_LINE_COLOR)
                    self.modes[self.mode]["state"] = "Ready"
                    self.set_graph_view()
                else:
                    if self.focus_field == "MP":
                        self.update_scale_line(value_yds, "MP_label")
                    self.display_status()
                    if self.solvability_check():
                        self.modes[self.mode]["state"] = "Side_Entry"
                        self.fields[self.focus_field].unhighlight()
                        self.display_solution()
                    else:
                        self.select_field(self.focus_field, "next")

    def valid_input(self, input):
        try:
            test = float(input)
            return True
        except:
            print("invalid input")
            return False

    def solvability_check(self):
        mp = self.lines["MP"]
        mc = self.lines["MC"]
        pc = self.lines["PC"]
        if mp == 0 or mc == 0 or pc == 0:
            return False  # one or more line lengths not defined
        elif pc >= mc:
            return False  # MP-MC angle greater than 45 degrees are problematic
        elif mp > mc and mp > mc + pc:
            return False  # cannot make a triangle out of given line lengths
        elif mc > mp and mc > mp + pc:
            return False  # cannot make a triangle out of given line lengths
        else:
            return True

    def display_status(self):
        mp = self.lines["MP"]
        mc = self.lines["MC"]
        pc = self.lines["PC"]
        if mp > 0:
            self.g.set_color(self.objects["MP"], INITIALIZED_LINE_COLOR)
            self.g.set_color(self.objects["MP_label"], INITIALIZED_LINE_COLOR)
            self.g.plot_line(self.objects["MP"], self.points["M"], self.points["P"])
            self.g.plot_point(self.objects["M"], self.points["M"])
            self.g.plot_point(self.objects["P"], self.points["P"])
        if mc > 0:
            self.g.plot_circle(self.objects["MC_circle"], self.points["M"], mc)
            self.objects_visible["MC_circle"] = True
        if pc > 0:
            self.g.plot_circle(self.objects["PC_circle"], self.points["P"], pc)
            self.objects_visible["PC_circle"] = True
        self.refresh_view()

    def display_solution(self):
        a = self.lines["MP"]
        b = self.lines["MC"]
        c = self.lines["PC"]
        theta = math.acos((a ** 2 + b ** 2 - c ** 2) / (2 * a * b))
        x = b * math.sin(theta)
        y = b * math.cos(theta) + self.points["M"][1]  # M.y
        self.points["C"] = (x, y)
        self.g.set_color(self.objects["MP"], INITIALIZED_LINE_COLOR)
        self.g.set_color(self.objects["MC"], INITIALIZED_LINE_COLOR)
        self.g.set_color(self.objects["PC"], INITIALIZED_LINE_COLOR)
        self.g.plot_line(self.objects["MC"], self.points["M"], self.points["C"])
        self.g.plot_line(self.objects["PC"], self.points["P"], self.points["C"])
        self.g.plot_point(self.objects["C"], self.points["C"])
        info_line = self.modes[self.mode]["states"][self.modes[self.mode]["state"]]
        self.g.set_label(self.objects["Info_Line"], info_line)
        for o in self.modes["MPC_mode"]["view"]:
            self.objects_visible[o] = True
        self.refresh_view()

    def clear_circles(self):
        for o in self.circles:
            self.objects_visible[o] = False
            self.g.hide(self.objects[o])
        self.refresh_view()

    def update_scale_line(self, value_yds, label):
        p0, p1 = tuple(self.focus_field)
        self.points[p0] = (0, -value_yds / 2)
        self.points[p1] = (0, value_yds / 2)
        self.g.set_label(self.objects[label], str(int(value_yds)))
        self.modes[self.mode]["scale"] = SCALE_REFERENCE / value_yds
        self.g.set_scale(self.modes[self.mode]["scale"])

    def refresh_view(self):
        self.g.set_scale(self.modes[self.mode]["scale"])
        for o in self.modes[self.mode]["view"]:
            if self.objects_visible[o]:
                self.g.show(self.objects[o])

    def toggle_side(self):
        if self.mode == "MPC_mode":
            x, y = self.points["C"]
            self.points["C"] = -1 * x, y
            x, y = self.labels["MP_label"]
            self.labels["MP_label"] = -1 * x, y
            self.g.plot_line(self.objects["PC"], self.points["P"], self.points["C"])
            self.g.plot_line(self.objects["MC"], self.points["M"], self.points["C"])
            self.g.plot_point(self.objects["C"], self.points["C"])
            self.g.move_label(self.objects["MP_label"], self.labels["MP_label"])

    def dump(self):
        print(self.mode)
        print(self.points)
        print(self.modes)
        print(self.g.scale)
        print(self.active_fields)
        print(self.focus_field)
