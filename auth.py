from fastapi import APIRouter
from passlib.hash import bcrypt
from database import SessionLocal
from models import User
import jwt, datetime

router = APIRouter(prefix="/auth")

SECRET = "CHANGE_THIS"

@router.post("/signup")
def signup(data: dict):
    db = SessionLocal()
    user = User(
        email=data["email"],
        password=bcrypt.hash(data["password"])
    )
    db.add(user)
    db.commit()
    return {"status": "ok"}

@router.post("/login")
def login(data: dict):
    db = SessionLocal()
    user = db.query(User).filter(User.email == data["email"]).first()
    if not user or not bcrypt.verify(data["password"], user.password):
        return {"error": "Invalid credentials"}

    token = jwt.encode({
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)
    }, SECRET)

    return {"token": token}
