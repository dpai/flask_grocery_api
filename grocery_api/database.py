from flask_sqlalchemy import SQLAlchemy
import pymysql
import secrets

db = SQLAlchemy()
GROCERY_DATABASE = f"mysql+pymysql://{secrets.dbuser}:{secrets.dbpass}@{secrets.dbhost}/{secrets.dbname}"