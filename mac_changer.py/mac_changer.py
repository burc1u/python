#!/usr/bin/env python3
import re
import subprocess
import optparse
from termcolor import colored

def change_mac(interface,new_mac):

    # without regular expression
    # if options.new_mac in ifconfig_result:
    #     print(colored("[+]", "blue") + " Changed MAC address for " + interface + " to " + new_mac)
    # else:
    #     print(colored("[-]", "red") + " Can not change MAC address for " + interface + " to " + new_mac)


    print(colored("[+]", "blue") + "Changing MAC address for " + interface + " to " + new_mac)
    # in a list to prevent malicious use of shell commands
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])
def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="interface to change MAC add")
    parser.add_option("-m", "--mac", dest="new_mac", help="new mac address")
    # parse the args from command line
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error(colored("[-]","red")+" Please specify an interface, use --help for more info")
    if not options.new_mac:
        parser.error(colored("[-]", "red") + " Please specify a new MAC, use --help for more info")
    return options
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # print(ifconfig_result)

    mac_add_search = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    # print(mac_add_search.group(0))

    if not mac_add_search:
        print(colored("[-]", "red") + "MAC address is null")
    else:
       # print(colored("[+]", "blue") + "MAC address found: "+mac_add_search.group(0))
        return  mac_add_search.group(0)
def main():
    options = get_arguments()
    print(colored("[+]","blue")+"Current MAC: "+str(get_current_mac(options.interface)))

    change_mac(options.interface,options.new_mac)
    if get_current_mac(options.interface)==options.new_mac:
        print(colored("[+]","blue")+"MAC address was successfully changed to "+options.new_mac)
    else:
        print(colored("[-]","red")+"MAC address was not changed")


if __name__=="__main__":
    main()



