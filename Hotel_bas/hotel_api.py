from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import date
from passlib.context import CryptContext
from database import SessionLocal, User, Booking

app = FastAPI()



pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    username: str
    password: str

class UserSignIn(BaseModel):
    username: str
    password: str

class BookingCreate(BaseModel):
    name: str
    check_in: date
    check_out: date
    room_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@app.post("/register/", status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return {"message": "User registered successfully"}

@app.post("/signin/")
def sign_in(user: UserSignIn, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return {"message": "Sign-in successful"}

@app.post("/bookings/")
def create_booking(booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = Booking(
        name=booking.name,
        check_in=booking.check_in,
        check_out=booking.check_out,
        room_type=booking.room_type
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.get("/bookings/")
def read_bookings(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    bookings = db.query(Booking).offset(skip).limit(limit).all()
    return bookings

@app.put("/bookings/{booking_id}")
def update_booking(booking_id: int, booking: BookingCreate, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db_booking.name = booking.name
    db_booking.check_in = booking.check_in
    db_booking.check_out = booking.check_out
    db_booking.room_type = booking.room_type
    db.commit()
    db.refresh(db_booking)
    return db_booking

@app.delete("/bookings/{booking_id}")
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    db_booking = db.query(Booking).filter(Booking.id == booking_id).first()
    if not db_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    db.delete(db_booking)
    db.commit()
    return {"message": "Booking deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
