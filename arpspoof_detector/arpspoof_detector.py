#!/usr/bin/env python3
import re
import subprocess
import optparse
from termcolor import colored
import scapy.all as scapy
from scapy.layers import http



#TODO filter
# TODO add layer and field for packet
# TODO search for keyword
# TODO run with sudo
def sniff(interface):
    scapy.sniff(iface=interface, store=False, prn=process_sniffed_packet)

def get_mac(ip):

    arp_request=scapy.ARP(pdst=ip)
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast=broadcast/arp_request
    try:
        answered_list=scapy.srp(arp_request_broadcast,timeout=1,verbose=False)[0]

        # print(scapy.srp(arp_request_broadcast,timeout=1,verbose=False))
        # print("---------------------------")
        # print(scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0])
    except PermissionError:
        print(colored("[-]","red")+"Can not run without sudo privileges\n")
    # get the mac from the first device in answered list aka the router

    return answered_list[0][1].hwsrc


def process_sniffed_packet(packet):
    if packet.haslayer(scapy.ARP) and packet[scapy.ARP].op == 2:
        try:
            real_mac=get_mac(packet[scapy.ARP].psrc)
            response_mac=packet[scapy.ARP].hwsrc
            if real_mac != response_mac:
                print("[+] You are under MITM attack")

        except IndexError:
            pass


def main():

    sniff("eth0")

if __name__=="__main__":

    main()
