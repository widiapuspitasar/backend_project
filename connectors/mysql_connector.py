from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

username = os.getenv("DB_USERNAME")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
database = os.getenv("DB_NAME")
database_port = os.getenv("DB_PORT")


# Connect to the database
print("Connecting to the MySQL Database")
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{database_port}/{database}')

# Test the connection
connection = engine.connect()
Session = sessionmaker(connection)
print(f'Connected to the MySQL Database at {host}')