from fastapi import FastAPI
from motor import motor_asyncio
import asyncio


# set up database
client = motor_asyncio.AsyncIOMotorClient("localhost", 27017)
db = client.EDU

# import own files
import database.py
import schema.py

webapp = FastAPI()


@webapp.get("/")
async def index():
    return {"hello": "world"}
