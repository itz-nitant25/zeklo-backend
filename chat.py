from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Chat
from ai_engine import ask_ai

router = APIRouter()

GUEST_LIMIT = 100  # free messages

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/chat")
def chat(data: dict, db: Session = Depends(get_db)):
    guest_id = data.get("guest_id")
    message = data.get("message")

    if not guest_id or not message:
        return {"reply": "Invalid request"}

    used = db.query(Chat).filter(Chat.guest_id == guest_id).count()
    if used >= GUEST_LIMIT:
        return {
            "reply": "🚫 Free limit reached. Please sign up to continue with Zeklo."
        }

    reply = ask_ai(message)

    chat = Chat(
        guest_id=guest_id,
        message=message,
        response=reply
    )
    db.add(chat)
    db.commit()

    return {"reply": reply}
