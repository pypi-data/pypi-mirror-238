from setuptools import setup, find_packages

setup(
    name="CommonTelegramUsers",
    version="0.2.2",
    packages=find_packages(),
    install_requires=[
        "pyrogram",
        "tgcrypto"
    ],
)
