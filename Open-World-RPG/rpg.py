import os
# Define Player class
class Player:
    def __init__(self, ign, character_type, password):
        self.ign = ign
        self.character_type = character_type
        self.password = password
        self.attack = character_type.attack
        self.health = character_type.health
        self.defense = character_type.defense
        self.xp = 0
        self.level = 1

    def update_player_stats(self, new_attack, new_health, new_defense):
        self.attack = new_attack
        self.health = new_health
        self.defense = new_defense

    def level_up(self):
        self.level += 1
        print("Level Up! You are now level " + str(self.level))
        self.save_to_file() 

    def calculate_level(self):
        return self.level * 100
    
    def gain_xp(self, amount):
        self.xp += amount
        while self.xp >= self.calculate_level():
            self.level_up()
        self.save_to_file()
            
    def save_to_file(self):
        with open("players.txt", "r") as file:
            lines = file.readlines()

        with open("players.txt", "w") as file:
            for line in lines:
                if self.ign in line:
                    line = f"{self.ign} {self.password} {self.character_type.name} {self.attack} {self.health} {self.defense} {self.level} {self.xp}\n"
                file.write(line)
                
# Define CharacterType class
class CharacterType:
    def __init__(self, name, attack, health, defense):
        self.name = name
        self.attack = attack
        self.health = health
        self.defense = defense

# Define different character types
fairy = CharacterType("Fairy", 100, 1150, 100)
wizard = CharacterType("Wizard", 275, 900, 175)
elf = CharacterType("Elf", 200, 1000, 150)
goblin = CharacterType("Goblin", 125, 1000, 225)
valkyrie = CharacterType("Valkyrie", 250, 850, 250)

# Define create_player function, which prompts the user for a username and password
# The user must choose an original username that doesn't already exist on file
# Saves player data to file players.txt
def create_player():
    while True:
        player_name = input("Enter your in-game username: ")
        password = input("Enter your password: ")

        user_exists = False
        if os.path.exists("players.txt"):
            with open("players.txt", "r") as file:
                for line in file:
                    if player_name in line:
                        print("User is already taken. Please choose a different username.")
                        user_exists = True
                        break

        if not user_exists:
            while True:
                print("Choose your character type: ")
                print("1. Fairy\n2. Wizard\n3. Elf\n4. Goblin\n5. Valkyrie")
                character_type_choice = input()
                if character_type_choice == "1":
                    player = Player(player_name, fairy, password)
                elif character_type_choice == "2":
                    player = Player(player_name, wizard, password)
                elif character_type_choice == "3":
                    player = Player(player_name, elf, password)
                elif character_type_choice == "4":
                    player = Player(player_name, goblin, password)
                elif character_type_choice == "5":
                    player = Player(player_name, valkyrie, password)
                break
            # Check if the file doesn't exist and write the header
            if not os.path.exists("players.txt"):
                with open("players.txt", "w") as f:
                    f.write("Username Password CharacterType Attack Health Defense Level XP\n")

            # Append the player's data
            with open("players.txt", "a") as f:
                f.write(f"{player.ign} {player.password} {player.character_type.name} {player.character_type.attack} {player.character_type.health} {player.character_type.defense} {player.level} {player.xp}\n")
                print("User created successfully!")
                break

# Login 
def login():
    while True:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        player_found = False
        user = None

        with open("players.txt", "r") as file:
            for line in file:
                fields = line.split()
                if len(fields) == 8:
                    stored_username, stored_password = fields[0], fields[1]
                    if username == stored_username and password == stored_password:
                        player_found = True
                        character_type = CharacterType(fields[2], int(fields[3]), int(fields[4]), int(fields[5]))
                        user = Player(stored_username, character_type, stored_password)

        if not player_found:
            print("Invalid username or password. Please try again.")
        else:
            return user

def crystal_cave_exploration(player):
    print("You hear an ominous noise coming from the caves left tunnel, but theres a tiny glimmer of light.\n")
    print("The tunnel to the right is pitch black and silent.\n")
    print("1. Left\n2. Right\n")
    path = input("Which path would you like to take? ")
    if path == "1":
        print("What a relief! The noise was just the dripping of water from the top of the cave... But what is that light?\n")
        print("You've found a lucky health crystal! +50 Health")
        player.health += 50
        player.gain_xp(50)
    elif path == "2":
        print("An evil bat was silently waiting in the darkness. Get ready to fight!")
        print("1. Cast a spell\n2. Shoot an arrow")
        fight = input("We must defeat the bat to get out of here alive. Choose your attack: ")
        if fight == "1":
            print("The spell is successful. +50 Attack")
            player.attack += 50
            player.gain_xp(50)
        elif fight == "2":
            print("The arrow misses, and the bat bares its fangs before quickly flying away. -50 Health")
            player.health -= 50
            player.gain_xp(50)

def glittering_gardens_exploration(player):
    print("You stumble upon a beautiful flower field and contemplate picking one so you can always remember the beautiful sight.")
    print("Do you pick the flower?")
    print("1. Yes\n2. No")
    choice = input()
    if choice == "1":
        print("An angry elf comes running. 'How dare you touch my flowers!?'")
        print("You run away from the garden to avoid causing a scene.")
        player.health -= 50
        player.gain_xp(50)
    elif choice == "2":
        print("Might aswell enjoy the scenery while you can.")
        print("You stay at the flower field, taking in the beautiful colors.")
        print("Soon, the sun begins the set and night falls quickly.")
        print("An elf nearby notices you. 'Hello, are you lost?")
        print("1. Yes\n2. No")
        lost_choice = input()
        if lost_choice == "1":
            print("'Here's a map to help you find your way home. Goodluck on your travels!'")
            player.defense += 50
            player.gain_xp(50)
        elif lost_choice == "2":
            print("You inform the elf that you were just admiring the beautiful field and lost track of time.")
            print("The elf says, 'This is my field, but it's been a long time since I've been able to share the view with another. Please, take this flower and come again soon.'")
            player.health += 100
            player.gain_xp(100)

def fairy_forest_exploration(player):
    pass

def mystical_mountains_exploration(player):
    pass

def swamp_of_secrets_exploration(player):
    pass

regions = {
    "0": "Back to Main Menu",
    "1": "Crystal Cave",
    "2": "Glittering Gardens",
    "3": "Fairy Forest",
    "4": "Mystical Mountains",
    "5": "Swamp of Secrets"
    }


def explore_region(player):
    while True:
        print("\nMap:")
        for key, value in regions.items():
            print(f"{key}. {value}")
        location = input("Select a place to explore: ")

        if location == "0":
            break
        elif location == "1":
            crystal_cave_exploration(player)
        elif location == "2":
            glittering_gardens_exploration(player)
        elif location == "3":
            fairy_forest_exploration(player)
        elif location == "4":
            mystical_mountains_exploration(player)
        elif location == "5":
            swamp_of_secrets_exploration(player)
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    while True:
        print("1. Create New Player\n2. Login\n3. Exit")
        choice = input("Select an option: ")
        if choice == "1":
            create_player()
        elif choice == "2":
            player = login()
            explore_region(player)
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")
