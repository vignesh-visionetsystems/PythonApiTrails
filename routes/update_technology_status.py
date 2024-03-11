from fastapi import APIRouter,Header
from config.db import db_instance
from models.auth.update_techonology_status import UpdateTechnologyStatusRequest
from bson import ObjectId
from routes.autentication_token import getUserIdFromToken


userTechnologyStatus = APIRouter()

userTechnologyCollection = db_instance.userTechnology
userCollection = db_instance.user



@userTechnologyStatus.post("/update_technology_status")
async def updateTechnologyStatus(updateTechnologyStatusRequest:UpdateTechnologyStatusRequest,accessToken:str = Header()):
    userId = getUserIdFromToken(token=accessToken)
    userResult = userCollection.find_one({"_id":ObjectId(userId)})
    if userResult:
        userTechnologyCollection.insert_one({"userId":userResult["_id"],"techId":ObjectId(updateTechnologyStatusRequest.technologyId),"isCompleted":True})
        return {"message":"Updated Successfully"}
    else:
        return {"message":"User is not exists"}
    
   