from typing import Dict
from pydantic import BaseModel, Field
from bson import ObjectId
from pydantic.networks import EmailStr


class PyMongoObjectID(ObjectId):
    @classmethod
    def __get_validation__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, value):
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid objectID")
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
        json_encoders = {PyMongoObjectID: str}


class Questions(ObjectId):
    id: PyMongoObjectID = Field(default_factory=PyMongoObjectID, alias="_id")
    nr: int = Field(...)
    author: PyMongoObjectID = Field(default_factory=PyMongoObjectID, alias="_id")
    subject: str = Field(...)
    author_id: int = Field(...)
