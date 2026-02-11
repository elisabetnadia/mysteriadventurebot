"""
Legend of the Code Realm
Text-based Fantasy RPG Engine (CLI)

Author : Your Name
Purpose: Portfolio Project
"""

import time
import random
import json
from dataclasses import dataclass, field
import sys

# =========================
# UTILITIES
# =========================

def slow_print(text, delay=0.02):
    for c in text:
        print(c, end="", flush=True)
        time.sleep(delay)
    print()

def dramatic_print(text, delay=0.01, pause=0.5):
    """Untuk efek dramatis ekstra dengan jeda panjang di akhir"""
    slow_print(text, delay)
    time.sleep(pause)

def choose(prompt, options):
    dramatic_print(prompt)
    for i, opt in enumerate(options, 1):
        dramatic_print(f"{i}. {opt}", delay=0.01, pause=0.05)
    while True:
        ans = input("> ").strip()
        if ans.isdigit() and 1 <= int(ans) <= len(options):
            return options[int(ans)-1]
        dramatic_print("Pilihan tidak valid. Coba lagi...")

# =========================
# GAME STATE
# =========================

@dataclass
class Player:
    name: str
    hp: int = 100
    max_hp: int = 100
    atk: int = 12
    inventory: list = field(default_factory=list)
    gold: int = 0
    keys: int = 0

# =========================
# SAVE / LOAD
# =========================

SAVE_FILE = "save_game.json"

def save_game(player):
    with open(SAVE_FILE, "w") as f:
        json.dump(player.__dict__, f, indent=2)
    dramatic_print("💾 Game berhasil disimpan.\n", pause=0.3)

def load_game():
    try:
        with open(SAVE_FILE) as f:
            data = json.load(f)
        dramatic_print("📂 Save ditemukan.\n")
        return Player(**data)
    except FileNotFoundError:
        dramatic_print("Tidak ada save.\n")
        return None

# =========================
# COMBAT SYSTEM
# =========================

def combat(player, enemy_name, enemy_hp, enemy_atk):
    dramatic_print(f"\n⚔️ {enemy_name} muncul! Bersiaplah!", pause=0.5)
    while enemy_hp > 0 and player.hp > 0:
        dramatic_print(f"HP Kamu: {player.hp} | HP {enemy_name}: {enemy_hp}", delay=0.01)
        action = choose("Apa yang akan kau lakukan?", ["Serang", "Gunakan Potion", "Kabur"])

        if action == "Serang":
            dmg = random.randint(player.atk-2, player.atk+5)
            dramatic_print(f"Kau menyerang! Damage: {dmg}")
            enemy_hp -= dmg

        elif action == "Gunakan Potion":
            if "Potion" in player.inventory:
                player.hp = min(player.max_hp, player.hp+30)
                player.inventory.remove("Potion")
                dramatic_print("Potion digunakan. +30 HP")
            else:
                dramatic_print("Kau tidak punya Potion!")

        else:
            if random.random() < 0.5:
                dramatic_print("Kau berhasil kabur!\n")
                return False
            else:
                dramatic_print("Gagal kabur!")

        if enemy_hp > 0:
            edmg = random.randint(enemy_atk-2, enemy_atk+3)
            dramatic_print(f"{enemy_name} menyerang! Damage: {edmg}")
            player.hp -= edmg

    return player.hp > 0

# =========================
# ASCII ART
# =========================

sword_art = r"""
         />_________________________________
[#########################################]
         \>_________________________________
"""

skull_art = r"""
       .-''''-.
      /  .--.  \
     /  /    \  \
     |  |    |  |
     |  |.-""-.|
    ///`.::::.`\
   ||| ::/  \:: ;
   ||; ::\__/:: ;
    \\\'::::::' /
     `=':-..-'`
"""

# =========================
# STORY NODES
# =========================

def forest_node(player):
    dramatic_print("\n🌲 HUTAN SINTAKS 🌲")
    dramatic_print("Pepohonan berkilau dengan rune magis.")
    choice = choose("Makhluk Rune menghadangmu.", ["Lawan", "Negosiasi"])

    if choice == "Lawan":
        if combat(player, "Rune Beast", 50, 10):
            dramatic_print("Musuh tumbang. Kau mendapat Potion!")
            player.inventory.append("Potion")
        else:
            bad_ending(player)
    else:
        dramatic_print("Makhluk memberimu jimat kekuatan.")
        player.atk += 5

