#4)Get players depending on scores per game

import pymongo
from pymongo import MongoClient
from pprint import pprint
MONGO_HOST = "172.31.17.112"
MONGO_PORT = 27017
MONGO_DB = "db"
connection = MongoClient(MONGO_HOST, MONGO_PORT)
db = connection[MONGO_DB]

#4)Get players depending on scores per game
db = connection.get_database()
athletic_col = db["athletic_info"]
personal_col = db["personal_info"]
#inputs desired position and height 
min_points = input("Specify the minimum number of average points to search: ")
#operation that tells the code to accept on greater or equal than inputted item


#pipeline to be aggregate to retrieve players with specified  minimum number of points
pipeline = {
    {
        "$match": {
            "AveragePointsPerGame":{
                "$gte": min_points}

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
        "$project": {"_id": 0,
                     "FullName": {"$concat":
                                   ["$personal_info.FirstName", " ", "$personal_info.LastName"]},
                     "PlayerID": 1,
                     "AveragePointsPerGame": 1,
        }
    }}
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