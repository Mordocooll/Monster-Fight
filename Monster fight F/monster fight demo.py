import time, random, tkinter
import tkinter as tk
from tkinter import *


# Function to launch the game
def start_game():
# Clear the initial screen
    for widget in root.winfo_children():
        widget.destroy()

# Setting up the game GUI
    root.geometry("1250x1150")
    root.title("Monster Fight Demo")

# Background image
    bg_image = PhotoImage(file="Monster_Fight_GUI-removebg.png")
    bg_label = Label(root, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0)

# Monster images and names and rage threshold
    monsters = [
        # Tier 1
        {"name": "Goblin", "image": "goblin.png", "rage_threshold": 40, "health": 80},
        {"name": "Mummy", "image": "mummy.png", "rage_threshold": 40, "health": 80},
        {"name": "Wolf", "image": "wolf.png", "rage_threshold": 40, "health": 80},
        {"name": "Skeleton", "image": "skeleton.png", "rage_threshold": 40, "health": 80},
        {"name": "Zombie", "image": "zombie.png", "rage_threshold": 40, "health": 80},

        # Tier 2
        {"name": "Vampire", "image": "vampire.png", "rage_threshold": 60, "health": 90},
        {"name": "Wendigo", "image": "wendigo.png", "rage_threshold": 60, "health": 90},
        {"name": "Dullhan", "image": "dullhan.png", "rage_threshold": 60, "health": 90},

        #Tier 3
        {"name": "Dragon", "image": "dragon.png", "rage_threshold": 80, "health": 110}

    ]

