from fastapi import FastAPI
from routes.user import user
from routes.roles import roles
app  = FastAPI()
app.include_router(user)
app.include_router(roles)



