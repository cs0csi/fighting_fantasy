import random


def create_character():
    dexterity = random.randint(1, 6) + 6
    health = random.randint(2, 12) + 24
    luck = random.randint(1, 6) + 0

    character = {
        "dexterity": dexterity,
        "health": health,
        "luck": luck
    }

    return character
