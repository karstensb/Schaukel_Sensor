import asyncio
import math
import tkinter as tk

import server

swing_height_real = 1
swing_radius_real = 2

window = None
canvas = None
arcs = []
line = None
circle = None

circle_center_x = None
circle_center_y = 500
circle_radius = 10

angle_max = 91
angle_min = 91
value_field = None

swing_radius = 500

colors = [0xFF0000, 0xFF1100, 0xFF2200, 0xFF3300, 0xFF4400, 0xFF5500, 0xFF6600, 0xFF7700, 0xFF8800, 0xFF9900, 0xFFAA00, 0xFFBB00, 0xFFCC00, 0xFFDD00, 0xFFEE00, 0xFFFF00, 0xEEFF00, 0xDDFF00, 0xCCFF00, 0xBBFF00, 0xAAFF00, 0x99FF00, 0x88FF00, 0x77FF00, 0x66FF00, 0x55FF00, 0x44FF00, 0x33FF00, 0x22FF00, 0x11FF00, 0x00FF00]
class Arc:
    def __init__(self, *args, **kwargs):
        self.arc = canvas.create_arc(args, kwargs)
        self.color = kwargs['outline']
        self.ticks = 0

    def highlight(self):
        canvas.itemconfig(self.arc, outline="red", width=200)
        self.ticks = 0

    def unhighlight(self):
        canvas.itemconfig(self.arc, outline=self.color, width=100)

    def set_max(self):
        canvas.itemconfig(self.arc, outline='#'+hex(colors[-31]).replace('0x','').rjust(6,'0'))
        self.ticks = 90

    def tick(self):
        if self.ticks > 0:
            self.ticks -= 1
            canvas.itemconfig(self.arc, outline='#'+hex(colors[-self.ticks//3-1]).replace('0x','').rjust(6,'0'))
            if self.ticks <= 0:
                self.unhighlight()

def quit(e):
    window.destroy()

def map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

def show_values():
    global angle_max
    global angle_min
    global value_field
    global swing_height_real
    global swing_radius_real
    global canvas

    canvas.itemconfig(value_field, text=f'Maximum angle:  {angle_max-91}\nMinimum angle: {-1*(angle_min-91)}')
    

prev_angle = 91
def swing_pos(angle):
    global prev_angle
    global angle_max
    global angle_min
    if angle > 138:
        angle = 138
    elif angle < -139:
        angle = -139
    angle = int(angle)+91
    if angle > prev_angle:
        while prev_angle < angle:
            arcs[int(map(prev_angle, 230, -50, 0, 280))].set_max()
            prev_angle += 1
        if angle >= angle_max:
            arcs[int(map(angle_max+1, 230, -50, 0, 280))].unhighlight()
            angle_max = angle
            arcs[int(map(angle+1, 230, -50, 0, 280))].highlight()
    elif angle < prev_angle:
        while prev_angle > angle:
            arcs[int(map(prev_angle, 230, -50, 0, 280))].set_max()
            prev_angle -= 1
        if angle <= angle_min:
            arcs[int(map(angle_min-1, 230, -50, 0, 280))].unhighlight()
            angle_min = angle
            arcs[int(map(angle-1, 230, -50, 0, 280))].highlight()

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

    x=280
    for i in range(x):
        arc = Arc(
            circle_center_x-swing_radius,
            circle_center_y-swing_radius,
            circle_center_x+swing_radius,
            circle_center_y+swing_radius,
            width=100,
            outline='#00FF00',
            style='arc',
            start=130+i,
            extent=2)
        arcs.append(arc)

    global value_field
    value_field = canvas.create_text(200, 50, justify='left', text='Maximum angle: \nMinimum angle: ', font=('Helvetica','24','bold'))

    global line
    line = canvas.create_line(circle_center_x, circle_center_y, circle_center_x, circle_center_y+swing_radius, fill = 'black', width=10)

def update(angle):
    swing_pos(angle)
    show_values()
    for i in range(len(arcs)):
        arcs[i].tick()

async def main():
    screen_init()
    server.start()
    async for angle in server.receive():
        print(angle) # läuft deutlich besser so, problem liegt in server.receive()
        update(angle)

if __name__ == '__main__':
    asyncio.run(main())
