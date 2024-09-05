from sqlalchemy import create_engine, Column, Integer, String, Date
#from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import pyodbc

server = 'Pavan_Keladi\SQLEXPRESS'
database = 'Hotel'
driver = 'ODBC Driver 17 for SQL Server'

DATABASE_URL = f"mssql+pyodbc://@{server}/{database}?driver={driver.replace(' ', '+')}&Trusted_Connection=yes"
#DATABASE_URL = f"mssql+pyodbc://@{server}/{database}?driver={driver};Trusted_Connection=yes;"
#DATABASE_URL = "mssql+pyodbc://@{Pavan_Keladi//SQLEXPRESS}/Hotel?DRIVER={ODBC Driver 13 for SQL Server};Trusted_Connection=yes;"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)  # Specify a fixed length
    password = Column(String(128))  # Adjust the length as needed

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)  # Specify a fixed length
    check_in = Column(Date)
    check_out = Column(Date)
    room_type = Column(String(50))  # Specify a fixed length

Base.metadata.create_all(bind=engine)
