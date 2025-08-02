import os

class Config:
    DATABASE_NAME = 'users.db'
    DEBUG = True
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'a-secret-key')
