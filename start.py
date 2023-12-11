import random
from stories import *
from player_inventory import *
from character_create import *
from car_create import *
from enemies import enemies
import time
import os


current_story_key = "1"

os.system('cls')

character = create_character()
car = create_car()


player_health = character["health"]
player_dexterity = character["dexterity"]
player_luck = character["luck"]

player_car_armor = car["armor"]
player_car_firepower = car["firepower"]


def car_race(player_inventory, raceWin, raceLose):
    player_score = 0
    enemy_score = 0
    winning_score = 24

    print("Let the car race begin!")

    while player_score < winning_score and enemy_score < winning_score:
        enemy_roll = random.randint(1, 6)
        enemy_score += enemy_roll
        print(f"Enemy car rolled: {enemy_roll}, Total score: {enemy_score}")
        if enemy_score >= winning_score:
            print("Enemy car wins!")
            time.sleep(2.4)
            return raceLose
        time.sleep(2.4)

        player_roll = random.randint(1, 6)
        if check_car_inventory(player_inventory, "Tuning", 1):
            player_roll += 1
        player_score += player_roll

        print(f"Player car rolled: {player_roll}, Total score: {player_score}")

        if player_score >= winning_score:
            print("Player car wins!")
            time.sleep(2.4)
            return raceWin
        time.sleep(2.4)


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
        return current_story_key
    else:
        print("No luck this time.")
        player_luck -= 1
        current_story_key = lose_story_index
        return current_story_key


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


def start_close_combat(selected_enemies, player_health, player_dexterity, inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value):
    """
    Function to handle close combat system
    """
    if temp_stat_mod_stat == "player_dexterity":
        player_dexterity = player_dexterity - int(temp_negative_mod_value)
        print(f"For the battle the player dextirity is: {player_dexterity}")

    for enemy in selected_enemies:
        enemy_name = enemy["name"]
        enemy_health = enemy["health"]
        enemy_dexterity = enemy["dexterity"]
        enemy_weapon_damage = enemy.get("weapon_damage", 1)
        win_story_index = enemy.get("combat_data", {}).get("if_win", "")
        lose_story_index = enemy.get("combat_data", {}).get("if_lose", "")

    while player_health > 0 and enemy_health > 0:
        print(
            f"Your health: {player_health}")
        player_attack_power = random.randint(2, 12) + player_dexterity
        enemy_attack_power = random.randint(2, 12) + enemy_dexterity
        # Player selects which enemy to attack
        target_enemy = None
        while not target_enemy:
            for index, enemy in enumerate(selected_enemies):
                print(
                    f"{index + 1}: {enemy['name']}s Health: {enemy['health']}, Dexterity: {enemy['dexterity']}")
            if len(selected_enemies) == 1:
                target_enemy = selected_enemies[0]
            else:
                target_enemy_index = input(
                    f"Which enemy do you want to attack? Enter a number from 1 to {len(selected_enemies)}: ")
                try:
                    target_enemy_index = int(target_enemy_index)
                    if target_enemy_index > 0 and target_enemy_index <= len(selected_enemies):
                        target_enemy = selected_enemies[target_enemy_index-1]
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Invalid selection. Please try again.")
        if player_attack_power > enemy_attack_power:
            player_weapon_damage = 1
            for item in inventory:
                if item["type"] == "weapon":
                    player_weapon_damage = item.get("damage", 1)
                    break
            player_damage = max(player_weapon_damage, 1)
            print(f"You deal {player_damage} damage to the {
                  target_enemy['name']}!")
            target_enemy['health'] -= player_damage
            time.sleep(2.4)
        elif enemy_attack_power > player_attack_power:
            enemy_weapon_damage = 1
            for item in enemy.get("inventory", []):
                if item["type"] == "weapon":
                    enemy_weapon_damage = item.get("damage", 1)
                    break
            enemy_damage = max(enemy_weapon_damage, 1)
            print(f"The {target_enemy['name']} deals {
                  enemy_damage} damage to you!")
            player_health -= enemy_damage
        else:
            print("Both combatants attack with equal power!")
            time.sleep(2.4)

 # Check if any selected_enemies have been defeated
        defeated_enemies = []
        for enemy in selected_enemies:
            if enemy['health'] <= 0:
                defeated_enemies.append(enemy)
                print(f"You defeated the {enemy['name']}!")
                time.sleep(2.4)
        for defeated_enemy in defeated_enemies:
            selected_enemies.remove(defeated_enemy)

        if len(selected_enemies) == 0:
            print("Congratulations! You defeated all enemies!")

            if temp_stat_mod_stat == "player_dexterity":
                player_dexterity = player_dexterity + \
                    int(temp_negative_mod_value)
                print(f"Player dextirity is again: {player_dexterity}")
            current_story_key = win_story_index
            return current_story_key

        elif player_health <= 0:
            if temp_stat_mod_stat == "player_dexterity":
                player_dexterity = player_dexterity + \
                    int(temp_negative_mod_value)
            print(f"You were defeated by the {enemy_name}. Game over!")
            current_story_key = lose_story_index
            return current_story_key


