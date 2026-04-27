import os
import time
import random
from ppadb.client import Client as AdbClient

def start_bot():
    guild_id = "3047387700"
    package = "com.dts.freefireth"
    
    print("Connecting to ADB Server...")
    client = AdbClient(host="127.0.0.1", port=5037)
    
    # Wait for device to be ready
    device = None
    while not device:
        devices = client.devices()
        if len(devices) > 0:
            device = devices[0]
        else:
            print("Waiting for device...")
            time.sleep(5)

    print(f"[+] Bot Connected: {device.serial}")
    
    # Spawn Logic
    print("[*] Clearing old data and spoofing ID...")
    device.shell(f"pm clear {package}")
    new_id = "".join(random.choices("0123456789abcdef", k=16))
    device.shell(f"settings put secure android_id {new_id}")
    
    print("[*] Launching Free Fire...")
    device.shell(f"monkey -p {package} -c android.intent.category.LAUNCHER 1")
    
    # Wait for game to load
    time.sleep(60)
    
    # Guest Login Taps (Adjust coordinates if needed)
    print("[!] Attempting Guest Login...")
    device.shell("input tap 960 800") # Guest Button
    time.sleep(15)
    device.shell("input tap 960 950") # Tap to Begin
    
    print(f"[!] Sending Guild Request to {guild_id}...")
    # Add your specific guild search taps here
    # For now, we log the attempt
    print(f"[✓] Bot is now active on GitHub Server. Check your Guild Requests!")

if __name__ == "__main__":
    try:
        start_bot()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
