import socket

for i in range(10, 30):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("192.168.29.226", i))
        print(f"port {i} is open")

    except:
        print(f"port {i} is closed")
