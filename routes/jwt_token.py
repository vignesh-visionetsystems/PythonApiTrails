from fastapi import  status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import APIRouter



# replace it with your 32 bit secret key
SECRET_KEY = "09d25e094faa****************f7099f6f0f4caa6cf63b88e8d3e7"
 
# encryption algorithm
ALGORITHM = "HS256"
 
 
 
jwtRoute = APIRouter()
 
# this function will create the token
# for particular data
def create_access_token(data: dict):
    to_encode = data.copy()
     
    # expire time of the token
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
     
    # return the generated token
    return encoded_jwt
 

def get_token(userId:str):
    # data to be signed using token
    data = {
        'info': 'secret information',
        'from': 'GFG',
        'userId':userId
    }
    token = create_access_token(data=data)
    return {'token': token}
 
# the endpoint to verify the token
@jwtRoute.post("/verify_token")
async def verify_token(token: str):
    try:
        # try to decode the token, it will 
        # raise error if the token is not correct
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException( 
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
