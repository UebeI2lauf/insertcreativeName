from typing import List, Optional
from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic.types import Json


class PyMongoObjectID(ObjectId):
    @classmethod
    def __get_validation__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid objectID")
        return ObjectId(value)


class User(BaseModel):
    id: Optional[PyMongoObjectID] = Field(alias="_id")
    name: str
    username: str
    email: str
    age: int
    gender: str


class Questions(ObjectId):
    id: Optional[PyMongoObjectID] = Field(alias="id")
    nr: int
    author: str
    author_id: int
    submit_Date: int  # in milliseconds (Unix tinme?)
    last_modified: int  # see above
    last_modifier: str
    last_modifier_id: List  # need new validator ...
