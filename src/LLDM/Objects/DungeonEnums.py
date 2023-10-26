from enum import Enum


class Backgrounds(Enum):
    Acolyte = {'name': 'Acolyte'}
    Athlete = {'name': 'Athlete'}
    Charlatan = {'name': 'Charlatan'}
    Criminal = {'name': 'Criminal'}
    Entertainer = {'name': 'Entertainer'}
    Folk_Hero = {'name': 'Folk Hero'}
    Gladiator = {'name': 'Gladiator'}
    Guild_Artisan = {'name': 'Guild Artisan'}
    Guild_Merchant = {'name': 'Guild Merchant'}
    Hermit = {'name': 'Hermit'}
    Knight = {'name': 'Knight'}
    Noble = {'name': 'Noble'}
    Outlander = {'name': 'Outlander'}
    Sage = {'name': 'Sage'}
    Sailor = {'name': 'Sailor'}
    Soldier = {'name': 'Soldier'}

# Hugely annoying subraces:
# Races:
# Hard mandatory subraces:
# Elf:      High / Wood
# Half-Elf: High / Wood
# Gnomes: Forest / Rock
# Halfling: Lightfoot / Stout
# Dragonborn: Draconic Ancestries...
# Tieflings: Bloodlines...so many bloodlines...

# Humans: Normal / Variant

# No Subraces:
# Half-Orc


class Races(Enum): # WIP subrace count
    # No Subraces:
    Half_Orc = {'name': 'Half Orc', 'size': 'MEDIUM', 'subraces': 0}
    # Optional Subraces
    Human = {'name': 'Human', 'size': 'MEDIUM', 'subraces': 0}
    # Hard mandatory subraces
    Gnome = {'name': 'Gnome', 'size': 'MEDIUM', 'subraces': 2}
    Elf = {'name': 'Elf', 'size': 'MEDIUM', 'subraces': 2}
    Half_Elf = {'name': 'Half_Elf', 'size': 'MEDIUM', 'subraces': 2}
    Halfling = {'name': 'Halfling', 'size': 'MEDIUM', 'subraces': 2}

    # Draconic Ancestries / Bloodlines
    Dragonborn = {'size': 'MEDIUM', 'subraces': 0}
    Tiefling = {'size': 'MEDIUM', 'subraces': 0}


class Subraces(Enum):
    Wood_Elf = {'parent': 'Elf', 'traits': []}
    High_Elf = {'parent': 'Elf', 'traits': []}
    Half_Wood_Elf = {'parent': 'Half_Elf', 'traits': []}
    Half_High_Elf = {'parent': 'Half_Elf', 'traits': []}
    Forest_Gnome = {'parent': 'Gnome', 'traits': []}
    Rock_Gnome = {'parent': 'Gnome', 'traits': []}
    Lightfoot_Halfling = {'parent': 'Halfling', 'traits': []}
    Stout_Halfling = {'parent': 'Halfling', 'traits': []}


# Class name, Hit dice, Spellcasting modifier
class Classes(Enum):
    Artificer = {'name': 'Artificer', 'hit_dice': 8, 'spellcasting_mod': 'INT', 'subclasses': 0}
    Barbarian = {'name': 'Barbarian', 'hit_dice': 12, 'spellcasting_mod': None, 'subclasses': 0}
    Bard = {'name': 'Bard', 'hit_dice': 8, 'spellcasting_mod': 'CHA', 'subclasses': 0}
    Cleric = {'name': 'Cleric', 'hit_dice': 8, 'spellcasting_mod': 'WIS', 'subclasses': 0}
    Druid = {'name': 'Druid', 'hit_dice': 8, 'spellcasting_mod': 'WIS', 'subclasses': 0}
    Fighter = {'name': 'Fighter', 'hit_dice': 10, 'spellcasting_mod': None, 'subclasses': 1}
    Monk = {'name': 'Monk', 'hit_dice': 8, 'spellcasting_mod': None, 'subclasses': 0}
    Paladin = {'name': 'Paladin', 'hit_dice': 10, 'spellcasting_mod': 'CHA', 'subclasses': 0}
    Ranger = {'name': 'Ranger', 'hit_dice': 10, 'spellcasting_mod': 'WIS', 'subclasses': 0}
    Rogue = {'name': 'Rogue', 'hit_dice': 8, 'spellcasting_mod': None, 'subclasses': 1}
    Sorcerer = {'name': 'Sorcerer', 'hit_dice': 6, 'spellcasting_mod': 'CHA', 'subclasses': 0}
    Warlock = {'name': 'Warlock', 'hit_dice': 6, 'spellcasting_mod': 'CHA', 'subclasses': 0}
    Wizard = {'name': 'Wizard', 'hit_dice': 8, 'spellcasting_mod': 'INT', 'subclasses': 0}


class Subclasses(Enum):
    Eldritch_Knight = {'name': 'Eldritch Knight', 'spellcast_mod': 'INT'}
    Arcane_Trickster = {'name': 'Arcane Trickster', 'spellcast_mod': 'INT'}


class Attributes(Enum):
    STR = "STR"
    DEX = "DEX"
    CON = "CON"
    INT = "INT"
    WIS = "WIS"
    CHA = "CHA"


class Size(Enum):
    TINY = "TINY"
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"
    HUGE = "HUGE"
    GARGANTUAN = "GARGANTUAN"

