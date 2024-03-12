from fastapi import APIRouter,HTTPException,Depends
from config.db import db_instance
from bson import ObjectId
from fastapi import Header
from routes.autentication_token import getUserIdFromToken
from jose import JWTError
from typing import List


userTechnologiesRouter = APIRouter()

userCollection = db_instance.user


@userTechnologiesRouter.get("/user_roles_details")
async def getUserRoleDetails(userId:str= Depends(getUserIdFromToken)):
    try:
        userResult = userCollection.find_one({"_id":ObjectId(userId)})
        userResult["_id"] = str(userResult["_id"])
        print("UserId",userId)

        if userResult:
            pipeline = [
                {
                    '$match': {
                        '_id': ObjectId(userId)
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
                        'let': {
                            'userId': '$userId', 
                            'techId': '$technologies._id'
                        }, 
                        'pipeline': [
                            {
                                '$match': {
                                    '$expr': {
                                        '$and': [
                                            {
                                                '$eq': [
                                                    '$userId', '$$userId'
                                                ]
                                            }, {
                                                '$eq': [
                                                    '$techId', '$$techId'
                                                ]
                                            }
                                        ]
                                    }
                                }
                            }
                        ], 
                        'as': 'userStatus'
                    }
                }, {
                    '$unwind': {
                        'path': '$userStatus', 
                        'preserveNullAndEmptyArrays': True
                    }
                }, {
                    '$addFields': {
                        'technologies.isCompleted': '$userStatus.isCompleted'
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
                                    'isCompleted': {
                                        '$cond': {
                                            'if': {
                                                '$eq': [
                                                    '$$item.isCompleted', True
                                                ]
                                            }, 
                                            'then': True, 
                                            'else': False
                                        }
                                    }
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
    except Exception as e:
         raise HTTPException(status_code=200, detail=str(e))

















