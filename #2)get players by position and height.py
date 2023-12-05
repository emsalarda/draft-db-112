#2)get players by position and height 
import pymongo
from pymongo import MongoClient
from pprint import pprint
MONGO_HOST = "172.31.17.112"
MONGO_PORT = 27017
MONGO_DB = "db"
connection = MongoClient(MONGO_HOST, MONGO_PORT)
db = connection[MONGO_DB]

#2)get players by position and height 
##specify what postion or height criteria
db = connection.get_database()
athletic_col = db["athletic_info"]
medical_col = db["medical_info"]
personal_col = db["personal_info"]
#inputs desired position and height 
Tposition = input("Enter desired position: ")
#only accepts float input 
min_height = float(input ("Enter minimum height: "))
#operation that tells the code to accept on greater or equal than inputted item


#pipeline to be aggregate to retrieve player position and height 
pipeline = {
    {
        "$match": {
            "Position": Tposition
        }
    },
    {"$lookup":{"from": "personal_info",
        "localField": "PlayerID", 
        "foreignField": "PlayerID", 
        "as": "personal_info"}
    },
    {
        "$unwind": "$personal_info" #checks personal info 
    },
    {
        "$match": {"medical_info": {
            {"$gte": min_height}
        }
    }
    },
    {
        "$project": {"_id": 0,
                     "FullName": {"$concat":
                                   ["$personal_info.FirstName", " ", "$personal_info.LastName"]},
                     "PlayerID": 1,
                     "Position": 1,
                     "Height": "medical_info.Height"
        }
    }
}

#prompt to aggregate 
result = list(athletic_col.aggregate(pipeline))

#print results
if result: 
    print ("Players who match the criteria: ")
    for player in result: 
        pprint(player)
else: 
    print("No Players found to match the specified criteria")
#except statement for error 
except Expection as e:
    print(f"An Unexpected error occured; {e}")