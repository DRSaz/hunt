import math
import sys


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


def distance(p0, p1):
    x0, y0 = p0
    x1, y1 = p1
    return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2)
