import math
import time
import tkinter as tk

window = tk.Tk()

circle_center_x = window.winfo_screenwidth() / 2
circle_center_y = 0
circle_radius = 10

swing_radius = 1000

def quit(e):
    window.destroy()

def swing_pos(angle):
    angle = angle * math.pi/180
    canvas.coords(line,
        circle_center_x,
        circle_center_y,
        swing_radius*math.cos(angle) + circle_center_x,
        swing_radius*math.sin(angle) + circle_center_y)
        
    window.update()

window.attributes('-fullscreen', True)
window.bind('<Escape>', quit)

canvas = tk.Canvas(window)
canvas.configure(bg='blue')
canvas.pack(fill='both', expand=True)


circle = canvas.create_oval(
    circle_center_x-circle_radius,
    circle_center_y-circle_radius,
    circle_center_x+circle_radius,
    circle_center_y+circle_radius,
    fill='red')

line = canvas.create_line(circle_center_x, circle_center_y, 0, 0, fill = 'red')

arc = canvas.create_arc(
    circle_center_x-swing_radius,
    circle_center_y-swing_radius,
    circle_center_x+swing_radius,
    circle_center_y+swing_radius,
    width=50,
    style='arc',
    fill='green',
    start=180,
    extent=359)

# x=10
# for i in range(x):
#     color = '#'+hex(i*(16777215//x)).replace('0x', '').rjust(6,'0')
#     arc = canvas.create_arc(
#         circle_center_x-swing_radius,
#         circle_center_y-swing_radius,
#         circle_center_x+swing_radius,
#         circle_center_y+swing_radius,
#         width=100,
#         outline=color,
#         style='arc',
#         start=180+180/x*i,
#         extent=181+180/x*i)

inc = True
i = 0
while True:
    if i >= 180:
        inc = False
    elif i <= 0:
        inc= True
    i = i+1 if inc else i-1
    swing_pos(i)
    time.sleep(0.01)