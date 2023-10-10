# DO NOT TOUCH THESE IMPORTS UNLESS YOU KNOW EXACTLY WHAT YOU ARE DOING: THE ORDER MATTERS!!!!!
from GPT       import *
from Campaign  import Campaign
from Character import Character
from Quest     import Quest
from World     import World


# Example Usage:
# world = World("FantasyLand", "A magical realm of adventures.")
# party = [Character("Alice", "Wizard", 5), Character("Bob", "Warrior", 6)]
# quests = [Quest("Find the magic stone"), Quest("Defeat the dragon", "In Progress")]
# campaign = Campaign(world, party, quests)
# print(campaign)


print("LLDM Active:\nType \"exit\" to stop this program.\n")
campaign = Campaign()

print("Stage 1: Character Creation")

print(f"[DEBUG]: Accessing character stored in {PATH_RESOURCE_SAMPLE_CHARACTER}")
player_character = Character(PATH_RESOURCE_SAMPLE_CHARACTER)

print(f"Adding [{player_character.JSON['name']}] to Party\n")
campaign.add_character(player_character)

print("[DEBUG] Fast-tracking Campaign Generation...")
print("Stage 2: World Generation")
print(f"Campaign Setup Complete:\n {campaign} \n")

print("Stage 3: ChatGPT Narration")

print("LLDM: Initializing Scene")
print(place_player(player_character))

user_input = str(input())
while user_input != "exit":
    match user_input:
        case "Print Environ":
            sdprompter()
        case _:
            lldm_output = gamemaster(user_input)
            mem_output = chronicler(lldm_output)
    user_input = str(input())
print("Goodbye")
