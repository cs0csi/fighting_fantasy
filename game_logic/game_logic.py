import random
from stories import *
from player_inventory import *
from character_create import *
from car_create import *


def dex_compare(player_dexterity, enemy_dex, ifLow, ifHigh):
    if player_dexterity >= int(enemy_dex):
        print("The player has a higher value of dexterity.")
        return ifHigh
    else:
        print("The player has a lower dexterity value.")
        return ifLow


def test_of_dexterity_diffrent(player_dexterity, enemy_dex, ifLow, ifHigh):
    enemy_roll = (random.randint(1, 6) + int(enemy_dex))
    player_roll = (random.randint(1, 6) + player_dexterity)

    if player_roll >= enemy_roll:
        print("The player has a higher value of dexterity.")
        return ifHigh
    else:
        print("The player has a lower dexterity value.")
        return ifLow


def process_result(result, threshold, ifLow, ifHigh):
    if result <= threshold:
        print(f"The result is equal or smaller than {threshold}: {result}")
        return ifLow
    elif result > threshold:
        print(f"The result is bigger than {threshold}: {result}")
        return ifHigh


def d6(d6range, ifLow, ifHigh):
    d6result = random.randint(1, 6)

    if d6range == "d6-12-36":
        return process_result(d6result, 2, ifLow, ifHigh)
    elif d6range == "d6-13-46":
        return process_result(d6result, 3, ifLow, ifHigh)
    elif d6range == "d6-14-56":
        return process_result(d6result, 4, ifLow, ifHigh)
    elif d6range == "d6-15-6":
        return process_result(d6result, 5, ifLow, ifHigh)


def check_hp(player_health, hpLevel, hp_bigger, hp_lower):
    if player_health >= int(hpLevel):
        print(
            f"\nPlayer health is greater than or equal to {hpLevel}. Player health: {player_health} \n")
        return hp_bigger
    else:
        print(
            f"\nPlayer health is less than {hpLevel}. Player health: {player_health} \n")
        return hp_lower


def test_of_luck(player_luck, enemy, current_story_key):
    win_story_index = enemy.get("combat_data", {}).get("if_win", "")
    lose_story_index = enemy.get("combat_data", {}).get("if_lose", "")
    luck_score = random.randint(2, 12)
    print(f"Your luck score is {luck_score}")
    if luck_score <= player_luck:
        print("You got lucky!")
        player_luck -= 1
        current_story_key = win_story_index
        return current_story_key, player_luck
    else:
        print("No luck this time.")
        player_luck -= 1
        current_story_key = lose_story_index
        return current_story_key, player_luck


def test_of_luck_without_minus(player_luck, enemy, current_story_key):
    win_story_index = enemy.get("combat_data", {}).get("if_win", "")
    lose_story_index = enemy.get("combat_data", {}).get("if_lose", "")
    luck_score = random.randint(2, 12)
    print(f"Your luck score is {luck_score}")
    if luck_score <= player_luck:
        print("You got lucky!")
        current_story_key = win_story_index
        return current_story_key
    else:
        print("No luck this time.")
        current_story_key = lose_story_index
        return current_story_key


def test_of_dexterity(player_dexterity, enemy, current_story_key):
    win_story_index = enemy.get("combat_data", {}).get("if_win", "")
    lose_story_index = enemy.get("combat_data", {}).get("if_lose", "")
    dexterity_score = random.randint(2, 12)
    print(f"Your dexterity score is {dexterity_score}")
    if dexterity_score >= player_dexterity:
        print("Dexterity test was success!")
        current_story_key = win_story_index
        return current_story_key
    else:
        print("Dexterity test failed!")
        current_story_key = lose_story_index
        return current_story_key


def select_enemies(enemies, *enemy_names):
    selected_enemies = []
    for enemy_names_str in enemy_names:
        enemy_name_list = enemy_names_str.split(',')
        for enemy_name in enemy_name_list:
            enemy = enemies.get(enemy_name)
            if enemy:
                selected_enemies.append(enemy)
    return selected_enemies


def modify_prop(prop_modification, prop_value):
    global player_health, player_dexterity, player_luck, player_car_armor, player_car_firepower

    if prop_modification == 'player_health':
        if prop_value.startswith('+'):
            player_health += int(prop_value[1:])
        elif prop_value.startswith('-'):
            player_health -= int(prop_value[1:])
    elif prop_modification == 'player_dexterity':
        if prop_value.startswith('+'):
            player_dexterity += int(prop_value[1:])
        elif prop_value.startswith('-'):
            player_dexterity -= int(prop_value[1:])
    elif prop_modification == 'player_luck':
        if prop_value.startswith('+'):
            player_luck += int(prop_value[1:])
        elif prop_value.startswith('-'):
            player_luck -= int(prop_value[1:])
    elif prop_modification == 'player_car_armor':
        if prop_value.startswith('+'):
            player_car_armor += int(prop_value[1:])
        elif prop_value.startswith('-'):
            player_car_armor -= int(prop_value[1:])
            if player_car_armor <= 0:
                current_story_key = 'game_over'
                print('game over')
                return current_story_key
    elif prop_modification == 'player_car_firepower':
        if prop_value.startswith('+'):
            player_car_firepower += int(prop_value[1:])
        elif prop_value.startswith('-'):
            player_car_firepower -= int(prop_value[1:])

    print(f"The {prop_modification} is now {eval(prop_modification)}")
