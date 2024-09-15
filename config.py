import os

class Config:
    SECRET_KEY = 'your_secret_key_here'  # Replace with a real secret key
    SQLALCHEMY_DATABASE_URI = 'sqlite:///school.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
