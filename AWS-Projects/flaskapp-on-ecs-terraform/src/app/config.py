import os

class Config:
    # Get DB URL from AWS Secrets Manager
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Other configurations
    SECRET_KEY = "2b9c329a83c48c8def8c4304972b56c636d92914e627cce780fe4d9730d3a047"