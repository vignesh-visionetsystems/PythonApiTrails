from  pydantic import BaseModel


class Technolgoy(BaseModel):
    tecName:str

    def to_dict(item) -> dict:
        return {
            "tecId":str(item["_id"]),
            "tecName":item["tecName"]
        }


    def toList(entity) -> list:
        return [Technolgoy.to_dict(item) for item in entity]

    @classmethod
    def from_dict(cls, data):
        return cls(
            tecId=data.get("_id_"),
            tecName=data.get("tecName")
            )
