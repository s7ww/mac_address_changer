import subprocess
import optparse
import re


def get_args():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not options.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more info.")

    return options

def change_mac(interface, new_mac):
    print(f"[+] Changing MAC address for {interface} to {new_mac}")
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])
def get_mac(interface):
    mac_change_result = subprocess.check_output(["ifconfig", interface]).decode(
        "utf-8")  # decode(utf...) because byte to string conversion
    regex_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", mac_change_result)
    if regex_result:
        return regex_result.group(0)
    else:
        print("[-f] could not read mac address")

options = get_args()
cur_mac=get_mac(options.interface)
print("current mac= " + str(cur_mac))
change_mac(options.interface, options.new_mac)
cur_mac=get_mac(options.interface)
if cur_mac==options.new_mac:
    print("mac was successfuly changed to " + cur_mac)






