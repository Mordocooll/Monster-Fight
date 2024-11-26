import time, random, tkinter
import tkinter as tk

# Setting up GUI
root = tkinter.Tk()
root.geometry("1250x1150")
root.title("Monster Fight Demo")

# Background image
bg_image = tk.PhotoImage(file="Monster_Fight_GUI.png")
bg_label = tkinter.Label(root, image=bg_image)
bg_label.pack(expand=True, fill=tk.BOTH)

# Monster images and names and rage threshhold (rage is just monster getting stronger after a certain damage is dealt)
monsters = [
    {"name": "Goblin", "image": "goblin.png", "rage_threshold": 40, "health": 80},
    {"name": "Skeleton", "image": "skeleton.png", "rage_threshold": 50, "health": 100},
    {"name": "Zombie", "image": "zombie.png", "rage_threshold": 60, "health": 130},
    {"name": "Dragon", "image": "dragon.png", "rage_threshold": 70, "health": 160}
]

# Randomly select a monster
monster_choice = random.choice(monsters)
m_name = monster_choice["name"]
monster_image = tk.PhotoImage(file=monster_choice["image"])
monster_image_resized = monster_image.subsample(2)
monster_label = tkinter.Label(root, image=monster_image_resized, bg='#fafbf8')
monster_label.place(x=750, y=120)

# Resizing player image
original_player_image = tk.PhotoImage(file="knight.png")
player_image = original_player_image.subsample(2) 
player_label = tkinter.Label(root, image=player_image, bg='#fafbf8')
player_label.place(x=100, y=450)

# Player and monster stats
p_name = "Albert"
p_health = 100
p_attack_dmg = random.randint(5, 12)

m_health = monster_choice["health"]
m_rage = 0  # Monster rage level
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
    global m_health, p_health, turn, m_rage, m_attack_dmg
    turn += 1
    p_attack_dmg = random.randint(5, 12)
# 15% chance of crit atk
    if random.random() < 0.15:
        p_attack_dmg *= 2
        action_label.config(text=f"Critical hit! You did {p_attack_dmg} damage!")
    else:
        action_label.config(text=f"You did {p_attack_dmg} damage to the {m_name}.")
    
    m_health -= p_attack_dmg
# Monster rage is the damage player does
    m_rage += p_attack_dmg
    
    if m_rage >= monster_choice["rage_threshold"]:
        m_rage = 0
# Monster damage increased when rage is met
        m_attack_dmg += 5
        action_label.config(text=f"The {m_name} is enraged!\n It becomes stronger.")
    
    if m_health <= 0:  
        m_health = 0
        monster_health_lbl.config(text=f"{m_health}")
        action_label.config(text=f"You defeated the {m_name}!")
        disable_all_btns()
        monster_label.config(state="disabled")
        return
    
# After attack the buttons are disabled until continue is pressed
    disable_all_btns()  
    enable_continue_btn() 
    
    player_health_lbl.config(text=f"{p_health}")
    monster_health_lbl.config(text=f"{m_health}")

# Player runs from fight
def p_run():
    action_label.config(text="You have fled the fight.")
    disable_all_btns()

# Player heals
def p_heal():
    global p_health, turn, heal_turn_tracker
    if turn - heal_turn_tracker >= 4: 
        heal_turn_tracker = turn
        p_heal_amt = random.randint(8, 15)
        p_health += p_heal_amt
        player_health_lbl.config(text=f"{p_health}")
        action_label.config(text=f"You consumed a healing potion\n and gained {p_heal_amt} health!")
    else:
        action_label.config(text="You can only heal once\n every 4 turns!")
# Player parrys
def p_parry():
    global p_health, m_health, turn, m_attack_dmg
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
        return
# Command for continue button so player and monster damage are displayed after attacking
def continue_turn():
    global p_health, m_health, m_attack_dmg
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

# Player and monster names and health displayed
player_name_lbl = tkinter.Label(root, text=p_name, font=('', 40, 'bold'), bg='#fafbf8')
player_name_lbl.place(x=75, y=40)

player_health_lbl = tkinter.Label(root, text=f"{p_health}", font=('', 32, 'bold'), bg='#fafbf8')
player_health_lbl.place(x=280, y=133)

monster_name_lbl = tkinter.Label(root, text=m_name, font=('', 40, 'bold'), bg='#fafbf8')
monster_name_lbl.place(x=640, y=500)

monster_health_lbl = tkinter.Label(root, text=f"{m_health}", font=('', 32, 'bold'), bg='#fafbf8')
monster_health_lbl.place(x=800, y=580)

# Label where all actions are displayed
action_label = tkinter.Label(root, text="A " + m_name + " appears!", font=("", 18), bg='#fafbf8')
action_label.place(x=130, y=920)

# Buttons for player actions
fight_btn = tkinter.Button(root, text="Fight", font=("", 30), height=1, width=7, bg='#fafbf8', command=p_attack)
fight_btn.place(x=730, y=880)

run_btn = tkinter.Button(root, text="Run", font=("", 30), height=1, width=7, bg='#fafbf8', command=p_run)
run_btn.place(x=901, y=959)

parry_btn = tkinter.Button(root, text="Parry", font=("", 30), height=1, width=7, bg='#fafbf8', command=p_parry)
parry_btn.place(x=901, y=880)

heal_btn = tkinter.Button(root, text="Heal", font=("", 30), height=1, width=7, bg='#fafbf8', command=p_heal)
heal_btn.place(x=730, y=959)

continue_btn = tkinter.Button(root, text="Continue", font=("", 30), height=1, width=7, bg='#fafbf8', command=continue_turn)
continue_btn.place(x=170, y=1000)
disable_continue_btn()

turns_lbl = tkinter.Label(root, text=0, bg='#fafbf8')
turns_lbl.pack()

root.mainloop()
