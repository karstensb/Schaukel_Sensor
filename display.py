import math
import tkinter as tk

def quit(e):
    window.destroy()

window = tk.Tk()
window.attributes('-fullscreen', True)
window.bind('<Escape>', quit)

canvas = tk.Canvas(window)
canvas.configure(bg='blue')
canvas.pack(fill='both', expand=True)

rect = canvas.create_rectangle(50, 50, 150, 200, fill='red')
while True:
    
    window.update()