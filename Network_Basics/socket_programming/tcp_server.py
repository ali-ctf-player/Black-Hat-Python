


import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 9999

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip,bind_port))

server.listen(5)

print("[*] Listening on %s:%d" % (bind_ip,bind_port))

client_socket ,addr = server.accept()
print(f"[*] Accepted connection from {addr[0]}:{addr[1]}")


def receive_message():
    
    while True:
        try:
            msg = client_socket.recv(1024).decode()
            if not msg:
                break
            print("[*] Received: %s" % msg)
        except:
            break
    

def send_message():
    
    while True:
        try:
            msg = input("")
            client_socket.send(msg.encode())
        except:
            break

recv_thread = threading.Thread(target=receive_message)
send_thread = threading.Thread(target=send_message)

recv_thread.start()
send_thread.start()