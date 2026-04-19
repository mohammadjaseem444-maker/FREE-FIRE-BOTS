# ╔══════════════════════════════════════════════════════════════════╗
# ║ NEXUS-AI SOVEREIGN ENGINE: PARALLEL SQUAD LOGIC (4 BOTS)         ║
# ║ MISSION: 100% SQUAD COHESION - NO BOT LEFT BEHIND                ║
# ╚══════════════════════════════════════════════════════════════════╝

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
        client = AdbClient(host="127.0.0.1", port=5037)
        self.device = client.device(f"localhost:{self.port}")
        return self.device

    def spawn(self):
        """Birth & Identity Spoofing"""
        print(f"[+] Bot {self.bot_num} (Port {self.port}): Spawning Identity...")
        self.device.shell(f"pm clear {self.package}")
        new_id = "".join(random.choices("0123456789abcdef", k=16))
        self.device.shell(f"settings put secure android_id {new_id}")
        self.device.shell(f"monkey -p {self.package} -c android.intent.category.LAUNCHER 1")
        time.sleep(40) # Wait for FF to load

    def tap(self, x, y):
        rx, ry = x + random.randint(-5, 5), y + random.randint(-5, 5)
        self.device.shell(f"input tap {rx} {ry}")

    def join_guild(self):
        """Request Guild Entry"""
        print(f"[!] Bot {self.bot_num}: Sending Guild Request...")
        self.tap(960, 800) # Guest Login
        time.sleep(15)
        self.tap(960, 950) # Begin
        time.sleep(20)
        # Guild search & request logic
        self.device.shell(f"input text {self.guild_id}")
        time.sleep(2)
        self.tap(1700, 200) # Search
        time.sleep(2)
        self.tap(1600, 900) # Join
        print(f"[✓] Bot {self.bot_num}: Request sent to {self.guild_id}")

    def play_as_squad(self, is_leader, team_code=None):
        """Squad Coordination Logic"""
        if is_leader:
            print(f"[👑] Bot {self.bot_num} is Squad Leader.")
            self.tap(1700, 800) # Create Squad
            time.sleep(5)
            # In real scenario, we'd OCR the team code here. 
            # For this logic, we assume leader invites or others join via Team Code UI.
            self.tap(1750, 950) # Start Match when squad is full
        else:
            print(f"[👤] Bot {self.bot_num} joining squad...")
            # Logic to input team code or accept invite
            time.sleep(10) # Wait for leader to set up
            
        # Match Grinding
        print(f"[*] Bot {self.bot_num}: In Match - Grinding Glory...")
        for _ in range(8):
            # Human Mimicry Movements
            self.device.shell(f"input swipe {random.randint(200,500)} 700 {random.randint(200,500)} 750 200")
            time.sleep(random.randint(20, 40))
        
        # Return to Lobby
        self.tap(100, 50)
        time.sleep(10)

def start_bot_process(bot_num, port, guild_id):
    bot = NexusBot(bot_num, port, guild_id)
    bot.connect()
    bot.spawn()
    bot.join_guild()
    
    # Wait for Bhai to accept all 4 bots in the guild
    print(f"--- Bot {bot_num} waiting for Guild Acceptance (60s) ---")
    time.sleep(60) 
    
    # Loop for continuous matches
    for match_num in range(10):
        # Bot 1 of each squad is the leader
        is_leader = (bot_num == 1)
        bot.play_as_squad(is_leader)

if __name__ == "__main__":
    guild_id = os.getenv("GUILD_ID", "3047387700")
    
    # 4 Bots in Parallel for the Squad
    processes = []
    for i in range(1, 5):
        port = 5554 + (i * 2)
        p = multiprocessing.Process(target=start_bot_process, args=(i, port, guild_id))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

    print(f"[†] Squad {os.getenv('SQUAD_ID')} has finished its daily duty.")
