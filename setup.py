from setuptools import setup, find_packages

setup(
    name="craftacoder",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "aider-chat", 
    ],
    entry_points={
        "console_scripts": [
            "craftacoder=cli.main:main",
        ],
    },
    author="Zoltán Csizmazia",
    author_email="cszoli81@gmail.com",
    description="craftacoder powered by aider",
)
