import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_NAME=os.getenv('DB_NAME')
DB_HOST=os.getenv('DB_HOST')
DB_PASSWORD=os.getenv('DB_PASSWORD')
DB_DIALECT=os.getenv('DB_DIALECT')
DB_USER=os.getenv('DB_USER')

print(os.getenv('SPAM'))
URL_CONNECTION = '{DB_DIALECT}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
engine = create_engine(URL_CONNECTION)
localSession = sessionmaker(autoflush=false,autocommit=false,bind=engine)

Base = declarative_base
print('hola')