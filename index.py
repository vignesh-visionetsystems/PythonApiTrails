from fastapi import FastAPI
from routes.user import user
from routes.roles import roles
from routes.technology import technologiesRouter
from routes.role_technology import roleTechnology
from routes.user_technolory import userTechnologiesRouter
from routes.autentication_token import jwtRoute
from routes.update_technology_status import userTechnologyStatus
from fastapi.middleware.cors import CORSMiddleware


app  = FastAPI()
# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # This should be more restrictive in a production environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user)
app.include_router(roles)
app.include_router(jwtRoute)
app.include_router(technologiesRouter)
app.include_router(roleTechnology)
app.include_router(userTechnologiesRouter)
app.include_router(userTechnologyStatus)




