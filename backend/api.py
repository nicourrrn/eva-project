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
async def get_user(request: Request):
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
async def main():
    return {"Access": "OK"}

