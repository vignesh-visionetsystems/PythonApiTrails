from fastapi import APIRouter
from config.db import db_instance
from models.auth.user import UserEntity
# from scheme.user import UsersEntity
from bson import ObjectId
from models.auth.login import Login
from models.auth.login_response import LoginResponse
from routes.jwt_token import get_token

user = APIRouter()

userCollection = db_instance.user

# @user.get("/")
# async def root():
#     return {"message":"Api is working..."}

# @user.get("/get_all_users")
# async def getAllUsers():
#     print("=======================")
#     curser = userCollection.find()
#     for item in curser:
#         print("**********************")
#         print(item)

#     print("**********************")
#     return UsersEntity(userCollection.find())


@user.post("/signup")
async def createUser(user:UserEntity):
    userStatus = userCollection.find_one({"email":user.email})
    print("userStatus : {}".format(userStatus))
    if userStatus:
        return {"message":"User already exists"}
    else:
        insertUser =userCollection.insert_one(dict(user))
        inserted_id = insertUser.inserted_id
        return UserEntity(userCollection.find_one({"_id":ObjectId(inserted_id)}))
    


@user.post("/login")
async def login(user:Login):
    userStatus = userCollection.find_one({"email":user.email})
    print("userStatus",userStatus)
    if userStatus != None:
        loginResponse =  LoginResponse.from_dict(userStatus)
        print("currentUser",loginResponse)
        if(user.password != loginResponse.password):
            return getErrorMesssage("Password Incorrect")
        else:
            token = await get_token()
            loginResponse.accessToken = token["token"]
            return loginResponse
    else:
     return getErrorMesssage("User doesn't exists")

    
def getErrorMesssage(message:str):
         return {"message":message}
