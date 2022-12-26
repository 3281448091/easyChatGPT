from src.easychatgpt.chatgpt import ChatClient
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_EMAIL = os.getenv("OPENAI_EMAIL")
OPENAI_PASSWORD = os.getenv("OPENAI_PASSWORD")


chat = ChatClient(OPENAI_EMAIL,OPENAI_PASSWORD,headless=False)

answer = chat.interact("What is among us?")

print(answer)
