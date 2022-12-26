
# EasyChatGPT
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)

An unofficial yet elegant interface of the ChatGPT API using browser automation that bypasses cloudflare detection and recaptchas.
## Features

- [x] Bypass Cloudflare's anti-bot protection using `undetected_chromedriver`
- [x] Complementary and fast Audio Recaptcha solver using the `pypasser` library.



## Installation

You must **install** ffmpeg and ffprobe on your machine before running.

[Install On Windows](https://phoenixnap.com/kb/ffmpeg-windows)\
[Install On Linux](https://www.golinuxcloud.com/ubuntu-install-ffprobe/)\
[Install On MacOS](https://bbc.github.io/bbcat-orchestration-docs/installation-mac-manual/)

Install the offical easyChatGPT package
```bash
pip install easychatgpt
```


    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`OPENAI_EMAIL`

`OPENAI_PASSWORD`

Copy the .env file and put in your openai email and password
```
cp .env.example .env
```


## Usage / Demo

Simple Usage

```python
from easychatgpt import ChatClient
import os
from dotenv import load_dotenv


load_dotenv()
OPENAI_EMAIL = os.getenv("OPENAI_EMAIL")
OPENAI_PASSWORD = os.getenv("OPENAI_PASSWORD")

chat = ChatClient(OPENAI_EMAIL,OPENAI_PASSWORD)

answer = chat.interact("Introduce your self")

print(answer)
```

[More examples to look at](https://github.com/LanLan69/easyChatGPT/tree/main/examples)
## Acknowledgement

[ChatGPT_Selenium](https://github.com/ugorsahin/ChatGPT_Selenium)\
[PyPasser](https://github.com/xHossein/PyPasser)
