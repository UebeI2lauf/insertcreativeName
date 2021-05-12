from motor import motor_asyncio
import asyncio

client = motor_asyncio.AsyncIOMotorClient("localhost", 27017)
db = client.BDO


async def do_count():
    n = await db.dataset.count_documents({})
    print("%s documents in collection" % n)


loop = asyncio.get_event_loop()
loop.run_until_complete(do_count())
