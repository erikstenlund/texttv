from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='texttv',
    version='0.1',
    description='A terminal SVT Text TV client',
    url='https://github.com/erikstenlund/texttv',
    author='Erik Stenlund',
    author_email='erikstenlund@protonmail.com',
    license='MIT',
    install_requires=['readchar'],
    packages=["texttv"],
    entry_points={
        "console_scripts": [
            "texttv = texttv:cli"
        ]
    },
)
