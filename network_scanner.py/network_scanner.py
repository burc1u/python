#!/usr/bin/env python3

from termcolor import colored
import scapy.all as scapy
import optparse
# optparse is deprecated , use argparse instead

def scan(ip):
    #creating an ARP packet
    #pdst is the ip field in ARP
    arp_request=scapy.ARP(pdst=ip)
    #ethernet obj
    #dst is destination MAC
    broadcast=scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    #scapy.ls(scapy.Ether())

    #print(arp_request.summary())
    #to check what fields from ARP class can be modified
    #scapy.ls(scapy.ARP())

    # arp_request.show()
    # broadcast.show()

    #appending packets to create a package using / specific to scapy
    arp_request_broadcast=broadcast/arp_request
    # print(arp_request_broadcast)
    #send packet with srp instead od sr because custom ethernet packet
    try:
        answered=scapy.srp(arp_request_broadcast,timeout=1, verbose=False)[0]
    except PermissionError:
        print(colored("[-]", "red") + " Access denied, please run with sudo privileges\n")
    clients_list=[]
    for element in answered:
        client_dict={"ip":element[1].psrc,"mac":element[1].hwsrc}
        clients_list.append(client_dict)
        # print(element[1].psrc+"\t\t"+element[1].hwsrc)
        #
        # print("------------------------------------")
    return clients_list

def get_arguments():
    parser=optparse.OptionParser()
    parser.add_option("-t","--target",dest="target",help="Target IP / IP range")
    (options,arguments)=parser.parse_args()
    if not options.target:
        parser.error(colored("[-]", "red") + " Please specify a target, use --help for more info")

    return options

def print_result(clients_list):
    print("IP\t\t\tMAC\n-----------------------------")
    for client in clients_list:
        print(client["ip"]+"\t\t"+client["mac"])

def main():
    options=get_arguments()
    scan_result = scan(options.target)
    print_result(scan_result)

if __name__ == "__main__":
    main()
