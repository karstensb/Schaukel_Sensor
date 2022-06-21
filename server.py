import socket

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

async def receive():
    while True:
        bytes = conn.recv(1024)
        while ';' not in str(bytes):
            bytes += conn.recv(1024)
        data = str(bytes).replace('b', '').replace("'", "").split(';')[1:-2]

        angle = float(data[0])
        yield angle