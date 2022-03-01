import os

from fastapi import (
    Request,
    status,
    responses
)
from fastapi.middleware.cors import CORSMiddleware
import pymongo.collection
from fastapi import FastAPI
from pymongo import MongoClient
import jwt
from pydantic import BaseModel

client = MongoClient("localhost", 27017)
users: pymongo.collection.Collection = client.eva_project.users

app = FastAPI()

origins = [
    "http://eva.centralus.cloudapp.azure.com/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/get_users")
async def get_user():
    statuses = []
    for user in users.find():
        statuses.append({"name": user["name"], "location": user["location"], **user["statuses"][-1]})
    return statuses


@app.middleware("http")
async def auth(request: Request, call_next):
    if (token := request.headers.get("Access-Token")) is None:
        return responses.JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    try:
        user_data = jwt.decode(token, key=os.getenv("ACCESS_KEY"), algorithms=["HS256"])
    except Exception as e:
        print(token)
        return responses.JSONResponse(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            content={"error": str(e)}
        )
    if user_data["username"] not in map(lambda u: u["username"], users.find()):
        return responses.JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED)
    return await call_next(request)


@app.get("/auth")
async def auth(request: Request):
    return {"Access": "OK", "Admin": is_admin(request)}

class User(BaseModel):
    name: str
    location: str
    username: str

def is_admin(request: Request):
    user_data = jwt.decode(
        token := request.headers.get("Access-Token"),
        key=os.getenv("ACCESS_KEY"), algorithms=["HS256"])
    return user_data["username"] == "nicourrrn"


@app.post("/new_user")
async def new_user(user: User, request: Request):
    if not is_admin(request):
        return responses.JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": "You not admin, how are you doing there?"})
    if user.username == "" or user.name == "" or user.location == "":
        return responses.JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST)

    users.insert_one({"name": user.name, "location": user.location,
                      "username": user.username, "statuses": [{"status": "Null", "scope": 0}]})

