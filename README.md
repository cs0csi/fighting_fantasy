# Fighting Fantasy

## Overview

**Fighting Fantasy** is a command-line game that combines elements of role-playing, strategy, and chance. Create your character, assemble your car, and navigate through a series of events where your choices shape the outcome of the story.


## Table of Contents

- [Getting Started](#getting-started)
- [Game Features](#game-features)
- [License](#license)

## Getting Started

Describe how someone can get a copy of your game and run it locally. Include any setup steps, dependencies, or installation instructions.

```bash
git clone https://github.com/cs0csi/fighting_fantasy
cd your-game
python start.py
```

## Game Features

1. **Character and Car Creation:**
   - At the start of the game, the player creates a character and a car with specified attributes such as health, dexterity, luck, armor, and firepower.

2. **Randomized Events:**
   - The game includes various events that involve random outcomes. These events are determined by rolling a six-sided die (D6) or using variations of it (e.g., D6-12-36).

3. **Inventory Management:**
   - Players can manage their inventory, which includes items such as weapons and other items. The `modify_inventory` function allows for adding, removing, or resetting quantities of items in the player's inventory.

4. **Combat Systems:**
   - The game features different combat systems, including close combat, firearms combat, and car combat.
   - Close Combat: Players engage in battles with enemies. The outcome is determined by comparing attack powers based on dexterity and weapon damage.
   - Firearms Combat: Similar to close combat but incorporates the use of ranged weapons. Players choose a ranged weapon from their inventory to engage enemies.
   - Car Combat: Players battle enemies using cars, considering car firepower, armor, and the option to use special items like rockets.

5. **Test of Luck and Dexterity:**
   - There are events that test the player's luck or dexterity. The player's luck or dexterity score is compared to a random score, and the outcome affects the direction of the story.

6. **Story Progression:**
   - The game is driven by a series of stories, and the player's choices in events determine the progression of the story.
   - Some story options may include property modifications, such as altering the player's health, dexterity, luck, car firepower, or car armor.

7. **Checking Inventory and Stats:**
   - Players can check their current inventory and stats at any time during the game.
   - The inventory includes information about weapons, items, and other relevant game elements.

8. **Game Over and Victory:**
   - The game can end in either victory or defeat. A "game over" scenario occurs if the player's car armor reaches zero. The "WIN" scenario indicates the player has successfully completed the game.

## License

This project is licensed under the [GNU Affero General Public License (AGPL)](LICENSE).

**Important:** If you intend to use, modify, or distribute this code, you must adhere to the terms of the AGPL. Any derivative work or modifications must also be released under the same license. For more details, refer to the [LICENSE](LICENSE) file.

For any specific inquiries or approval requests, please contact at cs0csi@proton.me.

