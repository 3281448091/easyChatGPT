from setuptools import find_packages
from setuptools import setup

setup(
    name="easychatgpt",
    version="0.0.8",
    license="GNU General Public License v2.0",
    author="LanLan",
    author_email="3281448091@proton.me",
    description="An unofficial yet elegant interface of the ChatGPT API using browser automation that bypasses cloudflare detection and recaptchas.",
    packages=find_packages("src"),
    package_dir={"": "src"},
    py_modules=["easychatgpt"],
    url="https://github.com/acheong08/ChatGPT",
    install_requires=[
        "selenium~=4.7.2",
        "undetected-chromedriver~=3.1.7",
        "pypasser",
        "pocketsphinx",
    ],
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)
