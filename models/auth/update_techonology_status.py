from  pydantic import BaseModel

class UpdateTechnologyStatusRequest(BaseModel):
    technologyId:str
    isCompleted:bool