from  pydantic import BaseModel
from  typing import Optional

class LoginResponse(BaseModel):
    firstName:str
    lastName:str
    email:str
    password:str
    phoneNumber:str
    roleId:str
    accessToken:Optional[str]

    def to_dict(item) -> dict:
            return {
            "id":str(item["_id"]),
            "firstName":item["firstName"],
            "lastName":item["lastName"],
            "email":item["email"],
            "password":item["password"],
            "phoneNumber":item["phoneNumber"],
            "roleId":item["roleId"],
            "accessToken":item["accessToken"]
        }

    @classmethod
    def from_dict(cls, data):
            return cls(
                id=data.get("_id_"),
                firstName=data.get("firstName"),
                lastName=data.get("lastName"),
                email=data.get("email"),
                password=data.get("password"),
                phoneNumber=data.get("phoneNumber"),
                roleId=data.get("roleId"),
                accessToken=data.get("accessToken")
            )