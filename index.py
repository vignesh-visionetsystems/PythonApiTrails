from fastapi import FastAPI
from routes.user import user
from routes.roles import roles
from routes.jwt_token import jwtRoute
app  = FastAPI()
app.include_router(user)
app.include_router(roles)
app.include_router(jwtRoute)



