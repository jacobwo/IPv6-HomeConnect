#!/usr/bin/python3
import os
import time
import random
import string
import socket
import subprocess
from pyroute2 import IPRoute
import logging

# === Configuration ===
ETH_INTERFACE = "enp1s0"  # Network interface name
SSH_HOST = "sshlog"  # SSH alias defined in your SSH config
REMOTE_CMD = "/home/sshlog/logargv"
LOG_FILE = "ip_monitor.log"  # Log file path
RENEW_THRESHOLD = 72 * 3600

# === Logging Setup ===
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# === SSH Connection ===
def ssh_to_host(local_ip):
    # Generate a simple random string of 3-23 characters for obfuscation 
    obf = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(3, 23)))
    ssh_cmd = [
        "ssh",
        SSH_HOST,
        f"{REMOTE_CMD} {local_ip} {obf}"
    ]

    try:
        subprocess.run(ssh_cmd, check=True)
        return 0
    except subprocess.CalledProcessError as e:
        logging.error(f"SSH fail: {e.returncode}")
        return 1
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        return 1


# === Monitor local IPv6 address changes using Netlink ===
def monitor_netlink(ip):
    last_triggered_ip = None
    target_idx = ip.link_lookup(ifname=ETH_INTERFACE)[0]
    ip.bind()

    if addr_info := ip.get_addr(family=socket.AF_INET6, index=target_idx, scope=0):
        last_triggered_ip = addr_info[0].get_attr('IFA_ADDRESS')
        if ssh_to_host(last_triggered_ip) == 0:
            next_renew = time.monotonic() + RENEW_THRESHOLD + random.randint(0, 1800)
    while True:
        try:
            events = ip.get()
            for event in events:
                if event['event'] == 'RTM_NEWADDR' and event.get('family') == socket.AF_INET6:
                    if event.get('index') == target_idx:
                        attrs = dict(event['attrs'])
                        addr = attrs.get('IFA_ADDRESS')
                        if addr and not addr.startswith('fe80'):
                            if addr != last_triggered_ip:
                                logging.info(f"Detected Global IPv6 change on {ETH_INTERFACE}: {addr}")
                                if ssh_to_host(addr) == 0:
                                    last_triggered_ip = addr
                                    next_renew = time.monotonic() + RENEW_THRESHOLD + random.randint(0, 1800)
                                else:
                                    next_renew = time.monotonic() + 18000 + random.randint(0, 1800)
                            else:
                                now = time.monotonic()
                                if now > next_renew:
                                    if ssh_to_host("Renew") == 0:
                                        next_renew = now + RENEW_THRESHOLD + random.randint(0, 1800)
                                    else:
                                        next_renew = time.monotonic() + 18000 + random.randint(0, 1800)

        except socket.timeout:
           logging.info(f"Timeout")
           if ssh_to_host(last_triggered_ip) == 0:
              next_renew = time.monotonic() + 18000 + random.randint(0, 1800)
           continue

# === Main entry point ===
def main():
    ip = IPRoute()
    ip.settimeout(18000)
    monitor_netlink(ip)

if __name__ == "__main__":
    main()

