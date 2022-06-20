import socket

HOST = "0.0.0.0"
PORT = 8080

s = None
conn =None
addr = None


def start_server():
    global conn, addr, s 
    print("Starting server...")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("Waiting for connection...")
    conn, addr = s.accept()
    print(f"Connected by {addr}")

async def receive():
    while True:
        data = conn.recv(1024)
        if ';' not in str(data):
            data += conn.recv(1024)
        try:
            angle = float(str(data).replace('b', '').replace("'", "").split(';')[0])
        except ValueError:
            continue
        yield angle
        # if '/' not in str(data):
        #     data += conn.recv(1024)
        # vals = str(data).replace('b', '').replace("'", "").split('/')[0]
        # try:
        #     gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = (float(x) for x in vals.split(';'))
        # except ValueError:
        #     continue
        # yield gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z