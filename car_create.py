import random
def create_car():
    """
    Function to create a car object with randomly generated firepower and armor.
    """
    firepower = random.randint(1, 6) + 6
    armor = random.randint(2, 12) + 24
    car = {
        "firepower": firepower,
        "armor": armor
    }

    return car
