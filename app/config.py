import os
from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# app/config.py

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
    'postgresql://postgres:password@localhost:5432/MStore_v1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ENVIRONMENT = "development"
    FLASK_APP = "app"
    FLASK_DEBUG = True
    SECRET_KEY = "0b6a3f3205bd3b63b803d815c938a981"
