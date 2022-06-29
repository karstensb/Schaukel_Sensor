import socket
import asyncio

HOST = "0.0.0.0"
PORT = 8080

s = None
conn = None
addr = None

def start():
    global conn, addr, s 
    print("Starting server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    s.settimeout(30)
    print("Waiting for connection...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")
    conn.settimeout(5)

async def get_data():
    bytes = conn.recv(1024)
    while ';' not in str(bytes):
        bytes += conn.recv(1024) 
    if 'R' in str(bytes):
        return 'RESET'
    data = str(bytes).replace('b', '').replace("'", "").split(';')[1:-2]
    return data

async def receive():
    task = asyncio.create_task(get_data())
    while True:
        data = await task
        task = asyncio.create_task(get_data())
        if data == 'RESET':
            yield 'RESET'
        try:
            yield float(data[0])
        except IndexError:
            pass
        i = 0
        x = 2
        while not task.done() and i <= x:
            try:
                yield float(data[(len(data)-1)//x*i])
            except IndexError:
                pass
            finally:
                i += 1