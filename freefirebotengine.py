import os
import time
import random
from ppadb.client import Client as AdbClient

def start_bot():
    print("Connecting to ADB Server...")
    client = AdbClient(host="127.0.0.1", port=5037)
    
    # Wait for device to be fully ready
    device = None
    max_retries = 10
    for i in range(max_retries):
        devices = client.devices()
        if len(devices) > 0:
            device = devices[0]
            # Check if device is actually 'device' and not 'offline'
            state = device.get_state()
            if state == "device":
                print(f"[+] Bot Connected and Online: {device.serial}")
                break
        print(f"[*] Waiting for device to stabilize (Attempt {i+1}/{max_retries})...")
        time.sleep(10)

    if not device:
        print("CRITICAL ERROR: Device could not be reached. Check logs.")
        return

    package = "com.dts.freefireth"
    
    print("[*] Clearing old data...")
    device.shell(f"pm clear {package}")
    
    print("[*] Launching Free Fire...")
    device.shell(f"monkey -p {package} -c android.intent.category.LAUNCHER 1")
    
    # Game loading time (GitHub servers are slow, so we wait 2 mins)
    print("[!] Waiting 2 minutes for Game to Load...")
    time.sleep(120)
    
    # Screenshot to check progress
    result = device.screencap()
    with open("screen_check.png", "wb") as f:
        f.write(result)
    print("[#] Screenshot saved as screen_check.png")

if __name__ == "__main__":
    try:
        start_bot()
    except Exception as e:
        print(f"ERROR: {e}")
