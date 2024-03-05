from fastapi import APIRouter
from config.db import db_instance
from models.roles import Roles
from scheme.role import RoleEntity,RolesEntity
from bson import ObjectId

roles = APIRouter()

rolesCollection = db_instance.roles


@roles.get("/roles")
async def getRoles():
    return RolesEntity(rolesCollection.find())


@roles.post("/create_role")
async def createUser(role:Roles):
    queryStatus = rolesCollection.find_one({"roleName":role.roleName})
    if queryStatus:
        return {"message":"Role is already exists"}
    else:
        inserRecord =rolesCollection.insert_one(dict(role))
        inserted_id = inserRecord.inserted_id
        return RoleEntity(rolesCollection.find_one({"_id":ObjectId(inserted_id)}))
    
