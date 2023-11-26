from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    HOST = os.getenv('HOST')
    USER = os.getenv('USER_DB')
    DATABASE = os.getenv('DATABASE')
    PASSWORD = os.getenv('PASSWORD')