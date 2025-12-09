# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'waniya-key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hotel.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False