from PrettyPrinter import PrettyPrinter

# This is the hierarchical file for objects from World >>> Building
# This may expand to include Characters, Lootables, and more (or put into separate file is possible)
#
# Possibly able to put add/remove into PrettyPrint base class,
#   but unlikely, as Objects may have differing data structures
# Currently, add() has support for the specific Object, and lists (no typechecks on list!!)
# remove() only removes single Objects of specific Type. (To-Do)


class World(PrettyPrinter):
    def __init__(self, name=None, description=None, continents=None):
        super().__init__()
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.continents = continents if continents is not None else []

    def add_continent(self, obj):
        if isinstance(obj, Continent):
            self.continents.append(obj)
        elif isinstance(obj, list):
            self.continents = obj
        else:
            raise ValueError("Expected either a Continent or a list.")

    def remove_continent(self, continent):
        if isinstance(continent, Continent):
            self.continents.remove(continent)
        else:
            raise ValueError("Expected either a Region.")


class Continent(PrettyPrinter):
    def __init__(self, name=None, description=None, regions=None):
        super().__init__()
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.regions = regions if regions is not None else []

    def add_region(self, obj):
        if isinstance(obj, Region):
            self.regions.append(obj)
        elif isinstance(obj, list):
            self.regions = obj
        else:
            raise ValueError("Expected either a Region or a list.")

    def remove_regions(self, region):
        if isinstance(region, Region):
            self.regions.remove(region)
        else:
            raise ValueError("Expected either a Region.")


class Region(PrettyPrinter):
    def __init__(self, name=None, description=None, notable_locations=None):
        super().__init__()
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.notable_locations = notable_locations if notable_locations is not None else []

    def add_location(self, obj):
        if isinstance(obj, City) or isinstance(obj, Site):
            self.notable_locations.append(obj)
        elif isinstance(obj, list):
            self.notable_locations = obj
        else:
            raise ValueError("Expected either a City, a Site or a list.")

    def remove_location(self, poi):
        if isinstance(poi, City) or isinstance(poi, Site):
            self.notable_locations.remove(poi)
        else:
            raise ValueError("Expected either a City or Site.")


# WIP: Currently a terminal endpoint
# Logically equivalent to City, but currently bare-bones. Use for some other TBD Point-of-Interest of the same scale
class Site(PrettyPrinter):
    def __init__(self, name=None, description=None):
        super().__init__()
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description


class City(PrettyPrinter):
    def __init__(self, name, description, districts):
        super().__init__()
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.districts = districts if districts is not None else []

    def add_district(self, obj):
        if isinstance(obj, CityDistrict):
            self.districts.append(obj)
        elif isinstance(obj, list):
            self.districts = obj
        else:
            raise ValueError("Expected either a CityDistrict or a list.")

    def remove_district(self, district):
        if isinstance(district, CityDistrict):
            self.districts.remove(district)
        else:
            raise ValueError("Expected a CityDistrict.")


class CityDistrict(PrettyPrinter):
    def __init__(self, name=None, description=None, buildings=None):
        super().__init__()
        if name is not None:
            self.name = name
        if description is not None:
            self.description = description
        self.buildings = buildings if buildings is not None else []

    def add_building(self, obj):
        if isinstance(obj, Building):
            self.buildings.append(obj)
        elif isinstance(obj, list):
            self.buildings = obj
        else:
            raise ValueError("Expected either a Building or a list.")

    def remove_building(self, bldg):
        if isinstance(bldg, Building):
            self.buildings.remove(bldg)
        else:
            raise ValueError("Expected a Building.")


class Building(PrettyPrinter):
    def __init__(self, name, description):
        super().__init__()
        self.name, self.description = name, description
