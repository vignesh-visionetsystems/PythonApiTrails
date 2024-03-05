from  pydantic import BaseModel

class Roles(BaseModel):
    roleName:str

    def to_dict(item) -> dict:
        return {
            "roleId":str(item["_id"]),
            "roleName":item["roleName"]
        }


    def toList(entity) -> list:
        return [Roles.to_dict(item) for item in entity]

    @classmethod
    def from_dict(cls, data):
        return cls(
            roleId=data.get("_id_"),
            roleName=data.get("roleName")
            )
