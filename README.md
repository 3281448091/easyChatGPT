## EasyChatGpt

> An unofficial yet elegant interface of the ChatGPT API using browser automation that bypasses cloudflare detection and recaptchas.

## Install

```pip install easychatgpt```

## Usage

```python
from easychatgpt import ChatClient
import os

OPENAI_EMAIL = os.getenv("OPENAI_EMAIL")
OPENAI_PASSWORD = os.getenv("OPENAI_PASSWORD")

chat = ChatClient(OPENAI_EMAIL,OPENAI_PASSWORD)

answer = chat.interact("Introduce your self")

print(answer)
```