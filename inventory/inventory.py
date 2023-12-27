from stories import *
from player_inventory import *
from character_create import *
from car_create import *
from enemies import enemies


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
