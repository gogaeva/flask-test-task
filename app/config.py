import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    MONGODB_URI = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017'
    MONGODB_USERNAME = os.environ.get('MONGODB_USERNAME') or 'flaskApp'
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD') or 'qwerty123'
