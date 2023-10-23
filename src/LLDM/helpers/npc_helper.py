import json
import jsonschema


class NPCBehavior:
    def __init__(self, schema_path):
        self.schema = self.load_schema(schema_path)
        self.data = {}

    def load_schema(self, schema_path):
        with open(schema_path, 'r') as schema_file:
            return json.load(schema_file)

    def validate_data(self):
        try:
            jsonschema.validate(self.data, self.schema)
            return True
        except jsonschema.exceptions.ValidationError:
            return False

    def set_data(self, data):
        if self.validate_data():
            self.data = data
            return True
        else:
            return False

    def get_data(self):
        return self.data

    def to_json(self):
        return json.dumps(self.data, indent=4)


# Usage example
npc_behavior = NPCBehavior("JSONSchema/npc_behavior.json")

# Example data to set (replace this with your actual data)
sample_data = {
    "name": "Sample Orc Fighter",
    "race": {
        "name": "Orc",
        "subtype": "",
        "traits": [
            {
                "name": "Adrenaline Rush",
                "description": "You can take the Dash action as a bonus action. You can use this trait a number of times equal to your proficiency bonus, and you regain all expended uses when you finish a long rest. Whenever you use this trait, you gain a number of temporary hit points equal to your proficiency bonus."
            },
            {
                "name": "Darkvision",
                "description": "You can see in dim light within 60 feet of you as if it were bright light and in darkness as if it were dim light. You discern colors in that darkness only as shades of gray."
            },
            {
                "name": "Powerful Build",
                "description": "You count as one size larger when determining your carrying capacity and the weight you can push, drag, or lift.",
            },
            {
                "name": "Relentless Endurance",
                "description": "When you are reduced to 0 hit points but not killed outright, you can drop to 1 hit point instead. Once you use this trait, you can’t do so again until you finish a long rest.",
            }
        ]
    },
    "classes": [
        {
            "name": "Fighter",
            "subtype": "",
            "level": 1,
            "hit_die": 10,
            "spellcasting": "",
            "features": [
                {
                    "name": "Great Weapon Fighting",
                    "description": "When you roll a 1 or 2 on a damage die for an attack you make with a melee weapon that you are wielding with two hands, you can reroll the die and must use the new roll, even if the new roll is a 1 or a 2. The weapon must have the two-handed or versatile property for you to gain this benefit.",
                },
                {
                    "name": "Second Wind",
                    "description": "You have a limited well of stamina that you can draw on to protect yourself from harm. On your turn, you can use a bonus action to regain hit points equal to 1d10 + your fighter level. Once you use this feature, you must finish a short or long rest before you can use it again.",
                }
            ]
        }
    ],
    "alignment": "neutral good",
    "speed": {
        "Walk": 30
    },
    "hit_points": {
        "max": 12,
        "current": 12
    },
    "ability_scores": {
        "str": 16,
        "dex": 14,
        "con": 14,
        "int": 10,
        "wis": 10,
        "cha": 12
    },
    "skills": {
        "Animal Handling": True,
        "Atheltics": True,
        "Intimidation": True,
        "Survival": True
    },
    "armor_class": {
        "value": 16,
        "description": "Chain mail"
    },
    "saving_throws": {
        "str": True,
        "con": True
    },
    "languages": ["Common"],
    "background": {
        "name": "Folk Hero"
    },
    "details": {
        "personality": "When I set my mind to something, I follow through no matter what gets in my way.",
        "ideal": "Destiny. Nothing and no one can steer me away from my higher calling.",
        "bond": "My tools are symbols of my past life, and I carry them so that I will never forget my roots.",
        "flaw": " I have a weakness for the vices of the city, especially hard drink."
    },
    "weapons": [
        {
            "name": "Glaive",
            "damage": {
                "dice": {
                    "sides": 10,
                    "count": 1
                },
                "type": "Slashing"
            },
            "equipped": True,
            "properties": {
                "Heavy": True,
                "Reach": True,
                "Two-Handed": True,
            }
        }
    ],
    "spells": [{""}]
}


# Set data (validate and store if it matches the schema)
if npc_behavior.set_data(sample_data):
    print("Data successfully set.")
else:
    print("Data does not match the schema.")

# Get and print the stored data
print(npc_behavior.to_json())
