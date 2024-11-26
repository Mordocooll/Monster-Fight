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

# Monster images and names
monsters = [
    {"name": "Goblin", "image": "goblin.png"},
    {"name": "Skeleton", "image": "skeleton.png"},
    {"name": "Zombie", "image": "zombie.png"},
    {"name": "Dragon", "image": "dragon.png"}
]

# Randomly select a monster
monster_choice = random.choice(monsters)
m_name = monster_choice["name"]
monster_image = tk.PhotoImage(file=monster_choice["image"])
monster_image_resized = monster_image.subsample(2)  # Resize to 50% of original size
monster_label = tkinter.Label(root, image=monster_image_resized, bg='#fafbf8')
monster_label.place(x=750, y=120)

# Resizing player image
original_player_image = tk.PhotoImage(file="knight.png")
player_image = original_player_image.subsample(2)  # Resize to 50% of the original size
player_label = tkinter.Label(root, image=player_image, bg='#fafbf8')
player_label.place(x=100, y=320)

# Player and monster stats
p_name = "Albert"
p_health = 100
p_stamina = 100

m_health = 100

turn = 0
heal_turn_tracker = -4

# Functions for button commands
def disable_all_btns():
    fight_btn.config(state="disabled")
    run_btn.config(state="disabled")
    parry_btn.config(state="disabled")
    heal_btn.config(state="disabled")

def disable_heal_btn():
    heal_btn.config(state="disabled")

def enable_heal_btn():
    heal_btn.config(state="normal")

def p_attack():
    global m_health, p_health, turn
    turn += 1
    turns_lbl.config(text=turn)
    p_attack_dmg = random.randint(5, 12)
    m_attack_dmg = 0
    m_health -= p_attack_dmg
    if p_health > 0 and m_health > 0:
        m_attack_dmg = random.randint(10, 13)
        p_health -= m_attack_dmg
    else:
        action_label.config(text=f"You defeated the {m_name}!")
    action_label.config(text=f"You did {p_attack_dmg} damage to\n the {m_name}.\nThe monster attacked. He did \n{m_attack_dmg} damage to you")
    player_health_lbl.config(text=f"{p_health}")
    monster_health_lbl.config(text=f"{m_health}")
    if m_health <= 0:  
        m_health = 0
        monster_health_lbl.config(text=f"{m_health}")
        action_label.config(text=f"You defeated the {m_name}!")
        disable_all_btns()
        monster_label.config(state="disabled")
        return
    if p_health <= 0: 
        p_health = 0
        player_health_lbl.config(text=f"{p_health}")
        action_label.config(text=f"You died")
        disable_all_btns()
        player_label.config(state="disabled")
        return

def p_run():
    action_label.config(text="You have fled the fight.")
    disable_all_btns()

def p_heal():
    global p_health, turn, heal_turn_tracker, m_health
    if turn - heal_turn_tracker >= 4: 
        heal_turn_tracker = turn
        p_heal_amt = random.randint(8, 15)
        p_health += p_heal_amt
        player_health_lbl.config(text=f"{p_health}")
        action_label.config(text=f"You consumed the glass \nvial of red liquid and gained {p_heal_amt}")
        if p_health < 0:
            p_health = 0
        if m_health < 0:
            m_health = 0
        player_health_lbl.config(text=f"{p_health}")
        monster_health_lbl.config(text=f"{m_health}")
    else:
        action_label.config(text="You can only heal once 4 turns!")

def p_parry():
    global p_health, m_health, turn
    turn += 1
    m_attack_dmg = random.randint(10, 13)
    parry_m_attack_dmg = round(m_attack_dmg * 0.7, 0)
    parry_p_deflect_dmg = round(m_attack_dmg * 0.4, 0)
    p_health -= parry_m_attack_dmg
    m_health -= parry_p_deflect_dmg
    action_label.config(text=f"You took {parry_m_attack_dmg} and deflected \n{parry_p_deflect_dmg} damage")
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
    if p_health <= 0 and m_health <= 0:
        m_health = 0
        p_health = 0
        monster_health_lbl.config(text=f"{m_health}")
        player_health_lbl.config(text=f"{p_health}")
        action_label.config(text=f"Both of you died")
        return

# Player and monster names and health displayed
player_name_lbl = tkinter.Label(root, text=p_name, font=('', 40, 'bold'), bg='#fafbf8')
player_name_lbl.place(x=75, y=40)

player_health_lbl = tkinter.Label(root, text=f"{p_health}", font=('', 32, 'bold'), bg='#fafbf8')
player_health_lbl.place(x=280, y=133)

monster_name_lbl = tkinter.Label(root, text=m_name, font=('', 40, 'bold'), bg='#fafbf8')
monster_name_lbl.place(x=640, y=500)

monster_health_lbl = tkinter.Label(root, text=f"{m_health}", font=('', 32, 'bold'), bg='#fafbf8')
monster_health_lbl.place(x=800, y=580)

# Main action label
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

turns_lbl = tkinter.Label(root, text=0, bg='#fafbf8')
turns_lbl.pack()

root.mainloop()
