import random
import time
from inventory.inventory import check_car_inventory
from player_inventory import inventory, car_inventory, fuel_level
from stories import enemies, stories
from player_inventory import fuel_level, car_inventory, inventory
from character_create import create_character
from car_create import create_car
from enemies import enemies

combat_wait_time = 2.4


def duel(player_dexterity, duelWin, duelLose):
    roll = (random.randint(1, 6)) + 7
    print(f"Rolled: {roll}")
    if roll >= player_dexterity:
        print("The player win the Duel")
        return duelWin
    if roll < player_dexterity:
        print("Player lost the Duel")
        return duelLose


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
            time.sleep(combat_wait_time)
            return raceLose
        time.sleep(combat_wait_time)

        player_roll = random.randint(1, 6)
        if check_car_inventory(player_inventory, "Tuning", 1):
            player_roll += 1
        player_score += player_roll

        print(f"Player car rolled: {player_roll}, Total score: {player_score}")

        if player_score >= winning_score:
            print("Player car wins!")
            time.sleep(combat_wait_time)
            return raceWin
        time.sleep(combat_wait_time)


def start_close_combat(selected_enemies, player_health, player_dexterity, inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value):
    """
    Function to handle close combat system
    """
    if temp_stat_mod_stat == "player_dexterity":
        player_dexterity = player_dexterity - int(temp_negative_mod_value)
        print(f"For the battle the player dexterity is: {player_dexterity}")

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
                    f"{index + 1}: {enemy['name']}'s Health: {enemy['health']}, Dexterity: {enemy['dexterity']}")
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
            if enemy_weapon_damage == 2:
                player_weapon_damage = 2
            else:
                player_weapon_damage = 1
            player_damage = max(player_weapon_damage, 1)
            print(f"You deal {player_damage} damage to the {
                  target_enemy['name']}!")
            target_enemy['health'] -= player_damage
            time.sleep(combat_wait_time)
        elif enemy_attack_power > player_attack_power:
            if enemy_weapon_damage is None:
                enemy_weapon_damage = 1
            for item in enemy.get("inventory", []):
                if item["type"] == "weapon":
                    enemy_weapon_damage = item.get("damage", 1)
                    break
            enemy_damage = max(enemy_weapon_damage, 1)
            print(f"The {target_enemy['name']} deals {
                  enemy_damage} damage to you!")
            player_health -= enemy_damage
            time.sleep(combat_wait_time)
        else:
            print("Both combatants attack with equal power!")
            time.sleep(combat_wait_time)

 # Check if any selected_enemies have been defeated
        defeated_enemies = []
        for enemy in selected_enemies:
            if enemy['health'] <= 0:
                defeated_enemies.append(enemy)
                print(f"You defeated the {enemy['name']}!")
                time.sleep(combat_wait_time)
        for defeated_enemy in defeated_enemies:
            selected_enemies.remove(defeated_enemy)

        if len(selected_enemies) == 0:
            print("Congratulations! You defeated all enemies!")

            if temp_stat_mod_stat == "player_dexterity":
                player_dexterity = player_dexterity + \
                    int(temp_negative_mod_value)
                print(f"Player dexterity is again: {player_dexterity}")
            current_story_key = win_story_index
            return current_story_key, player_health

        elif player_health <= 0:
            if temp_stat_mod_stat == "player_dexterity":
                player_dexterity = player_dexterity + \
                    int(temp_negative_mod_value)
            print(f"You were defeated by the {enemy_name}. Game over!")
            current_story_key = lose_story_index
            return current_story_key, player_health


