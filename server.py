import socket
import asyncio
from webbrowser import get

HOST = "0.0.0.0"
PORT = 8080

s : socket.socket = None
conn : socket.socket = None
addr = None


def start():
    global conn, addr, s 
    print("Starting server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("Waiting for connection...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")

def stop():
    s.close()

async def get_data():
    bytes = conn.recv(1024)
    while ';' not in str(bytes):
        bytes += conn.recv(1024)
    data = str(bytes).replace('b', '').replace("'", "").split(';')[1:-2]
    return data

async def receive():
    task = asyncio.create_task(get_data())
    while True:
        data = await task
        temp = asyncio.create_task(get_data())
        angle = float(data[0])
        yield angle
        try:
            angle = float(data[len(data)//3])
            yield angle
        except IndexError as e:
            pass
        try:
            angle = float(data[len(data)//3*2])
            yield angle
        except IndexError as e:
            pass
        angle = float(data[-1])
        yield angle
        task = temp