def start_firearms_combat(selected_enemies, player_health, player_dexterity, inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value):

    if temp_stat_mod_stat == "player_dexterity":
        player_dexterity = player_dexterity - int(temp_negative_mod_value)
        print(f"For the battle the player dextirity is: {player_dexterity}")

    for enemy in selected_enemies:
        enemy_name = enemy["name"]
        enemy_health = enemy["health"]
        enemy_dexterity = enemy["dexterity"]
        enemy_weapon_damage = enemy.get("weapon_damage", 1)
        win_story_index = enemy.get("combat_data", {}).get("if_win", "")
        lose_story_index = enemy.get("combat_data", {}).get("if_lose", "")
   # Determine ranged weapon
    ranged_weapons = []
    for item in inventory:
        if item["type"] == "ranged_weapon":
            ranged_weapons.append(item)
    if len(ranged_weapons) == 0:
        print("You have no ranged weapons. You cannot engage in firearms combat.")
        return
    elif len(ranged_weapons) == 1:
        ranged_weapon = ranged_weapons[0]

    else:
        print("Choose a ranged weapon from your inventory:")
        for i, weapon in enumerate(ranged_weapons):
            print(
                f"{i+1}. {weapon['name']} ({weapon.get('damage', 1)} damage)")
        weapon_choice = None
        while weapon_choice is None:
            try:
                weapon_choice = int(input("> "))
                if weapon_choice < 1 or weapon_choice > len(ranged_weapons):
                    print("Invalid choice.")
                    weapon_choice = None
            except ValueError:
                print("Invalid input.")
                weapon_choice = None
        ranged_weapon = ranged_weapons[weapon_choice-1]

        print(f"You pull out your {ranged_weapon['name']}!")

    while player_health > 0 and enemy_health > 0:
        print(f"Your health: {player_health}")
        player_attack_power = random.randint(2, 12) + player_dexterity
        enemy_attack_power = random.randint(2, 12) + enemy_dexterity
        # Player selects which enemy to attack
        target_enemy = None
        while not target_enemy:
            for index, enemy in enumerate(selected_enemies):
                print(
                    f"{index + 1}: {enemy['name']}s Health: {enemy['health']}, Dexterity: {enemy['dexterity']}")
            if len(selected_enemies) == 1:
                target_enemy = selected_enemies[0]
            else:
                target_enemy_index = input(
                    f"Which enemy do you want to attack? Enter a number from 1 to {len(selected_enemies)}: ")
                try:
                    target_enemy_index = int(target_enemy_index)
                    if target_enemy_index > 0 and target_enemy_index <= len(selected_enemies):
                        target_enemy = selected_enemies[target_enemy_index-1]
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Invalid selection. Please try again.")
        time.sleep(2.4)
        if player_attack_power > enemy_attack_power:
            player_damage = ranged_weapon.get("damage", 1)
            print(
                f"You hit the {target_enemy['name']} for {player_damage} damage!")
            target_enemy['health'] -= player_damage
            time.sleep(2.4)
        elif enemy_attack_power > player_attack_power:
            enemy_damage = max(enemy_weapon_damage, 1)
            print(
                f"The {enemy_name} fires and hits you for {enemy_damage} damage!")
            player_health -= enemy_damage
        else:
            print("Both combatants aim with equal accuracy!")
            time.sleep(2.4)

        # Check if any selected_enemies have been defeated
        defeated_enemies = []
        for enemy in selected_enemies:
            if enemy['health'] <= 0:
                defeated_enemies.append(enemy)
                print(f"You defeated the {enemy['name']}!")
                time.sleep(2.4)
        for defeated_enemy in defeated_enemies:
            selected_enemies.remove(defeated_enemy)

        if len(selected_enemies) == 0:
            print("Congratulations! You defeated all enemies!")

            if temp_stat_mod_stat == "player_dexterity":
                player_dexterity = player_dexterity + \
                    int(temp_negative_mod_value)
                print(f"Player dextirity is again: {player_dexterity}")
            current_story_key = win_story_index
            return current_story_key

        elif player_health <= 0:
            if temp_stat_mod_stat == "player_dexterity":
                player_dexterity = player_dexterity + \
                    int(temp_negative_mod_value)
            print(f"You were defeated by the {enemy_name}. Game over!")
            current_story_key = lose_story_index
            return current_story_key


