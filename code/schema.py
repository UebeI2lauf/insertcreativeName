# MongoDB base module -> ObjectId
from typing import Optional
from bson import ObjectId

# import pydantic stuff
from pydantic import BaseModel, Field
from pydantic.networks import EmailStr


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
    password: str = Field(...)
    age: int = Field(...)
    gender: str = Field(...)
    question_id: int = 0

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Gustav Ganz",
                "username": "Gustav2589",
                "email": "ganzganz@gmail.com",
                "password": ",njs<dglknjökm.,m??8u",
                "age": "13",
                "gender": "m",
                "question_id": "0",
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


class LogIn(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "username": "Gustav Ganz",
                "password": "GlupGlup",
            }
        }


class Questions(BaseModel):
    id: PyMongoObjectID = Field(default_factory=PyMongoObjectID, alias="_id")
    nr: int = Field(...)
    Frage: str = Field(...)
    Antwort_One: str = Field(...)
    Antwort_Two: str = Field(...)
    Antwort_Three: str = Field(...)
    Antwort_Four: str = Field(...)
    Richtig: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nr": "13",
                "Frage": "3 + 3",
                "Antwort_One": "16",
                "Antwort_Two": "5",
                "Antwort_Three": "8",
                "Antwort_Four": "6",
                "Richtig": "4",
            }
        }


class RNDQuestions(BaseModel):
    Frage: str = Field(...)
    Antwort_One: str = Field(...)
    Antwort_Two: str = Field(...)
    Antwort_Three: str = Field(...)
    Antwort_Four: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "Frage": "3 + 3",
                "Antwort_One": "16",
                "Antwort_Two": "5",
                "Antwort_Three": "8",
                "Antwort_Four": "6",
            }
        }


class AnswereQuestion(BaseModel):
    id: PyMongoObjectID = Field(default_factory=PyMongoObjectID, alias="_id")
    Answere: int = Field(..., lt=5)
    Username: str = Field(...)
    question_nr: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {"Answere": "2", "Username": "ABC", "question_nr": "13"}
        }


class TokenData(BaseModel):
    username: Optional[str] = None
