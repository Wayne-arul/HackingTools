import socket

# for i in range(1, 5):
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.connect(("192.168.29.226", 19+i))
#         msg = s.recv(2048).decode()
#         s.close()
#         print(msg)
#     except ConnectionRefusedError:
#         pass

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("192.168.29.226", 23))
msg = s.recv(2048)
s.close()
print(msg)
file = open('test.txt', 'wb')
a = file.write(msg)
b = open('test.txt', 'rb')
print(b.readlines())
