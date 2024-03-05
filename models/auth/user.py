from  pydantic import BaseModel


class UserEntity(BaseModel):
    firstName:str
    lastName:str
    email:str
    password:str
    phoneNumber:str
    roleId:str

    def to_dict(item) -> dict:
        return {
            "id":str(item["_id"]),
            "firstName":item["firstName"],
            "lastName":item["lastName"],
            "email":item["email"],
            "password":item["password"],
            "phoneNumber":item["phoneNumber"],
            "roleId":item["roleId"]
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
                roleId=data.get("roleId")
            )
    
    def toList(entity) -> list:
        return [UserEntity.to_dict(item) for item in entity]







 