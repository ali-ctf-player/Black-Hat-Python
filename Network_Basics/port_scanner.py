

import socket
import sys
from datetime import datetime



if len(sys.argv) == 2:
    target = socket.gethostbyname(sys.argv[1])

else:
    print("Invalid amounts of arguments")
    print("Usage: python3 port_scanner.py [host_ip]")


print("""
\033[1;36m
  _____           _    _____               _____                                  
 |  __ \         | |  |  __ \             / ____|                                 
 | |__) |__  _ __| |_ | |__) |__ _ ___   | (___   ___ __ _ _ __  _ __   ___ _ __ 
 |  ___/ _ \| '__| __||  ___/ _` / __|    \___ \ / __/ _` | '_ \| '_ \ / _ \ '__|
 | |  | (_) | |  | |_ | |  | (_| \__ \    ____) | (_| (_| | | | | | | |  __/ |   
 |_|   \___/|_|   \__||_|   \__,_|___/   |_____/ \___\__,_|_| |_|_| |_|\___|_|   
\033[0m                                                                          
\033[1;33m╔══════════════════════════════════════════════════════════╗
║ \033[1;33mPYTHON PORT SCANNER - FAST & ACCURATE PORT DETECTION \033[1;33m║
╚══════════════════════════════════════════════════════════╝\033[0m""")



print("\033[1;33m╔══════════════════════════════════════════════════════════╗\033[0m")
print(f"\033[1;33m║ \033[1;35mTIME: \033[1;32m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m")
print("\033[1;33m╚══════════════════════════════════════════════════════════╝\033[0m")



print("""\033[1;33m╔══════════════════════════════════════════════════════════╗\033[0m
\033[1;33m║ \033[1;34mSCANNING TARGET\033[0m""")
print(f"""\033[1;33m║   Target: \033[1;33m{target}\033[1;33m""")





try:

    open_ports = []

    for port in range(0,100):
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        socket.setdefaulttimeout(1)

        result = client.connect_ex((target,port))
        if result == 0:
            open_ports.append(port)
        
        client.close()

    print(f"\033[1;33m║   Ports:  \033[1;32m{[port for port in open_ports]}\033[0m")
    print("\033[1;33m╚══════════════════════════════════════════════════════════╝\033[0m")
except KeyboardInterrupt:
    print(f"""\033[1;34m║   \033[1;31m• Exiting\033[0m""")
except socket.gaierror:
    print(f"""\033[1;34m║   \033[1;31m• Hostname could not be resolved\033[0m""")
except socket.error as e:
    print(f"""\033[1;34m║   \033[1;31m• Could not connect to the host\033[0m""")

