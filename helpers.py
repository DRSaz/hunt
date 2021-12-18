import math


def select_item(current_item, the_list, direction):
    if direction == "previous":
        increment = -1
    elif direction == "next":
        increment = 1
    else:
        increment = 0
    new_index = the_list.index(current_item) + increment
    if new_index >= len(the_list):
        new_index = 0
    elif new_index < 0:
        new_index = len(the_list) - 1
    return the_list[new_index]


class Encoder_Toggle:
    def __init__(self, ws, encoders):
        self.toggle = 0
        self.encoders = encoders
        self.encoders[self.toggle].enable()
        ws.bind("<Up>", self.encoder_toggle)

    def encoder_toggle(self, event):
        self.encoders[self.toggle].disable()
        self.toggle += 1
        if self.toggle >= len(self.encoders):
            self.toggle = 0
        self.encoders[self.toggle].enable()


class Encoder:
    def __init__(self, ws, cw_action, ccw_action, button_action):
        self.cw_action = cw_action
        self.ccw_action = ccw_action
        self.buttun_action = button_action
        self.ws = ws

    def cw_event(self, event):
        self.cw_action()

    def ccw_event(self, event):
        self.ccw_action()

    def button_event(self, event):
        self.buttun_action()

    def enable(self):
        self.ws.bind("<Left>", self.ccw_event)
        self.ws.bind("<Right>", self.cw_event)
        self.ws.bind("<Down>", self.button_event)

    def disable(self):
        self.ws.unbind("<Left>")
        self.ws.unbind("<Right>")
        self.ws.unbind("<Down>")


def distance(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)


def to_yds(input):
    value = float(input)
    value = (value * 1760.0) / 2.0
    return value


class Input_Buffer:
    def __init__(self, ws, callback, callback2):
        self.callback = callback
        self.callback2 = callback2
        self.buffer = ""
        ws.bind("<Key>", self.process_key)

    def process_key(self, event):
        if event.keysym == "Return":
            self.callback(self.buffer)
            self.buffer = ""
        elif event.keysym == "slash":
            self.callback2()
        else:
            self.buffer = self.buffer + event.char
