# player inventory

inventory = [{"name": "Pistol", "quantity": 1, "type": "ranged_weapon", "damage": 18},
             {"name": "Uzi", "quantity": 1, "type": "ranged_weapon", "damage": 5},
             {"name": "Medicine package", "quantity": 11, "type": "consumable"},
             {"name": "Kés", "quantity": 1, "type": "weapon", "damage": 20},
             {"name": "Hitel", "quantity": 2000, "type": "money"}
             ]


###################### CAR #

car_inventory = [{"name": "rocket", "quantity": 4, "type": "weapon"},
                 {"name": "Iron Nail Box", "quantity": 3, "type": "item"},
                 {"name": "Oil Tank", "quantity": 2, "type": "item"},
                 {"name": "Tuning", "quantity": 1, "type": "item"}
                 ]


fuel_level = 100


# Function to display the contents of inventory
def show_inventory(player_inventory, car_inventory, fuel_level):
    print("Player Inventory:")
    print("{:<15} {:<10} {:<10} {:<10}".format(
        "Name", "Quantity", "Type", "Damage"))
    for item in player_inventory:
        name = item["name"]
        quantity = item["quantity"]
        item_type = item["type"]
        damage = item.get("damage", "")
        print("{:<15} {:<10} {:<10} {:<10}".format(
            name, quantity, item_type, damage))

    print("\nCar Inventory:")
    print("{:<15} {:<10} {:<10} {:<10}".format(
        "Name", "Quantity", "Type", "Attack Power"))
    for item in car_inventory:
        name = item["name"]
        quantity = item["quantity"]
        item_type = item["type"]
        attack_power = item.get("attack_power", "")
        print("{:<15} {:<10} {:<10} {:<10}".format(
            name, quantity, item_type, attack_power))

    print("\nFuel Level: {} gallons".format(fuel_level))
