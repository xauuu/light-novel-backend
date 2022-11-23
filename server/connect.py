import motor.motor_asyncio
from server.config.config import settings

client = motor.motor_asyncio.AsyncIOMotorClient(settings.DATABASE_URL)

database = client.xauuu

user_collection = database.get_collection("users")
novel_collection = database.get_collection("novels")
genre_collection = database.get_collection("genres")
chapter_collection = database.get_collection("chapters")
comment_collection = database.get_collection("comments")
rating_collection = database.get_collection("ratings")
