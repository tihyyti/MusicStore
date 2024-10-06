import os
from dotenv import load_dotenv
from datetime import timedelta

# app/config.py

# Load environment variables from a .env file
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
    SESSION_FILE_DIR = os.environ.get('SESSION_FILE_DIR', os.path.join(os.path.dirname(__file__), 'session_files'))
    SESSION_PERMANENT = os.environ.get('SESSION_PERMANENT', 'False').lower() in ['true', '1', 't']
    SESSION_USE_SIGNER = os.environ.get('SESSION_USE_SIGNER', 'True').lower() in ['true', '1', 't']
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=int(os.environ.get('PERMANENT_SESSION_LIFETIME', 30)))