def valley_node(player):
    dramatic_print("\n🏞️ LEMBAH KODE 🏞️")
    dramatic_print("Laptop raksasa tergeletak di tengah lembah.")
    choice = choose("Apa yang kau lakukan?", ["Gunakan IDE canggih", "Gunakan Editor sederhana"])

    if choice == "Gunakan IDE canggih":
        dramatic_print("Produktivitasmu meningkat! Kau mendapat Potion tambahan.")
        player.inventory.append("Potion")
    else:
        if random.random() < 0.3:
            dramatic_print("Keberuntungan! Editor sederhana bekerja dengan baik.")
            player.inventory.append("Potion")
        else:
            dramatic_print("Editor sederhana membuatmu salah langkah. -20 HP")
            player.hp -= 20
            if player.hp <= 0:
                bad_ending(player)

def cave_node(player):
    dramatic_print("\n🕸️ GUA ALGORITMA 🕸️")
    dramatic_print("Kamu mendengar suara bisikan 'Segmentation fault' dari kegelapan.")
    choice = choose("Ada dua jalan di gua:", ["Jalan gelap", "Jalan bercahaya"])

    if choice == "Jalan gelap":
        if combat(player, "Bug Goblin", 40, 12):
            dramatic_print("Kau menemukan Potion di tubuh Goblin.")
            player.inventory.append("Potion")
        else:
            bad_ending(player)
    else:
        dramatic_print("Jalan bercahaya membawa kau ke harta tersembunyi: 50 Gold!")
        player.gold += 50

def village_node(player):
    dramatic_print("\n🏘️ DESA BUG 🏘️")
    dramatic_print("Penduduk desa kesulitan karena bug berhamburan di mana-mana.")
    choice = choose("Apa yang kau lakukan?", ["Bantu mereka", "Lewati desa"])

    if choice == "Bantu mereka":
        dramatic_print("Penduduk memberimu kunci rahasia menara.")
        player.keys += 1
    else:
        dramatic_print("Kau melewati desa dengan hati berat.")

def tower_node(player):
    dramatic_print("\n🏰 MENARA RUNTIME 🏰")
    if player.keys == 0:
        dramatic_print("Kau tidak memiliki kunci rahasia. Pintu menara terkunci!")
        bitter_ending(player)
    else:
        dramatic_print("Dengan kunci rahasia, kau masuk ke menara.")
    dramatic_print("Kristal Takdir berdetak di puncak menara.")
    choice = choose("Apa yang kau lakukan?", ["Stabilkan dengan ritual", "Paksa aktifkan"])
    if choice == "Stabilkan dengan ritual":
        good_ending(player)
    else:
        if random.random() < 0.5:
            lucky_ending(player)
        else:
            player.hp -= 50
            if player.hp <= 0:
                bad_ending(player)
            else:
                bitter_ending(player)

# =========================
# ENDINGS
# =========================

def good_ending(player):
    dramatic_print("\n✨ ENDING LEGENDARIS ✨")
    dramatic_print(f"{player.name} menjadi Penjaga Kode. Dunia selamat!")
    dramatic_print(sword_art, pause=1)
    exit()

def lucky_ending(player):
    dramatic_print("\n🍀 ENDING BUG BERKAH 🍀")
    dramatic_print("Keberuntungan aneh menyelamatkan dunia.")
    dramatic_print(sword_art, pause=1)
    exit()

def bitter_ending(player):
    dramatic_print("\n🌘 ENDING PAHIT 🌘")
    dramatic_print("Dunia selamat, tapi namamu dilupakan...")
    dramatic_print(skull_art, pause=1)
    exit()

def bad_ending(player):
    dramatic_print("\n💀 ENDING GELAP 💀")
    dramatic_print("Runtime runtuh. Dunia berhenti.")
    dramatic_print(skull_art, pause=1)
    exit()

# =========================
# MAIN LOOP
# =========================

def main():
    dramatic_print("=== LEGEND OF THE CODE REALM ===\n", pause=1)

    if choose("Load game?", ["Ya", "Tidak"]) == "Ya":
        player = load_game()
        if not player:
            name = input("Namamu: ") or "Pengembara"
            player = Player(name=name)
    else:
        name = input("Namamu: ") or "Pengembara"
        player = Player(name=name)

    dramatic_print(f"\nSelamat datang, {player.name}! Bersiaplah untuk petualanganmu...\n", pause=0.5)

    # Sequence node cerita
    forest_node(player)
    valley_node(player)
    cave_node(player)
    village_node(player)

    if choose("Simpan game?", ["Ya", "Tidak"]) == "Ya":
        save_game(player)

    tower_node(player)

# =========================
# RUN
# =========================

if __name__ == "__main__":
    main()
