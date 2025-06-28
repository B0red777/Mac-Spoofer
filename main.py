import random
import subprocess
import time
import psutil
import os
import sys

def generate_mac():
    return "".join(random.choice("0123456789ABCDEF") for _ in range(12))

def spoof_mac(adapter):
    mac = generate_mac()
    try:
        command = f"Get-NetAdapter -Name '{adapter}' | Set-NetAdapterAdvancedProperty -RegistryKeyword 'NetworkAddress' -RegistryValue '{mac}'"
        subprocess.run(["powershell", "-Command", command], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["powershell", "-Command", f"Disable-NetAdapter -Name '{adapter}' -Confirm:$false"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        subprocess.run(["powershell", "-Command", f"Enable-NetAdapter -Name '{adapter}'"], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"[+] MAC spoofed: {adapter} -> {mac}")
    except Exception as e:
        print(f"[!] Failed to spoof {adapter}: {e}")

def reset_network():
    try:
        subprocess.run("ipconfig /release", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        subprocess.run("ipconfig /renew", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("[+] Network reset complete.")
    except Exception as e:
        print(f"[!] Network reset failed: {e}")

def main():
    if os.name != "nt":
        print("[-] This tool only works on Windows.")
        return

    adapters = [name for name in psutil.net_if_addrs() if "loopback" not in name.lower()]
    if not adapters:
        print("[-] No network adapters found.")
        return

    for adapter in adapters:
        spoof_mac(adapter)

    reset_network()

if __name__ == "__main__":
    print("[*] Starting Tool...")
    main()
    print("[*] Spoofed successfully.")
