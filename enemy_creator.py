# Initialize the dictionary
enemies = {}

while True:
    enemy_name = input("Enter enemy name (or type 'exit' to quit): ")
    if enemy_name.lower() == 'exit':
        break

    # Gather enemy attributes
    enemy_data = {
        "name": enemy_name,
        "car_firepower": int(input("Enter car firepower: ")),
        "car_armor": int(input("Enter car armor: ")),
        "combat_data": {
            "if_win": input("Enter 'if_win' data: "),
            "if_lose": "game_over"
        }
    }

    # Add enemy to the dictionary
    enemies[enemy_name] = enemy_data

# Write the dictionary to a Python file
with open('enemies3.py', 'w') as file:
    file.write("enemies = " + str(enemies))

print("Data saved to enemies.py.")
