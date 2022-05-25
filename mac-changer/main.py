#!/usr/bin/env python3

import subprocess
import optparse
import re
from logo import text_logo
from tqdm import tqdm

def get_arguments():
    """Takes input using flags and returns the values"""
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()
    if not options.interface:

        parser.error("\n[-] Please specify an interface. Use '--help' for more info.")
    if not options.new_mac:
        parser.error("\n[-] Please specify a mac address to change. Use '--help' for more info.")
    return parser.parse_args()

def change_mac(interface, new_mac):
    """Change your current MAC Address"""
    print(f"\n[+] Changing MAC address for {interface} to {new_mac}\n")
    loop = tqdm(total=7000, position=0, leave=False)
    for i in range(7000):
        loop.set_description("Changing MAC address...".format(i))
        loop.update(1)
    loop.close()
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_mac(interface):
    """Returns your current MAC Address"""
    # use decode() to convert bytes to string
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode()
    mac_search_results = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    mac_addr = mac_search_results.group(0)

    if mac_search_results:
        return mac_addr
    else:
        print("[-] Could not read MAC address")

def check_success():
    """Check If MAC Address was changed"""
    current_mac = get_mac(options.interface)
    if current_mac == options.new_mac:
        print(f"[+] MAC address has been successfully changed to {current_mac}.")
    else:
        print("[-] MAC address has not changed.")

print(text_logo)
(options, arguments) = get_arguments()
change_mac(options.interface, options.new_mac)
check_success()




