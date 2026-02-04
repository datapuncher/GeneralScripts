#!/opt/miniconda3/bin/python

import socket
from scapy.all import ARP, Ether, srp


def get_hostname_from_ip(ip_address):
    """
    Attempts to retrieve the hostname for a given IP address using reverse DNS lookup.
    """
    try:
        hostname, _, _ = socket.gethostbyaddr(ip_address)
        return hostname
    except socket.herror:
        return f"Hostname not found for IP: {ip_address}"
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage:
ip_to_check = "192.168.1.1"  # Replace with the IP address of the device
hostname = get_hostname_from_ip(ip_to_check)
print(f"The hostname for {ip_to_check} is: {hostname}")

def discover_ips_and_get_hostnames(ip_range):
    """
    Discovers active IPs in a given range using ARP scan and then attempts
    to get hostnames for them.
    """
    print(f"Scanning IP range: {ip_range}")
    ans, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_range), timeout=2, verbose=0)

    devices = []
    for _, received in ans:
        ip = received.psrc
        mac = received.hwsrc
        hostname = get_hostname_from_ip(ip)
        devices.append({"IP": ip, "MAC": mac, "Hostname": hostname})
    return devices

# Example usage with Scapy ARP scan:
local_network_range = "192.168.1.0/24"  # Adjust to your network range
discovered_devices = discover_ips_and_get_hostnames(local_network_range)

print("\nDiscovered Devices:")
for device in discovered_devices:
    print(f"IP: {device['IP']}, MAC: {device['MAC']}, Hostname: {device['Hostname']}")
