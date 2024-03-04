from  pydantic import BaseModel



class Users(BaseModel):
    userName:str
    email:str
    password:str

 