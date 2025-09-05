


import socket
import os
import struct
from ctypes import *

# Host to listen on
host = "192.168.1.71"

# Our IP header
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
    
    def __new__(cls, socket_buffer):
        return cls.from_buffer_copy(socket_buffer)
    
    def __init__(self, socket_buffer=None):
        # Map protocol constants to their names
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}
        
        # Human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("<L", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L", self.dst))
        
        # Human readable protocol
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

# Our ICMP header
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

# Create a raw socket and bind it to the public interface
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 0))

# We want the IP headers included in the capture
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# If we're on Windows, we need to send an IOCTL to set up promiscuous mode
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:
        # Read in a packet
        raw_buffer = sniffer.recvfrom(65565)[0]
        
        # Create an IP header from the first 20 bytes of the buffer
        ip_header = IP(raw_buffer[0:20])
        
        # If it's ICMP, we want it
        if ip_header.protocol == "ICMP":
            print(f"Protocol: {ip_header.protocol} {ip_header.src_address} -> {ip_header.dst_address}")
            
            # Calculate where our ICMP packet starts
            offset = ip_header.ihl * 4
            
            if len(raw_buffer) >= offset + 8:  # ICMP header is typically 8 bytes
                icmp_header = ICMP.from_buffer_copy(raw_buffer[offset:offset+8])
                print(f"ICMP -> Type: {icmp_header.type} Code: {icmp_header.code}")


# Handle CTRL-C
except KeyboardInterrupt:
    # If we're on Windows, turn off promiscuous mode
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    print("\nSniffer stopped.")