# import std modules
from typing import Dict, Optional
import asyncio

# Import fastAPI modules
from fastapi import FastAPI, status, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

# Import Pydantic modules
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


# Import MongoDB modules
from motor import motor_asyncio
from bson import ObjectId


# Side Note the uvicorn server is the main instance
# The normal __name__ == "__main__" would reult in False
# This code is more like a "Module"

# set up database
client = motor_asyncio.AsyncIOMotorClient("localhost", 27017)
db = client.EDU
# create the web application itself
webapp = FastAPI()


class PyMongoObjectID(ObjectId):
    # Wir erben von ObjectID
    # durch das erschaffen des Objects wird automatische eine _id erzeugt
    # diese wird dann hier validiert
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid objectid")
        return ObjectId(value)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyMongoObjectID = Field(default_factory=PyMongoObjectID, alias="_id")
    name: str = Field(...)
    username: str = Field(...)
    email: EmailStr = Field(...)
    age: int = Field(...)
    gender: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Gustav Ganz",
                "username": "Gustav2589",
                "email": "ganzganz@gmail.com",
                "age": "13",
                "gender": "m",
            }
        }


class UpdateUser(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    age: int = Field(...)
    gender: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Gustav Ganz",
                "email": "ganzganz@gmail.com",
                "age": "13",
                "gender": "m",
            }
        }


class Questions(ObjectId):
    id: PyMongoObjectID = Field(default_factory=PyMongoObjectID, alias="_id")
    nr: int = Field(...)
    author: PyMongoObjectID = Field(default_factory=PyMongoObjectID, alias="_id")
    subject: str = Field(...)
    author_id: int = Field(...)


@webapp.post("/", response_description="Add a user", response_model=User)
async def create_user(user: User = Body(...)):
    user = jsonable_encoder(user)
    new_user = await db["user"].insert_one(user)
    lookup_new_user = await db["user"].find_one({"_id": new_user.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=lookup_new_user)


@webapp.get("/{username}", response_description="Lookup a User", response_model=User)
async def show_student(username: str):
    if (user := await db["user"].find_one({"username": username})) is not None:
        return user
    else:
        raise HTTPException(
            status_code=404, detail=f"User {username} wurde nicht gefunden"
        )


@webapp.post("/{username}", response_description="mod User", response_model=User)
async def update_user(username: str, user: UpdateUser = Body(...)):
    user = {
        key: value for key, value in user.dict().items() if value is not None
    }  # We build a new dict with theb old values
    if len(user) >= 1:
        change = await db["user"].update_one({"username": username}, {"$set": user})
        if change.modified_count == 1:
            if (
                changed := await db["user"].find_one({"username": username})
            ) is not None:
                return changed

    if (user_is_there := await db["user"].find_one({"username": username})) is not None:
        return user_is_there
    raise HTTPException(status_code=404, detail=f"Unable to find User {username}")
