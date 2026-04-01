from sqlalchemy import Column, Integer, Text, ForeignKey
from app.database import Base


class Hint(Base):
    __tablename__ = "hints"

    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"), nullable=False)
    content = Column(Text, nullable=False)
    penalty = Column(Integer, nullable=False)
    order = Column(Integer, default=1)


class HintUsage(Base):
    __tablename__ = "hint_usages"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hint_id = Column(Integer, ForeignKey("hints.id"), nullable=False)
