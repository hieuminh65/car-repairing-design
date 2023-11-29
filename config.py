from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # HOST = os.getenv('HOST')
    # USER = os.getenv('USER_DB')
    # DATABASE = os.getenv('DATABASE')
    # PASSWORD = os.getenv('PASSWORD')
    HOST = "localhost"
    USER = "postgres"
    DATABASE = "final_project"
    PASSWORD = "Hieu652003psql"
    SECRET_KEY = os.getenv('SECRET_KEY')