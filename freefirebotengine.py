import os
import time
import random
import multiprocessing
from ppadb.client import Client as AdbClient

class NexusBot:
    def __init__(self, bot_num, port, guild_id):
        self.bot_num = bot_num
        self.port = port
        self.guild_id = guild_id
        self.package = "com.dts.freefireth"
        self.device = None

    def connect(self):
        try:
            client = AdbClient(host="127.0.0.1", port=5037)
            self.device = client.device(f"localhost:{self.port}")
            return self.device
        except Exception as e:
            print(f"Connection Error Bot {self.bot_num}: {e}")
            return None

    def spawn(self):
        if not self.device: return
        print(f"[+] Bot {self.bot_num}: Spawning...")
        self.device.shell(f"pm clear {self.package}")
        new_id = "".join(random.choices("0123456789abcdef", k=16))
        self.device.shell(f"settings put secure android_id {new_id}")
        self.device.shell(f"monkey -p {self.package} -c android.intent.category.LAUNCHER 1")
        time.sleep(40)

    def tap(self, x, y):
        if self.device:
            rx, ry = x + random.randint(-5, 5), y + random.randint(-5, 5)
            self.device.shell(f"input tap {rx} {ry}")

    def run_logic(self):
        self.spawn()
        print(f"[!] Bot {self.bot_num}: Sending Guild Request to {self.guild_id}...")
        # Basic sequence to reach guild search
        time.sleep(20)
        self.device.shell(f"input text {self.guild_id}")
        time.sleep(5)
        # Search and Join Taps
        self.tap(1700, 200) 
        time.sleep(2)
        self.tap(1600, 900)
        print(f"[✓] Bot {self.bot_num}: Request cycle finished.")

def start_bot_process(bot_num, port, guild_id):
    bot = NexusBot(bot_num, port, guild_id)
    if bot.connect():
        bot.run_logic()

if __name__ == "__main__":
    guild_id = os.getenv("GUILD_ID", "3047387700")
    # Running 2 bots in parallel
    p1 = multiprocessing.Process(target=start_bot_process, args=(1, 5555, guild_id))
    p2 = multiprocessing.Process(target=start_bot_process, args=(2, 5557, guild_id))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
