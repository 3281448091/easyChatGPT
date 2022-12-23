import asyncio

from wechaty_puppet_itchat import PuppetItChat
from wechaty_puppet import PuppetOptions
from wechaty import Wechaty, WechatyOptions, wechaty

from src.easychatgpt.chatgpt import ChatClient

import os

OPENAI_EMAIL = os.getenv("OPENAI_EMAIL")
OPENAI_PASSWORD = os.getenv("OPENAI_PASSWORD")


chat = ChatClient(OPENAI_EMAIL,OPENAI_PASSWORD,headless=False)


class MyBot(Wechaty):
    async def on_message(self, msg : wechaty.Message):
        print(type(msg))
        print(msg.room())
        #if msg.text().startswith("@懒懒"):

        # replies to every message
        talker = msg.talker() if msg.room() is None else msg.room()
        reply = chat.interact(msg.text().replace("@懒懒", ""))
        print(reply)
        await talker.say(reply)



async def main():
    options = WechatyOptions(
        puppet=PuppetItChat(PuppetOptions())
    )
    bot = MyBot(options=options)
    await bot.start()

asyncio.run(main())

