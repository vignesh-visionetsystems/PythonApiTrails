from fastapi import APIRouter
from config.db import db_instance
from models.role_technology.role_technology import RoleTechnology
from bson import ObjectId



roleTechnology = APIRouter()

roleTechnologyCollection = db_instance.roleTechnology
rolesCollection = db_instance.roles
technologiesCollection = db_instance.technologies




@roleTechnology.post("/assign_tech_to_role")
async def createNewRole(roleTechnology:RoleTechnology):
    
    roleResult = rolesCollection.find_one({"_id":ObjectId(roleTechnology.roleId)})
    technologyeResult = technologiesCollection.find_one({"_id":ObjectId(roleTechnology.techId)})

    if not roleResult or not technologyeResult:
        return "Role or Technology is missing"
    else:
        queryStatus = roleTechnologyCollection.find_one({"roleId":ObjectId(roleTechnology.roleId),"techId":ObjectId(roleTechnology.techId)})
        if queryStatus:
            return {"message":"This Technology is already assigned"}
        else:
            roleTechnologyCollection.insert_one({"roleId":roleResult["_id"],"techId":technologyeResult["_id"]})
            return {"message":"Technology Assigned Successfully"}
    



@roleTechnology.post("/get_all_tech_by_roles")
async def getAllTechByRoleBase():
    pipeline = [
    {
        '$lookup': {
            'from': 'roleTechnology', 
            'localField': '_id', 
            'foreignField': 'roleId', 
            'as': 'roleTechnologies'
        }
    }, {
        '$unwind': {
            'path': '$roleTechnologies', 
            'preserveNullAndEmptyArrays': True
        }
    }, {
        '$lookup': {
            'from': 'technologies', 
            'localField': 'roleTechnologies.techId', 
            'foreignField': '_id', 
            'as': 'techDetails'
        }
    }, {
        '$unwind': {
            'path': '$techDetails', 
            'preserveNullAndEmptyArrays': True
        }
    }, {
        '$group': {
            '_id': {
                '_id': '$_id', 
                'roleName': '$roleName'
            }, 
            'techDetails': {
                '$push': '$techDetails'
            }
        }
    }, {
        '$project': {
            'roleId': {
                '$toString': '$_id._id'
            }, 
            'roleName': '$_id.roleName', 
            '_id': 0, 
            'technologies': {
                '$cond': {
                    'if': {
                        '$eq': [
                            {
                                '$size': '$techDetails'
                            }, 0
                        ]
                    }, 
                    'then': None, 
                    'else': {
                        '$map': {
                            'input': '$techDetails', 
                            'as': 'item', 
                            'in': {
                                '_id': {
                                    '$toString': '$$item._id'
                                }, 
                                'techName': '$$item.tecName'
                            }
                        }
                    }
                }
            }
        }
    }
    ]



    # Convert ObjectId to string in the result
    results =list(rolesCollection.aggregate(pipeline))

    # print("get_all_tech_by_roles:", results)

    # return [{**doc,'_id':str(doc["_id"])} for doc in results]
    return results

    






