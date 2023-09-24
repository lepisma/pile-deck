import sys
import time
from collections import namedtuple
import random
import os

from PIL import Image, ImageDraw, ImageFont

from dataclasses import dataclass
from displayhatmini import DisplayHATMini
from PIL import Image, ImageDraw


class Display:
    def __init__(self):
        self.width: int = DisplayHATMini.WIDTH
        self.height: int = DisplayHATMini.HEIGHT
        self.buffer = Image.new("RGB", (self.width, self.height))
        self.draw = ImageDraw.Draw(self.buffer)
        self.hat = DisplayHATMini(self.buffer)

display = Display()
display.hat.set_led(0.05, 0.05, 0.05)


Position = namedtuple('Position', 'x y')
Size = namedtuple('Size', 'w h')


def millis():
    return int(round(time.time() * 1000))


def text(draw, text, position, size, color):
    fnt = ImageFont.load_default()
    draw.text(position, text, font=fnt, fill=color)

time_last = millis()

display.hat.set_led(0, 0, 0)

color = (155, 0, 0)

def set_title(string, color):
    text(display.draw, string, (15, 15), 15, color)

def shutdown():
    os.system("sudo shutdown now")


if __name__ == "__main__":
    args = sys.argv[1:]

    while True:
        time_now = millis()
        time_delta = time_now - time_last

        if display.hat.read_button(display.hat.BUTTON_A):
            color = (random.randint(0, 254), random.randint(0, 254), random.randint(0, 254))
        if display.hat.read_button(display.hat.BUTTON_B):
            pass

        if display.hat.read_button(display.hat.BUTTON_X):
            set_title("shutting down ...", "yellow")
            time.sleep(2)
            shutdown()
        if display.hat.read_button(display.hat.BUTTON_Y):
            pass

        display.draw.rectangle((0, 0, display.width, display.height), color)
        display.draw.rectangle((5, 5, display.width-5, display.height-5), (0, 0, 0))

        set_title("pile-deck", color)

        display.hat.display()

        time.sleep(0.1)
        time_last = time_now
