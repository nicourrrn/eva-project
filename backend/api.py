import os

import jwt
import pymongo.collection
import time
from fastapi import (
    FastAPI,
    Request,
    status
)
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
users: pymongo.collection.Collection = client.eva_project.users
admin_username = os.getenv("ADMIN_USERNAME")

app = FastAPI()

origins = [
    "https://eva.centralus.cloudapp.azure.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def auth(request: Request, call_next):
    if (token := request.headers.get("Access-Token")) is None:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        user_data = jwt.decode(token, key=os.getenv("ACCESS_KEY"), algorithms=["HS256"])
    except Exception as e:
        print(token)
        return JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"error": str(e)}
        )
    is_register = user_data["username"] not in map(lambda u: u["username"], users.find())

    if is_register or is_admin(request):
        return await call_next(request)
    else:
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)

@app.get("/get_users")
async def get_user():
    return map(lambda user:
               {"name": user["name"], "location": user["location"], **user["statuses"][-1]},
               users.find())

@app.get("/auth")
async def auth(request: Request):
    return {"Admin": is_admin(request)}


class User(BaseModel):
    name: str
    location: str
    username: str

def is_admin(request: Request):
    user_data = jwt.decode(
        request.headers.get("Access-Token"),
        key=os.getenv("ACCESS_KEY"), algorithms=["HS256"])
    return user_data["username"] == admin_username

@app.post("/new_user")
async def new_user(user: User, request: Request):
    if not is_admin(request):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "You not admin, how are you doing there?"})
    if user.username == "" or user.name == "" or user.location == "":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST)

    users.insert_one({"name": user.name, "location": user.location,
                      "username": user.username, "statuses":
                          [{"status": "Null", "scope": 0, "time": int(time.time())}]})
