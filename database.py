import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

_DB_NAME=os.getenv('DB_NAME')
DB_HOST=os.getenv('DB_HOST')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_DIALECT=os.getenv('DB_DIALECT')
DB_USER=os.getenv('DB_USER')

def db_name():
    if os.getenv('RUN_ENV') == 'test':
        return 'test_' + _DB_NAME

    return _DB_NAME
      
      
URL_CONNECTION = '{}://{}:{}@{}/{}'.format(DB_DIALECT,DB_USER,DB_PASSWORD,DB_HOST,db_name())
engine = create_engine(URL_CONNECTION)
SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()