from fastapi import APIRouter
from config.db import db_instance
from models.user import Users
from scheme.user import UserEntity
from scheme.user import UsersEntity
from bson import ObjectId

user = APIRouter()

userCollection = db_instance.user



@user.get("/get_all_users")
async def getAllUsers():
    print("=======================")
    curser = userCollection.find()
    for item in curser:
        print("**********************")
        print(item)

    print("**********************")
    return UsersEntity(userCollection.find())


@user.post("/create_user")
async def createUser(user:Users):
    userStatus = userCollection.find_one({"email":user.email})
    print("userStatus : {}".format(userStatus))
    if userStatus:
        return {"message":"User already exists"}
    else:
        insertUser =userCollection.insert_one(dict(user))
        inserted_id = insertUser.inserted_id
        return UserEntity(userCollection.find_one({"_id":ObjectId(inserted_id)}))
    
