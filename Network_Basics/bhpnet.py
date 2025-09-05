

import socket
import threading
import sys
import subprocess
import getopt


listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0




def usage():
    print("BHP Net Tool")
    print()
    print("Usage:python bhpnet.py -t target_host -p port")
    print("-l --listen                - listen on [host]:[port ]")
    print("-e --execute=file_to_run   - execute the given file")
    print("-c --command               - initialize a command shell")
    print("-u --upload=destination    - upon receiving upload a file")
    print()

    sys.exit(0)





def client_sender(buffer):
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    try:
        client.connect((target,port))

        if len(buffer):
            client.send(buffer.encode())


        while True:
            recv_len = 1
            response = ""


            while recv_len:
                data = client.recv(4096).decode()
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break


            print(response,end=' ')

            buffer = input('')
            buffer += "\n"
            client.send(buffer.encode())

    except Exception as e:
        print("[*] Exception! Exiting. %s" % e)
        client.close()



def server_loop():
    global target

    if not len(target):
        target = "0.0.0.0"
    
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)

    print(f"[*] Listening on {target}:{port}...")

    while True:
        client_socket,addr = server.accept()
        client_thread = threading.Thread(target=client_handler,args=(client_socket,))
        client_thread.start()


def run_command(command):
    command = command.strip()

    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT,shell=True)
    except:
        output = b"Failed to execute command.\n"
    return output



def client_handler(client_socket):
    global upload
    global execute
    global command


    if len(upload_destination):
        file_buffer = b""

        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data
        

        try:
            with open(upload_destination,"wb") as f:
                f.write(file_buffer)
            client_socket.send(f"Successfully saved file to {upload_destination}\n".encode())
        except:
            client_socket.send(f"Faile to save file to {upload_destination}\n".encode())

    
    if len(execute):
        output = run_command(execute)
        client_socket.send(output)

    
    if command:
        while True:
            client_socket.send(b"<BHP:#> ")
            cmd_buffer = b""
            while b'\n' not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            response = run_command(cmd_buffer.decode())
            client_socket.send(response)





def main():
    global listen
    global target
    global port
    global execute
    global command
    global upload_destination
    

    if not len(sys.argv[1:]):
        usage()

    try:
        opts,args = getopt.getopt(sys.argv[1:],"hle:t:p:cu",["help","listen","execute=","target=","port=","command","upload="])

    except getopt.GetoptError as err:
        print(str(err))
        usage()
    

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-l","--listen"):
            listen = True
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c","--command"):
            command = True
        elif o in ("-u","--upload"):
            upload_destination = a
        elif o in ("-t","--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"
    

    if not listen and len(target) and port > 0:
        buffer = sys.stdin.read()
        client_sender(buffer)
        
    if listen:
        server_loop()

if __name__ == "__main__":
    main()