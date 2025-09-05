

import os
import socket
import struct
from ctypes import *
import threading
import time
from netaddr import IPAddress,IPNetwork



host = "192.168.100.14"
subnet = "192.168.100.0/24"
magic_message = "PYTHONFORBLACKHATS"

class IP(Structure):
    _fields_ = [
        ("ihl",             c_ubyte, 4),    # 4-bit header length
        ("version",         c_ubyte, 4),    # 4-bit version
        ("tos",             c_ubyte),       # 8-bit type of service
        ("len",             c_ushort),      # 16-bit total length
        ("id",              c_ushort),      # 16-bit identification
        ("offset",          c_ushort),      # 16-bit fragment offset
        ("ttl",             c_ubyte),       # 8-bit time to live
        ("protocol_num",    c_ubyte),       # 8-bit protocol number
        ("sum",             c_ushort),      # 16-bit checksum
        ("src",             c_uint),        # 32-bit source address
        ("dst",             c_uint)         # 32-bit destination address
    ]

    def __new__(cls,socket_buffer):
        return cls.from_buffer_copy(socket_buffer)
    

    def __init__(self,socket_buffer=None):  

        self.protocol_map = {1:"ICMP",6:"TCP",17:"UDP"} 


        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src)) 
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))


        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)   


class ICMP(Structure):
    _fields_ = [
        ("type",         c_ubyte),
        ("code",         c_ubyte),
        ("checksum",     c_ushort),
        ("unused",       c_ushort),
        ("next_hop_mtu", c_ushort)
    ]
    
    def __new__(cls, socket_buffer):
        return cls.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer = None):
        pass

def udp_sender(subnet,magic_message):
    time.sleep(5)

    sender = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    for ip in IPNetwork(subnet):

        try:
            sender.sendto(magic_message,(str(ip),65212))
        except:
       
            pass

t = threading.Thread(target=udp_sender,args=(subnet,magic_message))
t.start()


if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP


sniffer = socket.socket(socket.AF_INET,socket.SOCK_RAW,socket_protocol)

sniffer.bind((host,0))

sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)


if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_ON)

try:

    while True:

        raw_buffer = sniffer.recvfrom(65565)[0]

        ip_header = IP(raw_buffer[0:20])


        if ip_header.protocol == "ICMP":

            offset = ip_header.ihl * 4
            buf = raw_buffer[offset:offset + sizeof(ICMP)]
            icmp_header = ICMP(buf)


            if icmp_header.type == 3 and icmp_header.code == 3:
                IPAddress(ip_header.src_address) in IPNetwork(subnet)
                if raw_buffer[-len(magic_message):] == magic_message:
                    print(f"\n[***] Host up: {ip_header.src_address}\n")



except KeyboardInterrupt:

    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL,socket.RCVALL_OFF)
    
    print("\nSniffing stopped.")



        