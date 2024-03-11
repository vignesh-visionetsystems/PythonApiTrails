from fastapi import APIRouter
from config.db import db_instance
from models.roles.roles import Roles
from models.technology.technology import Technolgoy
from bson import ObjectId

technologiesRouter = APIRouter()

technologyCollection = db_instance.technologies


@technologiesRouter.get("/technologies")
async def getTechnologies():
    return Technolgoy.toList(technologyCollection.find())


@technologiesRouter.post("/create_technology")
async def createNewTechnology(tech:Technolgoy):
    queryStatus = technologyCollection.find_one({"tecName":tech.tecName})
    if queryStatus:
        return {"message":"Tec Name is already exists"}
    else:
        inserRecord =technologyCollection.insert_one(dict(tech))
        inserted_id = inserRecord.inserted_id
        return Technolgoy.to_dict(technologyCollection.find_one({"_id":ObjectId(inserted_id)}))
    
