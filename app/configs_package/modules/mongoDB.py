import os
from flask import current_app
from pymongo import MongoClient

#create the connection url
#connecturl = "mongodb://{}:{}@{}:27017/?authSource=course".format(os.getenv,password,host)
#connecturl = "mongodb+srv://{}:{}@{}/?retryWrites=true&w=majority&appName=Cluster0".format(user,password,host)#"mongodb+srv://rocketmc2009:<db_password>@cluster0.s2tvs.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"


mongodb_connection = MongoClient(current_app.config['MONGO_URI'])

def close():
    mongodb_connection.close()

# get database list
print("Getting list of databases")
dbs = mongodb_connection.list_database_names()
# print the database names
for db in dbs:
    print(db)
print("Closing the connection to the mongodb server")

