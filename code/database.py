# Import MongoDB modules
from motor import motor_asyncio

# set up database
client = motor_asyncio.AsyncIOMotorClient("localhost", 27017)
db = client.EDU
