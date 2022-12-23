## EasyChatGPT

> An unofficial yet elegant interface of the ChatGPT API using browser automation that bypasses cloudflare detection and recaptchas.

## Install

```pip install easychatgpt```

## Features

- [x] Bypass Cloudflare's anti-bot protection using `undetected_chromedriver`
- [x] Audio Recaptcha solver

## Usage

Copy the .env file and put in your openai email and password
```bash
cp .env.example .env
```

Simple Usuage
```python
from easychatgpt.chatgpt import ChatClient
import os

OPENAI_EMAIL = os.getenv("OPENAI_EMAIL")
OPENAI_PASSWORD = os.getenv("OPENAI_PASSWORD")

chat = ChatClient(OPENAI_EMAIL,OPENAI_PASSWORD)

answer = chat.interact("Introduce your self")

print(answer)
```


## TODOS
1. Headless Support
2. Session login
3. Rapid Deploys