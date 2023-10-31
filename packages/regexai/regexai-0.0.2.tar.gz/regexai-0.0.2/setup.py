from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.2'
DESCRIPTION = 'Tranform regex into regexai'
LONG_DESCRIPTION = '''RegexAI is a user-friendly library powered by generative AI, simplifying regular expression use. It interprets plain language regex queries, making data extraction and text manipulation easy. Whether you're a beginner or pro, RegexAI adapts to your needs, streamlining regex tasks for enhanced efficiency and accessibility.'''

# Setting up
setup(
    name="regexai",
    version='0.0.2',
    author="Shreyash Rote",
    author_email="shreyashrote321@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['openai'],
    keywords=['openai', 'regex', 'pattern', 'text_analysis','text_preprocessing'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)