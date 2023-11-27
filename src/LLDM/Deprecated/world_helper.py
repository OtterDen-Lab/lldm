# This is my first time making a JSON schema helper function I made it into a class just so I get my head around it
import json
import jsonschema


class DnDWorld:
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
dnd_world = DnDWorld("JSONSchema/world_architecture.json")

# Example data to set (replace this with your actual data)
sample_data = {
    # This is an array of continents
    "continents": [],
    # This is the continent object it'll house regions
    "continent": {
        "name": "MyContinent",
        "id": "Description of MyContinent"
    },
    # This is the region it will house important places and cities with buildings in them
    "region": {
        "name": "MyRegion",
        "id": "Description of MyRegion"
    }
}

# Set data (validate and store if it matches the schema)
if dnd_world.set_data(sample_data):
    print("Data successfully set.")
else:
    print("Data does not match the schema.")

# Get and print the stored data
print(dnd_world.to_json())
