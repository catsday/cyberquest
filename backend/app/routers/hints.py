from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Hint, HintUsage, User
from app.middleware.jwt_auth import get_current_user

router = APIRouter(prefix="/api/challenges", tags=["hints"])


@router.get("/{challenge_id}/hints")
def get_hints(
    challenge_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    hints = (
        db.query(Hint)
        .filter(Hint.challenge_id == challenge_id)
        .order_by(Hint.order)
        .all()
    )
    used_ids = {
        u.hint_id
        for u in db.query(HintUsage).filter(HintUsage.user_id == user.id).all()
    }
    return [
        {
            "id": h.id,
            "order": h.order,
            "penalty": h.penalty,
            "content": h.content if h.id in used_ids else None,
            "unlocked": h.id in used_ids,
        }
        for h in hints
    ]


@router.post("/{challenge_id}/hints/{hint_id}/unlock")
def unlock_hint(
    challenge_id: int,
    hint_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    hint = (
        db.query(Hint)
        .filter(Hint.id == hint_id, Hint.challenge_id == challenge_id)
        .first()
    )
    if not hint:
        raise HTTPException(404, "Hint not found")
    already = (
        db.query(HintUsage)
        .filter(HintUsage.user_id == user.id, HintUsage.hint_id == hint_id)
        .first()
    )
    if already:
        return {"content": hint.content, "penalty": hint.penalty, "already_unlocked": True}
    usage = HintUsage(user_id=user.id, hint_id=hint_id)
    db.add(usage)
    db.commit()
    return {"content": hint.content, "penalty": hint.penalty, "already_unlocked": False}
