from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    category = Column(String(50), nullable=False, index=True)
    difficulty = Column(String(20), nullable=False)
    points = Column(Integer, nullable=False)
    flag_hash = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
