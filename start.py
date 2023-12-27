import random
from stories import *
from player_inventory import *
from character_create import *
from car_create import *
from enemies import enemies
from inventory.inventory import check_car_inventory, modify_inventory, check_inventory, show_inventory
from combat.combat import start_car_combat, start_firearms_combat, start_close_combat, duel, car_race
from game_logic.game_logic import modify_prop, select_enemies, test_of_dexterity, test_of_luck_without_minus, test_of_luck, check_hp, d6, test_of_dexterity_diffrent, dex_compare
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


def run_game(current_story_key, player_health, player_dexterity, player_luck, player_car_armor, player_car_firepower):
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
                    print("\n Not enough " +
                          inv_chk_value_second + " available. \n")
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

        if not current_story_key in stories:

            if current_option.get("text") == "Duel!":
                duelWin = current_option.get("duel_win")
                duelLose = current_option.get("duel_lose")
                current_story_key = duel(player_dexterity, duelWin, duelLose)
                continue

            if current_option.get("text") == "Compare Dexterity":
                enemy_dex = current_option.get("enemydex")
                ifLow = current_option.get("iflow")
                ifHigh = current_option.get("ifhigh")
                current_story_key = dex_compare(
                    player_dexterity, enemy_dex, ifLow, ifHigh)
                continue

            if current_option.get("text") == "Compare your Dexterity":
                enemy_dex = current_option.get("enemydex")
                ifLow = current_option.get("iflow")
                ifHigh = current_option.get("ifhigh")
                current_story_key = test_of_dexterity_diffrent(
                    player_dexterity, enemy_dex, ifLow, ifHigh)
                continue

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
                current_story_key, player_health = start_close_combat(
                    selected_enemies, player_health, player_dexterity, inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value)
                continue

            if current_option.get("combat_type") == "firearms":
                enemy_names = current_option.get("enemy_name", "")
                temp_stat_mod_stat = current_option.get("temp_stat_mod_stat")
                temp_negative_mod_value = current_option.get(
                    "temp_negative_mod_value")
                selected_enemies = select_enemies(enemies, *enemy_names)
                current_story_key, player_health, player_dexterity = start_firearms_combat(
                    selected_enemies, player_health, player_dexterity, inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value)
                continue

            if current_option.get("combat_type") == "car":
                enemy_names = current_option.get("enemy_name", "")
                temp_stat_mod_stat = current_option.get("temp_stat_mod_stat")
                temp_negative_mod_value = current_option.get(
                    "temp_negative_mod_value")
                rounds_to_survive = current_option.get("rounds_to_survive")
                selected_enemies = select_enemies(enemies, *enemy_names)
                current_story_key, player_car_armor = start_car_combat(
                    selected_enemies, player_car_firepower, player_car_armor, car_inventory, current_story_key, temp_stat_mod_stat, temp_negative_mod_value, rounds_to_survive)
                continue

            if current_option.get("combat_type") == "luck":
                enemy_name = current_option.get("enemy_name", "")
                enemy = enemies.get(enemy_name)
                if enemy:
                    current_story_key, player_luck = test_of_luck(
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


if __name__ == "__main__":
    run_game(current_story_key, player_health, player_dexterity,
             player_luck, player_car_armor, player_car_firepower)
