import os
from setuptools import setup, find_packages

setup(
    name = "whos-in",
    version = "0.0.1",
    author = "Brendon Lees",
    author_email = "brendon1555@gmail.com",
    description = ("A way to keep track of whos in the office"),
    url = "https://github.com/brendon1555/whos-in",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
    install_requires=[
        'flask-socketio==3.0.2',
        'flask-sqlalchemy==2.3.2',
        'flask-marshmallow==0.9.0',
        'marshmallow-sqlalchemy==0.14.1',
        'eventlet==0.24.1'
    ]
)