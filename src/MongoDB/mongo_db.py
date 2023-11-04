from pymongo import MongoClient
# Connection
client = MongoClient('localhost', 8192)
# Database
db = client['LLDM']
# Collections (= Tables)
backgrounds = db['background']
classes = db['class']
subclasses = db['subclass']
races = db['race']
subraces = db['subrace']


for record in backgrounds.find({}):
    print(record)

# query_result = backgrounds.find({"name": "Acolyte", "description": "a acolyte"})
# for record in query_result:
#     print(record)




#
# my_collection.update_one({"name": "Acolyte", "description": "a acolyte"}, {"$set": {"description": "a new acolyte"}})
#
#
# query_result = my_collection.find({"name": "Acolyte"})
# for document in query_result:
#     print(document)


# new_data = {"key": "value"}
# result = my_collection.insert_one(new_data)
#
# query_result = my_collection.find({"key": "value"})
# for document in query_result:
#     custom_obj = custom_object_hook(document)
#     # Do something with custom_obj
#
# my_collection.update_one({"key": "value"}, {"$set": {"key": "new_value"}})
#
# my_collection.delete_one({"key": "value"})
