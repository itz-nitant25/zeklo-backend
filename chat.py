from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Chat
from ai_engine import ask_ai
from image_gen import generate_image

router = APIRouter()

GUEST_LIMIT = 100

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 💬 CHAT (GUEST OR USER)
@router.post("/chat")
def chat(data: dict, db: Session = Depends(get_db)):
    message = data.get("message")
    guest_id = data.get("guest_id")
    user_id = data.get("user_id")

    if not message:
        return {"reply": "Invalid request"}

    # 🚫 BLOCK IMAGE PROMPTS FOR GUESTS
    if message.lower().startswith("image:") and not user_id:
        return {"reply": "🔒 Login required to generate images"}

    # 🧑‍🚀 GUEST MODE
    if guest_id and not user_id:
        used = db.query(Chat).filter(Chat.guest_id == guest_id).count()
        if used >= GUEST_LIMIT:
            return {"reply": "🚫 Free limit reached. Please sign up to continue."}

        reply = ask_ai(message)

        db.add(Chat(
            guest_id=guest_id,
            message=message,
            response=reply
        ))
        db.commit()

        return {"reply": reply}

    # 🔐 LOGGED-IN USER
    if user_id:
        reply = ask_ai(message)

        db.add(Chat(
            user_id=user_id,
            message=message,
            response=reply
        ))
        db.commit()

        return {"reply": reply}

    return {"reply": "Invalid request"}

# 🖼 IMAGE GENERATION (LOGIN ONLY)
@router.post("/image")
def image(data: dict):
    user_id = data.get("user_id")
    prompt = data.get("prompt")

    if not user_id:
        return {"error": "🔒 Login required"}

    if not prompt:
        return {"error": "Prompt missing"}

    url = generate_image(prompt)

    if not url:
        return {"error": "Image generation failed"}

    return {"image_url": url}
