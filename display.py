import asyncio
import math
import sys
import time
import random
import tkinter as tk

from server import receive, start_server

window = None
canvas = None
arcs = []
line = None
circle = None
fps_counter = None

circle_center_x = None
circle_center_y = 300
circle_radius = 10

swing_radius = 500

colors = [0x000000, 0x110000, 0x220000, 0x330000, 0x440000, 0x550000, 0x660000, 0x770000, 0x880000, 0x990000, 0xAA0000, 0xBB0000, 0xCC0000, 0xDD0000, 0xEE0000, 0xFF0000, 0xFF1100, 0xFF2200, 0xFF3300, 0xFF4400, 0xFF5500, 0xFF6600, 0xFF7700, 0xFF8800, 0xFF9900, 0xFFAA00, 0xFFBB00, 0xFFCC00, 0xFFDD00, 0xFFEE00, 0xFFFF00, 0xEEFF00, 0xDDFF00, 0xCCFF00, 0xBBFF00, 0xAAFF00, 0x99FF00, 0x88FF00, 0x77FF00, 0x66FF00, 0x55FF00, 0x44FF00, 0x33FF00, 0x22FF00, 0x11FF00, 0x00FF00, 0x00FF11, 0x00FF22, 0x00FF33, 0x00FF44, 0x00FF55, 0x00FF66, 0x00FF77, 0x00FF88, 0x00FF99, 0x00FFAA, 0x00FFBB, 0x00FFCC, 0x00FFDD, 0x00FFEE, 0x00FFFF, 0x00EEFF, 0x00DDFF, 0x00CCFF, 0x00BBFF, 0x00AAFF, 0x0099FF, 0x0088FF, 0x0077FF, 0x0066FF, 0x0055FF, 0x0044FF, 0x0033FF, 0x0022FF, 0x0011FF, 0x0000FF, 0x0000EE, 0x0000DD, 0x0000CC, 0x0000BB, 0x0000AA, 0x000099, 0x000088, 0x000077, 0x000066, 0x000055, 0x000044, 0x000033, 0x000022, 0x000011, 0x000000]
class Arc:
    def __init__(self, *args, **kwargs):
        self.arc = canvas.create_arc(args, kwargs)
        self.color = kwargs['outline']
        self.ticks = 0

    def highlight(self):
        canvas.itemconfig(self.arc, outline="#000000")
        self.ticks = 1800

    def tick(self):
        if self.ticks > 0:
            self.ticks -= 1
            canvas.itemconfig(self.arc, outline='#'+hex(colors[self.ticks//20]).replace('0x','').rjust(6,'0'))
            if self.ticks <= 1300:
                self.unhighlight()

    def unhighlight(self):
        canvas.itemconfig(self.arc, outline=self.color)

def quit(e):
    window.destroy()

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def swing_pos(angle):
    try:
        arcs[int(map(angle, 210, -30, 0, len(arcs)))].highlight()
    except IndexError:
        pass
    angle = angle * math.pi/180
    canvas.coords(line,
        circle_center_x,
        circle_center_y,
        swing_radius*math.cos(angle) + circle_center_x,
        swing_radius*math.sin(angle) + circle_center_y)
    window.update()

def screen_init():
    global window
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    window.bind('<Escape>', quit)

    global circle_center_x
    circle_center_x = window.winfo_screenwidth() / 2

    global canvas
    canvas = tk.Canvas(window)
    canvas.pack(fill='both', expand=True)

    global circle
    circle = canvas.create_oval(
        circle_center_x-circle_radius,
        circle_center_y-circle_radius,
        circle_center_x+circle_radius,
        circle_center_y+circle_radius,
        fill='red')

    x=100
    for i in range(x):
        arc = Arc(
            circle_center_x-swing_radius,
            circle_center_y-swing_radius,
            circle_center_x+swing_radius,
            circle_center_y+swing_radius,
            width=100,
            outline='green',
            style='arc',
            start=150+i*(240/x),
            extent=240/x+1)
        arcs.append(arc)

    global line
    line = canvas.create_line(circle_center_x, circle_center_y, 0, 0, fill = 'black', width=10)

def update(angle):
    swing_pos(angle)
    for i in range(len(arcs)):
        arcs[i].tick()

prev_angle = 0
async def main():
    screen_init()
    start_server()
    async for angle in receive():
        print(angle)
        update(angle)
    # async for gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z in receive():
    #     print(gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z)

if __name__ == '__main__':
    asyncio.run(main())