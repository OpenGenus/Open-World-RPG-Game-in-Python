# Open-World-RPG-Game-in-Python

A text-based open world RPG game in Python! Create your own character, explore the various regions, and level-up. RPG features a variety of classes and functions that support gameplay such as:

### Player Class

Defines a players username, password, character type, and character stats such as attack, health, defense, xp, and level. The player class updates the players stats accordingly and saves/updates this data within players.txt

### CharacterType Class

Defines the variety of different character types supported in game along with their specified stats. These types include: fairy, wizard, elf, goblin, valkyrie

### Map Regions

The game currently supports the following regions:
1. Crystal Cave
2. Glittering Gardens
3. Fairy Forest
4. Mythical Mountains
5. Swamp of Secrets

### Player Creation and Login

**create_player()** allows a new player to create a new character. They pick a username, password, and character type. Then, that data is uploaded to players.txt.

**login()** prompts the user to input their username and password, and when correct they will be successfully logged into their account.

**crystal_cave_exploration(player), glittering_gardens_exploration(player), ...** define player exploration within the specific regions and allows the user to take actions within the game. 

**explore_region(player)** prompts the player to select a location to explore and simulates the exploration of the specified region.

### How To Play

Use numeric keys to select choices and travel to different regions of the map.
