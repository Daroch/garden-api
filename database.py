import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_DIALECT = os.getenv('DB_DIALECT')
DB_USER = os.getenv('DB_USER')

URL_CONNECTION = '{}://{}:{}@{}/{}'.format(
    DB_DIALECT, DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)
engine = create_engine(URL_CONNECTION)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base = declarative_base()

# Testing Enviroment
TEST_DB_NAME = "test_"+os.getenv('DB_NAME')
TEST_URL_CONNECTION = '{}://{}:{}@{}/{}'.format(
    DB_DIALECT, DB_USER, DB_PASSWORD, DB_HOST, TEST_DB_NAME)
