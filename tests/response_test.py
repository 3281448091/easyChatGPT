from src.easychatgpt.chatgpt import ChatClient
import os

OPENAI_EMAIL = os.getenv("OPENAI_EMAIL")
OPENAI_PASSWORD = os.getenv("OPENAI_PASSWORD")

chat = ChatClient(OPENAI_EMAIL,OPENAI_PASSWORD,headless=False)

answer = chat.interact("What is among us?")

print(answer)

answer = chat.interact("Why is 1 + 1")

print("answer")