def start_car_combat(selected_enemies, player_car_firepower, player_car_armor, car_inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value):

    if temp_stat_mod_stat == "player_car_firepower":
        player_car_firepower = player_car_firepower - \
            int(temp_negative_mod_value)
        print(f"For the battle the {temp_stat_mod_stat} is: {
              player_car_firepower}")

    for enemy in selected_enemies:
        enemy_car_firepower = enemy["car_firepower"]
        enemy_car_armor = enemy["car_armor"]
        win_story_index = enemy.get("combat_data", {}).get("if_win", "")
        lose_story_index = enemy.get("combat_data", {}).get("if_lose", "")

    while player_car_armor > 0 and enemy_car_armor > 0:
        defeated_enemies = []

   # Player selects which enemy to attack
        target_enemy = None
        while not target_enemy:
            print(f"Your armor: {player_car_armor}")
            for index, enemy in enumerate(selected_enemies):
                print(
                    f"{index + 1}: {enemy['name']} Firepower: {enemy['car_firepower']}, Health: {enemy['car_armor']}")
            if len(selected_enemies) == 1:
                target_enemy = selected_enemies[0]
            else:
                target_enemy_index = input(
                    f"Which enemy do you want to attack? Enter a number from 1 to {len(selected_enemies)}: ")
                try:
                    target_enemy_index = int(target_enemy_index)
                    if target_enemy_index > 0 and target_enemy_index <= len(selected_enemies):
                        target_enemy = selected_enemies[target_enemy_index-1]
                    else:
                        print("Invalid selection. Please try again.")
                except ValueError:
                    print("Invalid selection. Please try again.")

            player_attack_power = random.randint(2, 12) + player_car_firepower
            enemy_attack_power = random.randint(2, 12) + enemy_car_firepower

            rocket_used = False
            rocket_index = None
            for j, item in enumerate(car_inventory):
                if item["name"] == "rocket":
                    rocket_index = j
                    break

            if rocket_index is not None and car_inventory[rocket_index]["quantity"] > 0:
                print(
                    "You have a rocket! Press 'r' to fire the rocket or any other key to skip.")
                choice = input().lower()
                if choice == 'r':
                    print("You fire the rocket and defeat the enemy!")
                    car_inventory[rocket_index]["quantity"] -= 1
                    print("You used a rocket and there are",
                          car_inventory[rocket_index]["quantity"], "rockets left in your inventory.")
                    target_enemy['car_armor'] = 0
                    rocket_used = True
                    time.sleep(2.4)

            if rocket_used == False:
                if player_attack_power > enemy_attack_power:
                    player_damage = random.randint(1, 6)
                    print(
                        f"You deal {player_damage} damage to the {target_enemy['name']}!")
                    target_enemy['car_armor'] -= player_damage
                    time.sleep(2.4)
                elif enemy_attack_power > player_attack_power:
                    enemy_damage = random.randint(1, 6)
                    print(
                        f"The {target_enemy['name']} deals {enemy_damage} damage to your car!")
                    player_car_armor -= enemy_damage
                else:
                    print("Both cars attack with equal power!")
                    time.sleep(2.4)

            for enemy in selected_enemies:
                if enemy['car_armor'] <= 0:
                    defeated_enemies.append(enemy)
                    print(f"You defeated the {target_enemy['name']}!")
                    time.sleep(2.4)
            for defeated_enemy in defeated_enemies:
                selected_enemies.remove(defeated_enemy)

            if len(selected_enemies) == 0:
                print("Congratulations! You defeated all enemies! \n")

                if temp_stat_mod_stat == "player_car_firepower":
                    player_car_firepower = player_car_firepower + \
                        int(temp_negative_mod_value)
                    print(f"The {temp_stat_mod_stat} is again: {
                          player_car_firepower}")

                current_story_key = win_story_index
                return current_story_key

            elif player_car_armor <= 0:
                print(f"You were defeated by the {
                      target_enemy['name']}. Game over! \n")
                current_story_key = lose_story_index
                return current_story_key


