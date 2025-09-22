import random
import subprocess
import time
import psutil
import os
import sys
import threading

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
    except Exception:
        print(f"\n[!] Fatal Error: Adapter Failure for {adapter}")

def reset_network():
    try:
        subprocess.run("ipconfig /release", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)
        subprocess.run("ipconfig /renew", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        print("\n[!] Fatal Error during network reset")

def spoof_all_adapters():
    adapters = [name for name in psutil.net_if_addrs() if "loopback" not in name.lower()]
    if not adapters:
        print("[-] Fatal Error: Adapter list not reachable")
        return
    for adapter in adapters:
        spoof_mac(adapter)
    reset_network()

def typewriter_title(text, stop_event, delay=0.15):
    while not stop_event.is_set():
        for i in range(1, len(text) + 1):
            if stop_event.is_set():
                break
            os.system(f"title {text[:i]}")
            time.sleep(delay)
        time.sleep(0.5)
        for i in range(len(text), 0, -1):
            if stop_event.is_set():
                break
            os.system(f"title {text[:i]}")
            time.sleep(delay)
        time.sleep(0.2)

if __name__ == "__main__":
    if os.name != "nt":
        print("[-] Get off linux you skid.")
        sys.exit(0)

    title_text = "Made by @guns.lol/bored777"
    stop_event = threading.Event()
    title_thread = threading.Thread(target=typewriter_title, args=(title_text, stop_event), daemon=True)
    title_thread.start()

    print("[*] Spoofing...")
    spoof_all_adapters()
    stop_event.set()
    title_thread.join()
    os.system(f"title {title_text}")
    print("[*] Spoofed Successfully.")
    time.sleep(3)
