import hashlib
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Challenge, Hint, User
from app.schemas.challenge import ChallengeCreate
from app.middleware.jwt_auth import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"])


class HintCreate(BaseModel):
    content: str
    penalty: int
    order: int = 1


@router.post("/challenges", status_code=201)
def create_challenge(
    data: ChallengeCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    ch = Challenge(
        title=data.title,
        description=data.description,
        category=data.category,
        difficulty=data.difficulty,
        points=data.points,
        flag_hash=hashlib.sha256(data.flag.encode()).hexdigest(),
    )
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return {"id": ch.id, "title": ch.title}


@router.put("/challenges/{cid}")
def update_challenge(
    cid: int,
    data: ChallengeCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    ch = db.query(Challenge).filter(Challenge.id == cid).first()
    if not ch:
        raise HTTPException(404, "Not found")
    ch.title = data.title
    ch.description = data.description
    ch.category = data.category
    ch.difficulty = data.difficulty
    ch.points = data.points
    ch.flag_hash = hashlib.sha256(data.flag.encode()).hexdigest()
    db.commit()
    return {"id": ch.id, "title": ch.title}


@router.delete("/challenges/{cid}", status_code=204)
def delete_challenge(
    cid: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    ch = db.query(Challenge).filter(Challenge.id == cid).first()
    if not ch:
        raise HTTPException(404, "Not found")
    db.delete(ch)
    db.commit()


@router.post("/challenges/{cid}/hints", status_code=201)
def add_hint(
    cid: int,
    data: HintCreate,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    hint = Hint(
        challenge_id=cid,
        content=data.content,
        penalty=data.penalty,
        order=data.order,
    )
    db.add(hint)
    db.commit()
    return {"id": hint.id}
