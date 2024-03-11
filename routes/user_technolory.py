from fastapi import APIRouter
from config.db import db_instance
from models.roles.roles import Roles
from models.technology.technology import Technolgoy
from bson import ObjectId
from fastapi import Header
from routes.autentication_token import getUserIdFromToken
from jose import JWTError
from typing import List


userTechnologiesRouter = APIRouter()

userCollection = db_instance.user


@userTechnologiesRouter.get("/user_roles_details")
async def getUserRoleDetails(accessToken:str= Header()):
    try:
        userId = getUserIdFromToken(token=accessToken)
        userResult = userCollection.find_one({"_id":ObjectId(userId)})
        userResult["_id"] = str(userResult["_id"])
        print("UserId",userId)

        if userResult:
            pipeline = [
                {
                    '$match': {
                        '_id': ObjectId('65e964184af6c9c48a81696c')
                    }
                }, {
                    '$unwind': {
                        'path': '$roleId', 
                        'preserveNullAndEmptyArrays': True
                    }
                }, {
                    '$project': {
                        'roleId': {
                            '$convert': {
                                'input': '$roleId', 
                                'to': 'objectId', 
                                'onError': None, 
                                'onNull': None
                            }
                        }, 
                        'userId': '$_id', 
                        '_id': 0
                    }
                }, {
                    '$lookup': {
                        'from': 'roles', 
                        'localField': 'roleId', 
                        'foreignField': '_id', 
                        'as': 'roles'
                    }
                }, {
                    '$unwind': {
                        'path': '$roles', 
                        'preserveNullAndEmptyArrays': True
                    }
                }, {
                    '$project': {
                        'userId': 1, 
                        'roleId': 1, 
                        'roleName': '$roles.roleName'
                    }
                }, {
                    '$lookup': {
                        'from': 'roleTechnology', 
                        'localField': 'roleId', 
                        'foreignField': 'roleId', 
                        'as': 'roleTechnology'
                    }
                }, {
                    '$unwind': {
                        'path': '$roleTechnology', 
                        'preserveNullAndEmptyArrays': True
                    }
                }, {
                    '$lookup': {
                        'from': 'technologies', 
                        'localField': 'roleTechnology.techId', 
                        'foreignField': '_id', 
                        'as': 'technologies'
                    }
                }, {
                    '$unwind': {
                        'path': '$technologies', 
                        'preserveNullAndEmptyArrays': True
                    }
                }, {
                    '$lookup': {
                        'from': 'userTechnology', 
                        'localField': 'technologies._id', 
                        'foreignField': 'techId', 
                        'as': 'userStatus'
                    }
                }, {
                    '$unwind': {
                        'path': '$userStatus', 
                        'preserveNullAndEmptyArrays': True
                    }
                }, {
                    '$project': {
                        'userId': 1, 
                        'roleId': 1, 
                        'roleName': 1, 
                        'technologies': {
                            '$mergeObjects': [
                                '$technologies', {
                                    'isCompleted': {
                                        '$cond': {
                                            'if': {
                                                '$eq': [
                                                    '$userStatus.isCompleted', True
                                                ]
                                            }, 
                                            'then': True, 
                                            'else': False
                                        }
                                    }
                                }
                            ]
                        }
                    }
                }, {
                    '$group': {
                        '_id': '$roleId', 
                        'userId': {
                            '$first': '$userId'
                        }, 
                        'roleId': {
                            '$first': '$roleId'
                        }, 
                        'roleName': {
                            '$first': '$roleName'
                        }, 
                        'technologies': {
                            '$push': '$technologies'
                        }
                    }
                }, {
                    '$project': {
                        '_id': 0, 
                        'userId': {
                            '$toString': '$userId'
                        }, 
                        'roleId': {
                            '$toString': '$roleId'
                        }, 
                        'roleName': 1, 
                        'technologies': {
                            '$map': {
                                'input': '$technologies', 
                                'as': 'item', 
                                'in': {
                                    'technName': '$$item.tecName', 
                                    'techId': {
                                        '$toString': '$$item._id'
                                    }, 
                                    'isCompleted': '$$item.isCompleted'
                                }
                            }
                        }
                    }
                }
            ]
            result = list(userCollection.aggregate(pipeline=pipeline))
            print("result___",result)
            return result
        else:
            return {"message":"User not exists"}
    except JWTError:
        raise

















