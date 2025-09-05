
import socket
import threading

target_host = "0.0.0.0"
target_port = 9999

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

client.connect((target_host,target_port))



def receive_message():
    while True:
        try:
            msg = client.recv(1024).decode()
            if not msg:
                break
            print(f"[*] Received: {msg}")
        except:
            break


def send_message():
    
    while True:
        try:
            msg = input("")
            client.send(msg.encode())
        except:
            break


recv_thread =  threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

recv_thread.start()
send_thread.start()
