from motor.motor_asyncio import AsyncIOMotorClient
import config

# Database connection
SonaliChat = AsyncIOMotorClient(config.MONGO_URL)
db = SonaliChat["SonaliChat"]  # Database
usersdb = db["users"]    # Users Collection
chatsdb = db["chats"]    # Chats Collection

# Import functions for use in other parts of the application
from .chats import *
from .admin import *
from .fsub import *
from .sonali import *
from .SonaliChat import *
