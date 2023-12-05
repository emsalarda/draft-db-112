#1)Get player's personal athletic and medical information 
import pymongo
from pymongo import MongoClient
from pprint import pprint
MONGO_HOST = "172.31.17.112"
MONGO_PORT = 27017
MONGO_DB = "db"
connection = MongoClient(MONGO_HOST, MONGO_PORT)
db = connection[MONGO_DB]

    # Access the collection
db = connection.get_database()
players_col = db["player_info"]
athletic_col = db["athletic_info"]
medical_col = db ["medical_info"]

# Specify last name and first name 
Search_Fname = input("Enter player's first name: ")
Search_Lname = input("Enter player's last name: ")
    # looks up similar to merge or left joi
pipeline = [
    {"$match": {
     "PersonalInformation.FirstName": Search_Fname,
     "PersonalInformation.LastName": Search_Lname
     }
     },
    {"$lookup":
      {"from": "athletic_info",
        "localField": "PlayerID", 
        "foreignField": "PlayerID", 
        "as": "athletic_info"}},
    {"$lookup": {"from": "medical_info",
                  "localField": "PlayerID",
                  "foreignField": "PlayerID",
                  "as": "medical_info"}},
    {"$project": {
        "_id": 0,
        "PlayerID": 1,
        "PersonalInformation": {
            "FirstName": "$FirstName",
            "LastName": "$LastName",
            "Birthday": "$Birthday",
            "Age": "$Age",
            "Nationality": "$Nationality",
            "ContactInformation": "$ContactInformation",
            "Address": "$Address",
            "School": "$School",
            "GPA": "$GPA"
            },
        "AthleticInfo": {
            "Position": "$athletic_col.Position",
            "AveragePointsPerGame": "$athletic_col.AveragePointsPerGame",
            "AverageReboundsPerGame": "$athletic_col.AverageReboundsPerGame",
            "AverageAssistsPerGame": "$athletic_col.AverageAssistsPerGame",
            "AveragePlayingTime": "$athletic_col.AveragePlayingTime",
            "FreeThrowPercentage": "$athletic_col.FreeThrowPercentage",
            "FieldGoalPercentage": "$athletic_col.FieldGoalPercentage"
            },
        "MedicalInfo": {
            "Height": "$medical_info.Height",
            "Weight": "$medical_info.Weight",
            "PastMedicalConditions": "$medical_info.PastMedicalConditions",
            "CurrentMedicalConditions": "$medical_info.CurrentMedicalConditions"
            }
            }
        }
    ]

    # result, executes pipeline functions 
result = list(players_col.aggregate(pipeline))

    # if statement to Check if any user was found
if result:
    # Print the simplified information
    player_info = result[0]
    pprint("Player Information:", players_col) #Player_info can be changed to name of collections
else:
    print(f"No user found with ID '{user_id}'.")



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
        }},
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
    }},
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
except Excepction as e:
    print(f"An Unexpected error occured; {e}")