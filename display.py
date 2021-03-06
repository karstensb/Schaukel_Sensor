import asyncio
import math
import tkinter as tk

import server

window = None
canvas = None
arcs = []
line = None
circle = None
value_field = None

circle_center_x = None
circle_center_y = None
circle_radius = None
swing_radius = None

angle_max = 91
angle_min = 91
prev_angle = 91

colors = [0xFF0000, 0xFF0500, 0xFF1100, 0xFF1600, 0xFF2200, 0xFF2700, 0xFF3300, 0xFF3800, 0xFF4400,
          0xFF4900, 0xFF5500, 0xFF5A00, 0xFF6600, 0xFF6B00, 0xFF7700, 0xFF7C00, 0xFF8800, 0xFF8D00,
          0xFF9900, 0xFF9E00, 0xFFAA00, 0xFFAF00, 0xFFBB00, 0xFFC800, 0xFFCC00, 0xFFD900, 0xFFDD00,
          0xFFEA00, 0xFFEE00, 0xFFFB00, 0xFFFF00, 0xFBFF00, 0xEEFF00, 0xEAFF00, 0xDDFF00, 0xD9FF00,
          0xCCFF00, 0xC8FF00, 0xBBFF00, 0xAFFF00, 0xAAFF00, 0x9EFF00 ,0x99FF00, 0x8DFF00, 0x88FF00,
          0x7CFF00, 0x77FF00, 0x6BFF00, 0x66FF00, 0x5AFF00, 0x55FF00, 0x49FF00, 0x44FF00, 0x38FF00,
          0x33FF00, 0x27FF00, 0x22FF00, 0x16FF00, 0x11FF00, 0x05FF00, 0x00FF00]

class Arc:
    def __init__(self, *args, **kwargs):
        self.arc = canvas.create_arc(args, kwargs)
        self.color = kwargs['outline']
        self.ticks = 0

    def highlight(self):
        canvas.itemconfig(self.arc, outline="red", width=600)
        self.ticks = 0

    def unhighlight(self):
        canvas.itemconfig(self.arc, outline=self.color, width=400)

    def set_max(self):
        canvas.itemconfig(self.arc, outline='#'+hex(colors[-61]).replace('0x','').rjust(6,'0'))
        self.ticks = 61

    def tick(self):
        if self.ticks > 0:
            self.ticks -= 1
            canvas.itemconfig(self.arc, outline='#'+hex(colors[-self.ticks]).replace('0x','').rjust(6,'0'))
            if self.ticks <= 0:
                self.unhighlight()

class Dummy:
    def __init__(self, *args, **kwargs):
        self.ticks = 0
    def highlight(self):
        pass
    def unhighlight(self):
        pass
    def set_max(self):
        pass
    def tick(self):
        pass

def quit(e):
    window.destroy()

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def show_values():
    global angle_max
    global angle_min
    global value_field
    global canvas

    canvas.itemconfig(value_field, text=f'Maximum angle back:  {angle_max-91}??\nMaximum angle front: {-1*(angle_min-91)}??\nCurrent angle: {prev_angle-91}??')

def swing_pos(angle):
    global prev_angle
    global angle_max
    global angle_min
    if angle > 46:
        angle = 46
    elif angle < -49:
        angle = -49
    angle = int(angle+91)
    if angle > prev_angle:
        while prev_angle <= angle:
            arcs[int(map(prev_angle, 139, 40, 0, 99))].set_max()
            prev_angle += 1
        if angle >= angle_max:
            arcs[int(map(angle_max+2, 139, 40, 0, 99))].unhighlight()
            angle_max = angle
            arcs[int(map(angle+2, 139, 40, 0, 99))].highlight()
    elif angle < prev_angle:
        while prev_angle >= angle:
            arcs[int(map(prev_angle, 139, 40, 0, 99))].set_max()
            prev_angle -= 1
        if angle <= angle_min:
            arcs[int(map(angle_min-2, 139, 40, 0, 99))].unhighlight()
            angle_min = angle
            arcs[int(map(angle-2, 139, 40, 0, 99))].highlight()

    angle = ((angle-91)*2+92) * math.pi/180
    canvas.coords(line,
        circle_center_x,
        circle_center_y,
        swing_radius * math.cos(angle) + circle_center_x,
        swing_radius * math.sin(angle) + circle_center_y)
    window.update()

def screen_init():
    global window
    window = tk.Tk()
    window.attributes('-fullscreen', True)
    window.bind('<Escape>', quit)

    global circle_center_x
    global circle_center_y
    global circle_radius
    global swing_radius
    circle_center_x = window.winfo_screenwidth() / 2
    circle_center_y = window.winfo_screenheight() / 4
    circle_radius = 10
    swing_radius = window.winfo_screenheight() / 2

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

    for i in range(100):
        if i == 94:
            arcs.append(Dummy())
            continue
        arc = Arc(
            circle_center_x-swing_radius,
            circle_center_y-swing_radius,
            circle_center_x+swing_radius,
            circle_center_y+swing_radius,
            width=400,
            outline='#00FF00',
            style='arc',
            start=170+i*2,
            extent=3)
        arcs.append(arc)

    global value_field
    value_field = canvas.create_text(220, 70, justify='left', font=('Helvetica','24','bold'))

    global line
    line = canvas.create_line(circle_center_x, circle_center_y, circle_center_x, circle_center_y+swing_radius, fill = 'black', width=10)

def update(angle):
    swing_pos(angle)
    show_values()
    for arc in arcs:
        arc.tick()

def reset():
    global angle_max
    global angle_min
    global prev_angle
    angle_max = 91
    angle_min = 91
    prev_angle = 91

    for arc in arcs:
        arc.ticks = 0
        arc.unhighlight()

async def main():
    server.start()
    while True:
        reset()
        async for angle in server.receive():
            if angle == 'RESET':
                break
            update(angle)
            print(angle) # l??uft deutlich besser so, problem liegt in server.receive()

if __name__ == '__main__':
    screen_init()
    while True:
        try:
            asyncio.run(main())
        except TimeoutError:
            print("Arduino disconnected! Restarting...")
