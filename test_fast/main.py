from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

app = FastAPI()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

class Hotel(Base):
    __tablename__ = "hotels"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    price = Column(Integer)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class HotelCreate(BaseModel):
    name: str
    location: str
    price: int

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register/")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    new_user = User(username=user.username, password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username, User.password == user.password).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {"message": "Login successful", "user": db_user.username}

@app.post("/hotels/")
def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    new_hotel = Hotel(name=hotel.name, location=hotel.location, price=hotel.price)
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel

@app.get("/hotels/")
def get_hotels(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).all()
    return hotels

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    db.delete(hotel)
    db.commit()
    return {"message": "Hotel deleted successfully"}
