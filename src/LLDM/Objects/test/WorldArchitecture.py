from LLDM.Core.PrettyPrinter import PrettyPrinter


# This is the hierarchical file for objects from World >>> Building
# This may expand to include Characters, Lootables, and more (or put into separate file is possible)
#
# Possibly able to put add/remove into PrettyPrint base class,
#   but unlikely, as Objects may have differing data structures
# Currently, add() has support for the specific Object, and lists (no typechecks on list!!)
# remove() only removes single Objects of specific Type. (To-Do)

# ToDo: Major: Implement Factory Pattern onto zones. Make new inheritable for name, description, and child location list

class BaseLocation(PrettyPrinter):
    def __init__(self, name: str, description: str, children=None):
        super().__init__()
        self.name = name
        self.description = description
        self.children = children if children is not None else []

    def add(self, obj):
        self.children.append(obj)

    def remove(self, obj):
        self.children.remove(obj)


class Building(BaseLocation):
    pass  # Currently, Building doesn't need any additional methods or attributes.


class CityDistrict(BaseLocation):
    def add_building(self, building: Building):
        self.add(building)

    def remove_building(self, building: Building):
        self.remove(building)


class City(BaseLocation):
    def add_district(self, district: CityDistrict):
        self.add(district)

    def remove_district(self, district: CityDistrict):
        self.remove(district)


class Site(BaseLocation):
    pass  # Currently, Site doesn't need any additional methods or attributes.


class Region(BaseLocation):
    def add_location(self, location: City | Site):
        self.add(location)

    def remove_location(self, location: City | Site):
        self.remove(location)


class Continent(BaseLocation):
    def add_region(self, region: Region):
        self.add(region)

    def remove_region(self, region: Region):
        self.remove(region)


class World(BaseLocation):
    def add_continent(self, continent: Continent):
        self.add(continent)

    def remove_continent(self, continent: Continent):
        self.remove(continent)
