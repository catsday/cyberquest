from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.score.desc()).limit(100).all()
    return [
        {"rank": i + 1, "username": u.username, "score": u.score}
        for i, u in enumerate(users)
    ]
