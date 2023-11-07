from LLDM.Objects.ObjectSerializer import *
from LLDM.Objects.WorldArchitecture import *

# Main file to test Factory/World generation


# Create new objects & connections
# World
world1 = World("Azeroth", "A planet under construction", [])

# Continent
continent1 = Continent("Eastern Kingdoms", "Landmass on the right", [])
continent2 = Continent("Kalimdor", "Landmass on the left", [])

# Region
region1 = Region("Elwynn Forest", "A lush, temperate forest", [])
region2 = Region("Duskwood", "A dark and twisted forest", [])
region3 = Region("Durotar", "A dry, hard land", [])
region4 = Region("The Barrens", "A dusty wasteland", [])
region5 = Region("Teldrassil", "One of the great World Trees", [])

# City / Site
city1 = City("Stormwind City", "Alliance Capital", [])
city2 = City("Orgrimmar", "Horde Capital", [])
city3 = City("Darnassas", "Home city of the elves", [])
site1 = Site("Crossroads", "Deadly place. Beware bandits in the plains")
site2 = Site("Darkshire", "Small town in the dark. Mind the Night Watch")

# CityDistrict
district1 = CityDistrict("Trade District", "Center for commerce")
district2 = CityDistrict("Dwarven District", "Industrial center. Perpetually lit by forge-fire")
district3 = CityDistrict("Path of Honor", "A zone dedicated to fallen heroes")
district4 = CityDistrict("Cenarion Grove", "An enclave for the druidic order")

# Building
# To-Do: Add buildings

# Add Connections
city1.add_district(district1)
city1.add_district(district2)
city2.add_district(district3)
city3.add_district(district4)
region1.add_location(city1)
region3.add_location(city2)
region5.add_location(city3)
region2.add_location(site2)
region4.add_location(site1)
continent1.add_region(region1)
continent1.add_region(region2)
continent2.add_region(region3)
continent2.add_region(region4)
continent2.add_region(region5)

world1.add_continent(continent1)
world1.add_continent(continent2)


# Pack World into json
worldJson = obj_to_json(world1)

# Unpack World into object
worldObj = json_to_obj(worldJson)

print(worldJson)
print(worldObj)

# WorldObj is treated as a new World instance
worldObj.set_name("Argus")
print(worldObj)
