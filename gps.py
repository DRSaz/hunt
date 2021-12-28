import sys
import serial
import time
import math
from threading import Thread

GNGGA = [
    "$GNGGA",
    "Time",
    "LAT",
    "NorS",
    "LONG",
    "EorW",
    "Quality",
    "Sats",
    "Dilution",
    "Altitude",
    "Units_Altitude" "Geoidal",
    "Units_Geoidal",
    "Age",
    "ID",
    "Checksum",
]

GNGLL = ["$GNGLL", "LAT", "NorS", "LONG", "EorW", "Time", "Status"]
GPS_STATUS = ["Searching", "GPS", "DGPS"]


class GPS:
    def __init__(self, callback) -> None:
        self.callback = callback
        self.fix = 0
        self.lat = ""
        self.long = ""
        self.nors = ""
        self.eorw = ""
        self.serial = serial.Serial("/dev/ttyS0", baudrate=9600)
        input_task = Thread(target=self.process_input)
        input_task.daemon = True
        input_task.start()

    def get_location(self):
        lat = 0
        long = 0
        if self.lat != "" and self.nors != "" and self.long != "" and self.eorw != "":
            lat = self.dms_to_degrees(self.lat)
            if self.nors == "S":
                lat = -lat
            long = self.dms_to_degrees(self.long)
            if self.eorw == "W":
                long = -long
        return (GPS_STATUS[self.fix], lat, long)

    def dms_to_degrees(self, dms):
        parse = dms.split(".")
        d = int(parse[0][:-2])
        m = int(parse[0][-2:])
        s = int(parse[1])
        return float(d) + float(m) / 60 + float(s) / (60 * 60)

    def degrees_to_radians(self, deg):
        return deg * math.pi / 180

    def process_input(self):
        while True:
            line = str(self.serial.readline())
            line = line.lstrip("b'")
            parsed_line = line.split(",")
            if parsed_line[0] == GNGGA[0]:
                self.fix = int(parsed_line[GNGGA.index("Quality")])
                self.altitude = parsed_line[GNGGA.index("Altitude")]
                self.lat = parsed_line[GNGGA.index("LAT")]
                self.nors = parsed_line[GNGGA.index("NorS")]
                self.long = parsed_line[GNGGA.index("LONG")]
                self.eorw = parsed_line[GNGGA.index("EorW")]
                self.callback()
            elif parsed_line[0] == GNGLL[0]:
                self.lat = parsed_line[GNGLL.index("LAT")]
                self.nors = parsed_line[GNGLL.index("NorS")]
                self.long = parsed_line[GNGLL.index("LONG")]
                self.eorw = parsed_line[GNGLL.index("EorW")]
                self.status = parsed_line[GNGLL.index("Status")]
                self.callback()
