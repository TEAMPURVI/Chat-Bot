import importlib

from pyrogram import idle

from SonaliChat import app
from SonaliChat.modules import ALL_MODULES

async def boot():
    await app.start()

    for module in ALL_MODULES:
        importlib.import_module(f"SonaliChat.modules.{module}")

    await idle()
    await app.stop()

if __name__ == "__main__":
    app.run(boot())
