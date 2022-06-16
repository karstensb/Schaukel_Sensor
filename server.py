import socket

HOST = "0.0.0.0"
PORT = 8080

print("Starting server...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print("Waiting for connection...")
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if '/' not in str(data):
                data += conn.recv(1024)

            #TODO: wenn mehrere werte ankommen nicht nur die ersten verarbeiten
            vals = str(data).replace('b', '').replace("'", "").split('/')[0]
            try:
                gyro_x, gyro_y, gyro_z, accel_x, accel_y, accel_z = (float(x) for x in vals.split(';'))
            except ValueError: # wenn zu viele daten auf einaml ankommen
                continue
            #print(f"{gyro_x=}, {gyro_y=}, {gyro_z=}, {accel_x=}, {accel_y=}, {accel_z=}")
            print(f"{accel_x}, {accel_y}, {accel_z}")
            if not data:
                print("Client disconnected!")