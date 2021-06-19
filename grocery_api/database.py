import pymysql
import os
import grocery_api.secrets as secrets
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

#GROCERY_DATABASE = f"mysql+pymysql://{secrets.dbuser}:{secrets.dbpass}@{secrets.dbhost}/{secrets.dbname}"
GROCERY_DATABASE = os.getenv('DATABASE_URI')

engine = create_engine(GROCERY_DATABASE, pool_pre_ping=True, pool_recycle=30)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = scoped_session(SessionLocal)

Base = declarative_base()
Base.query = db_session.query_property()