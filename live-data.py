import socket

# Configure server address and port to match LabVIEW
HOST = '127.0.0.1'  # Localhost
PORT = 5005

print("Waiting for LabVIEW connection...")

# Open the network socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()

    with conn:
        print(f"Connected successfully to LabVIEW at {addr}")
        buffer = ""

        while True:
            # Receive incoming chunks of data (up to 1024 bytes)
            data = conn.recv(1024)
            if not data:
                print("LabVIEW closed the connection.")
                break

            # Decode bytes to text and handle line breaks
            buffer += data.decode('utf-8')
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                print(f"Received Data: {line}")