def modify_inventory(inventory, item_name, action, quantity, item_type):
    def find_item(inventory, item_name):
        for item in inventory:
            if item["name"] == item_name:
                return item
        return None

    def update_quantity(item, action, quantity):
        current_quantity = int(item["quantity"])
        if action == "add":
            item["quantity"] = str(current_quantity + int(quantity))
        elif action == "remove":
            new_quantity = max(0, current_quantity - int(quantity))
            item["quantity"] = str(new_quantity)
        elif action == "reset":
            item["quantity"] = '0'

    item = find_item(inventory, item_name)
    if not item:
        inventory.append(
            {"name": item_name, "quantity": '0', "type": item_type})
        item = find_item(inventory, item_name)

    update_quantity(item, action, quantity)


def check_inventory(inventory, item_name, quantity):
    for item in inventory:
        if item["name"] == item_name:
            if quantity is not None:
                if item["quantity"] >= int(quantity):
                    return True
                else:
                    return False
    return False


def check_car_inventory(car_inventory, item_name, quantity):
    for item in car_inventory:
        if item["name"] == item_name:
            if quantity is not None:
                if item["quantity"] >= int(quantity):
                    return True
                else:
                    return False
    return False


def select_enemies(enemies, *enemy_names):
    selected_enemies = []
    for enemy_name in enemy_names:
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