# Randomly select a monster
    monster_choice = random.choice(monsters)
    m_name = monster_choice["name"]
    monster_image = PhotoImage(file=monster_choice["image"])
    monster_image_resized = monster_image.subsample(2)
    monster_label = Label(root, image=monster_image_resized, bg='#a2cad3')
    monster_label.image = monster_image_resized 
    monster_label.place(x=750, y=120)

    # Resizing player image
    original_player_image = PhotoImage(file="knight.png")
    player_image = original_player_image.subsample(2)
    player_label = Label(root, image=player_image, bg='#a2cad3')
    player_label.image = player_image  
    player_label.place(x=100, y=450)

    # Player and monster stats
    p_name = "Albert"
    p_health = 100
    p_attack_dmg = random.randint(5, 12)

    m_health = monster_choice["health"]
    m_rage = 0 
    m_attack_dmg = random.randint(10, 13)

    turn = 0
    heal_turn_tracker = -4

    # Functions for button commands
    def disable_all_btns():
        fight_btn.config(state="disabled")
        run_btn.config(state="disabled")
        parry_btn.config(state="disabled")
        heal_btn.config(state="disabled")

    def enable_action_btns():
        fight_btn.config(state="normal")
        parry_btn.config(state="normal")
        heal_btn.config(state="normal")

    def disable_continue_btn():
        continue_btn.config(state="disabled")

    def enable_continue_btn():
        continue_btn.config(state="normal")

    def p_attack():
        nonlocal m_health, p_health, turn, m_rage, m_attack_dmg
        turn += 1
        p_attack_dmg = random.randint(5, 12)
        if random.random() < 0.15:
            p_attack_dmg *= 2
            action_label.config(text=f"Critical hit! You did {p_attack_dmg} damage!")
        else:
            action_label.config(text=f"You did {p_attack_dmg} damage to the {m_name}.")

        m_health -= p_attack_dmg
        m_rage += p_attack_dmg

        if m_rage >= monster_choice["rage_threshold"]:
            m_rage = 0
            m_attack_dmg += 5
            action_label.config(text=f"The {m_name} is enraged!\n It becomes stronger.")

        if m_health <= 0:
            m_health = 0
            monster_health_lbl.config(text=f"{m_health}")
            action_label.config(text=f"You defeated the {m_name}!")
            disable_all_btns()
            monster_label.config(state="disabled")
            return

        disable_all_btns()
        enable_continue_btn()

        player_health_lbl.config(text=f"{p_health}")
        monster_health_lbl.config(text=f"{m_health}")

    def p_run():
        action_label.config(text="You have fled the fight.")
        disable_all_btns()

    def p_heal():
        nonlocal p_health, turn, heal_turn_tracker
        if turn - heal_turn_tracker >= 4:
            heal_turn_tracker = turn
            p_heal_amt = random.randint(8, 15)
            p_health += p_heal_amt
            player_health_lbl.config(text=f"{p_health}")
            action_label.config(text=f"You consumed a healing potion\n and gained {p_heal_amt} health!")
        else:
            action_label.config(text="You can only heal once\n every 4 turns!")

    def p_parry():
        nonlocal p_health, m_health, turn, m_attack_dmg
        turn += 1
        m_attack_dmg = random.randint(10, 13)
        parry_m_attack_dmg = round(m_attack_dmg * 0.7, 0)
        parry_p_deflect_dmg = round(m_attack_dmg * 0.4, 0)
        p_health -= parry_m_attack_dmg
        m_health -= parry_p_deflect_dmg
        action_label.config(text=f"You took {parry_m_attack_dmg} and deflected\n {parry_p_deflect_dmg} damage.")
        player_health_lbl.config(text=f"{p_health}")
        monster_health_lbl.config(text=f"{m_health}")

        if m_health <= 0:
            m_health = 0
            monster_health_lbl.config(text=f"{m_health}")
            action_label.config(text=f"You defeated the {m_name}!")
            monster_label.config(state="disabled")
            disable_all_btns()
        if p_health <= 0:
            p_health = 0
            player_health_lbl.config(text=f"{p_health}")
            action_label.config(text=f"You died")
            disable_all_btns()
            player_label.config(state="disabled")

    def continue_turn():
        nonlocal p_health, m_health, m_attack_dmg
        m_attack_dmg = random.randint(10, 13)
        p_health -= m_attack_dmg
        action_label.config(text=f"The {m_name} attacks!\n It did {m_attack_dmg} damage to you.")
        player_health_lbl.config(text=f"{p_health}")

        if m_health <= 0:
            m_health = 0
            monster_health_lbl.config(text=f"{m_health}")
            action_label.config(text=f"You defeated the {m_name}!")
            disable_all_btns()
            monster_label.config(state="disabled")
        if p_health <= 0:
            p_health = 0
            player_health_lbl.config(text=f"{p_health}")
            action_label.config(text=f"You died")
            disable_all_btns()
            player_label.config(state="disabled")
            return

        enable_action_btns()
        disable_continue_btn()

    # Player and monster names and health labels
    player_name_lbl = Label(root, text=p_name, font=('', 40, 'bold'), bg='#a2cad3')
    player_name_lbl.place(x=75, y=40)

    player_health_lbl = Label(root, text=f"{p_health}", font=('', 32, 'bold'), bg='#a2cad3')
    player_health_lbl.place(x=280, y=133)

    monster_name_lbl = Label(root, text=m_name, font=('', 40, 'bold'), bg='#a2cad3')
    monster_name_lbl.place(x=640, y=500)

    monster_health_lbl = Label(root, text=f"{m_health}", font=('', 32, 'bold'), bg='#a2cad3')
    monster_health_lbl.place(x=800, y=580)

    # Label where all actions are displayed
    action_label = Label(root, text="A " + m_name + " appears!", font=("", 18), bg='#a2cad3')
    action_label.place(x=130, y=920)

    # Buttons for player actions
    fight_btn = Button(root, text="Fight", font=("", 30), height=1, width=7, bg='#a2cad3', command=p_attack)
    fight_btn.place(x=730, y=880)

    run_btn = Button(root, text="Run", font=("", 30), height=1, width=7, bg='#a2cad3', command=p_run)
    run_btn.place(x=901, y=959)

    parry_btn = Button(root, text="Parry", font=("", 30), height=1, width=7, bg='#a2cad3', command=p_parry)
    parry_btn.place(x=901, y=880)

    heal_btn = Button(root, text="Heal", font=("", 30), height=1, width=7, bg='#a2cad3', command=p_heal)
    heal_btn.place(x=730, y=959)

    continue_btn = Button(root, text="Continue", font=("", 30), height=1, width=7, bg='#a2cad3', command=continue_turn)
    continue_btn.place(x=170, y=1000)
    disable_continue_btn()

    turns_lbl = Label(root, text=0, bg='#a2cad3')
    turns_lbl.pack()

    root.mainloop()


def start_fight():
# Clear the start window
    for widget in root.winfo_children():
        widget.destroy()

# fight GUI
    start_game()

root = Tk()
root.geometry("1250x1150")

def start_screen():
    bg_image_start = PhotoImage(file="Forest.png")
    bg_label_start = Label(root, image=bg_image_start)
    bg_label_start.image = bg_image_start  
    bg_label_start.pack(expand=True, fill=BOTH)

    start_fight_lbl = Label(root, text="You hear a crinkle behind a tree", font=("", 30), bg = '#a2cad3')
    start_fight_lbl.place(x = 340, y = 700)

    start_fight_btn = Button(root, text="Investigate", font=("", 30), bg = '#a2cad3', command=start_fight)
    start_fight_btn.place(x = 490, y = 850)

# runs start screen then the fighting
start_screen()
root.mainloop()
