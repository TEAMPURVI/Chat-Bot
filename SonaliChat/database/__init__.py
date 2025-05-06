from motor.motor_asyncio import AsyncIOMotorClient
import config

# Database connection
vickdb = AsyncIOMotorClient(config.MONGO_URL)
vick = vickdb["VickDb"]["Vick"]
usersdb = vick["users"]    # Users Collection
chatsdb = vick["chats"]    # Chats Collection

# Import functions for use in other parts of the application
from .chats import *
from .admin import *
from .fsub import *
