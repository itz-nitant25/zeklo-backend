from sqlalchemy import Column, Integer, String
from database import Base

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    guest_id = Column(String, index=True)
    message = Column(String)
    response = Column(String)
