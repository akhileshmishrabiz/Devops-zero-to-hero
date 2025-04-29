import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DB_LINK')
    SQLALCHEMY_TRACK_MODIFICATIONS = False