while True:

    current_story = stories[current_story_key]
    print(current_story["text"])
    if current_story_key == "game_over":
        exit()
    if current_story_key == "WIN":
        exit()
    if "property_modification" in current_story:
        prop_modification = current_story.get("property_modification")
        prop_value = current_story.get("modification_value")
        if prop_value == "-D6":
            d6 = random.randint(1, 6)
            prop_value = prop_value[0] + str(d6)
        if prop_value == "-D6+2":
            d6p2 = random.randint(3, 8)
            prop_value = prop_value[0] + str(d6p2)
        if prop_value == "-2D6":
            twod6 = random.randint(2, 12)
            prop_value = prop_value[0] + str(twod6)
        modify_prop(prop_modification, prop_value)
    if "st_modify_inventory" in current_story:
        if not current_story.get('inventory_modified', False):
            current_story['inventory_modified'] = True
            item_modifiers = current_story.get('st_modify_inventory', [])

            for item_modifier in item_modifiers:
                item_name = item_modifier['item_name']
                action = item_modifier['action']
                quantity = item_modifier.get('quantity')
                item_type = item_modifier['item_type']
                inv_type = item_modifier['inv_type']

                if inv_type == "player_inv":
                    modify_inventory(inventory, item_name,
                                     action, quantity, item_type)
                elif inv_type == "car_inv":
                    modify_inventory(car_inventory, item_name,
                                     action, quantity, item_type)

    for i, option in enumerate(current_story["options"]):
        print(f"{i + 1}. {option['text']}")
    print(f"{len(current_story['options'])+1}. Check inventory")
    print(f"{len(current_story['options'])+2}. Check stats")
    choice = input("Enter choice number: ")
    if choice == str(len(current_story['options'])+1):
        show_inventory(inventory, car_inventory, fuel_level)
        continue
    if choice == str(len(current_story['options'])+2):
        print(f"PLAYER STATS")
        print(f"Health: {player_health}")
        print(f"Dexterity: {player_dexterity}")
        print(f"Luck: {player_luck}")
        print(f"CAR STATS")
        print(f"Car Armor: {player_car_armor}")
        print(f"Car Firepower: {player_car_firepower}")

        continue
    if not choice.isdigit() or int(choice) not in range(1, len(current_story["options"]) + 1):
        print("Invalid choice. Please try again.")
        continue
    current_option = current_story["options"][int(choice) - 1]

    # Inv check before choose

    dontGoTo = False
    contain = False
    contain_second = None
    if current_option.get("inv_chk"):
        inv_chk_value = current_option.get("inv_chk")
        inv_amount = current_option.get("amount")
        if (check_inventory(inventory, inv_chk_value, inv_amount)) or (check_car_inventory(car_inventory, inv_chk_value, inv_amount)):
            contain = True
        else:
            print("\n Not enough " + inv_chk_value + " available. \n")
            dontGoTo = True
            contain = False
        if current_option.get("inv_second"):
            inv_chk_value_second = current_option.get("inv_second")
            inv_amount_second = current_option.get("amount_second")
            if (check_inventory(inventory, inv_chk_value_second, inv_amount_second)) or (check_car_inventory(car_inventory, inv_chk_value_second, inv_amount_second)):
                contain_second = True
            else:
                print("\n Not enough " + inv_chk_value_second + " available. \n")
                dontGoTo = True
                contain_second = False
    else:
        if dontGoTo:
            current_story_key = stories[current_story_key]
        else:
            current_story_key = current_option.get("goto")

    if contain_second is not None:
        if contain and contain_second:
            current_story_key = current_option.get("goto")
        else:
            dontGoTo = True
    else:
        if contain_second is None:
            if contain:
                current_story_key = current_option.get("goto")
        else:
            dontGoTo = True

    # property modification

    if current_option.get("property_modification"):
        prop_modification = current_option.get("property_modification")
        prop_value = current_option.get("modification_value")
        modify_prop(prop_modification, prop_value)
    else:
        if dontGoTo == False:

            current_story_key = current_option.get("goto")

    if not current_story_key in stories:

        if current_option.get("text") == "Start Race!":
            raceWin = current_option.get("race_win")
            raceLose = current_option.get("race_lose")
            current_story_key = car_race(car_inventory, raceWin, raceLose)
            continue

        if current_option.get("text") == "Check HP":
            hpLevel = current_option.get("hp_level")
            hp_bigger = current_option.get("hp_bigger")
            hp_lower = current_option.get("hp_lower")
            current_story_key = check_hp(
                player_health, hpLevel, hp_bigger, hp_lower)
            continue

        if current_option.get("text") == "Roll a D6 dice":
            d6range = current_option.get("d6")
            ifLow = current_option.get("iflow")
            ifHigh = current_option.get("ifhigh")
            current_story_key = d6(d6range, ifLow, ifHigh)
            continue

        if current_option.get("combat_type") == "close":
            enemy_names = current_option.get("enemy_name", "")
            temp_stat_mod_stat = current_option.get("temp_stat_mod_stat")
            temp_negative_mod_value = current_option.get(
                "temp_negative_mod_value")
            selected_enemies = select_enemies(enemies, *enemy_names)
            current_story_key = start_close_combat(
                selected_enemies, player_health, player_dexterity, inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value)
            continue

        if current_option.get("combat_type") == "firearms":
            enemy_names = current_option.get("enemy_name", "")
            temp_stat_mod_stat = current_option.get("temp_stat_mod_stat")
            temp_negative_mod_value = current_option.get(
                "temp_negative_mod_value")
            selected_enemies = select_enemies(enemies, *enemy_names)
            current_story_key = start_firearms_combat(
                selected_enemies, player_health, player_dexterity, inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value)
            continue

        if current_option.get("combat_type") == "car":
            enemy_names = current_option.get("enemy_name", "")
            temp_stat_mod_stat = current_option.get("temp_stat_mod_stat")
            temp_negative_mod_value = current_option.get(
                "temp_negative_mod_value")
            selected_enemies = select_enemies(enemies, *enemy_names)
            current_story_key = start_car_combat(
                selected_enemies, player_car_firepower, player_car_armor, car_inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value)
            continue

        if current_option.get("combat_type") == "luck":
            enemy_name = current_option.get("enemy_name", "")
            enemy = enemies.get(enemy_name)
            if enemy:
                current_story_key = test_of_luck(
                    player_luck, enemy, current_story_key)
            continue

        if current_option.get("combat_type") == "luck_without_minus":
            enemy_name = current_option.get("enemy_name", "")
            enemy = enemies.get(enemy_name)
            if enemy:
                current_story_key = test_of_luck_without_minus(
                    player_luck, enemy, current_story_key)
            continue

        if current_option.get("combat_type") == "dext":
            enemy_name = current_option.get("enemy_name", "")
            enemy = enemies.get(enemy_name)
            if enemy:
                current_story_key = test_of_dexterity(
                    player_dexterity, enemy, current_story_key)
            continue
        else:
            print("Invalid story key. Please try again.")