def start_firearms_combat(selected_enemies, player_health, player_dexterity, inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value):

    if temp_stat_mod_stat == "player_dexterity":
        player_dexterity = player_dexterity - int(temp_negative_mod_value)
        print(f"For the battle the player dexterity is: {player_dexterity}")
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
        time.sleep(combat_wait_time)
        if player_attack_power > enemy_attack_power:
            player_damage = ranged_weapon.get("damage", 1)
            print(
                f"You hit the {target_enemy['name']} for {player_damage} damage!")
            target_enemy['health'] -= player_damage
            time.sleep(combat_wait_time)
        elif enemy_attack_power > player_attack_power:
            enemy_damage = max(enemy_weapon_damage, 1)
            print(
                f"The {enemy_name} fires and hits you for {enemy_damage} damage!")
            player_health -= enemy_damage
            print(f"your dexterity was {player_dexterity}")
            player_dexterity -= 1
            print(f"your dexterity is now {player_dexterity}")
        else:
            print("Both combatants aim with equal accuracy!")
            time.sleep(combat_wait_time)

        # Check if any selected_enemies have been defeated
        defeated_enemies = []
        for enemy in selected_enemies:
            if enemy['health'] <= 0:
                defeated_enemies.append(enemy)
                print(f"You defeated the {enemy['name']}!")
                time.sleep(combat_wait_time)
        for defeated_enemy in defeated_enemies:
            selected_enemies.remove(defeated_enemy)

        if len(selected_enemies) == 0:
            print("Congratulations! You defeated all enemies!")
            print(f"your dexterity is now {player_dexterity}")
            if temp_stat_mod_stat == "player_dexterity":
                player_dexterity = player_dexterity + \
                    int(temp_negative_mod_value)
                print(f"Player dextirity is again: {player_dexterity}")
            current_story_key = win_story_index
            return current_story_key, player_health, player_dexterity

        elif player_health <= 0 or player_dexterity <= 0:
            if temp_stat_mod_stat == "player_dexterity":
                player_dexterity = player_dexterity + \
                    int(temp_negative_mod_value)
            print(f"You were defeated by the {enemy_name}. Game over!")
            current_story_key = lose_story_index
            return current_story_key, player_health, player_dexterity


def start_car_combat(selected_enemies, player_car_firepower, player_car_armor, car_inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value, rounds_to_survive):

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

    rounds_survived = 0

    # Check if rounds_to_survive is provided and not empty
    if rounds_to_survive is not None and rounds_to_survive.strip():
        rounds_to_survive = int(rounds_to_survive)
    else:
        rounds_to_survive = 0  # Set a default value if not provided
    while player_car_armor > 0 and enemy_car_armor > 0 and (rounds_to_survive == 0 or rounds_survived < rounds_to_survive):
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

            rounds_survived += 1

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
                    time.sleep(combat_wait_time)

            if rocket_used == False:
                if player_attack_power > enemy_attack_power:
                    player_damage = random.randint(1, 6)
                    print(
                        f"You deal {player_damage} damage to the {target_enemy['name']}!")
                    target_enemy['car_armor'] -= player_damage
                    time.sleep(combat_wait_time)
                elif enemy_attack_power > player_attack_power:
                    enemy_damage = random.randint(1, 6)
                    print(
                        f"The {target_enemy['name']} deals {enemy_damage} damage to your car!")
                    player_car_armor -= enemy_damage
                else:
                    print("Both cars attack with equal power!")
                    time.sleep(combat_wait_time)

            for enemy in selected_enemies:
                if enemy['car_armor'] <= 0:
                    defeated_enemies.append(enemy)
                    print(f"You defeated the {target_enemy['name']}!")
                    time.sleep(combat_wait_time)
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
                return current_story_key, player_car_armor

            elif player_car_armor <= 0:
                print(f"You were defeated by the {
                    target_enemy['name']}. Game over! \n")
                current_story_key = lose_story_index
                return current_story_key, player_car_armor

            elif (rounds_to_survive != 0) and (rounds_survived >= rounds_to_survive):
                print(f"Congratulations! You survived {
                    rounds_to_survive} rounds!")
                current_story_key = win_story_index
                return current_story_key, player_car_armor
