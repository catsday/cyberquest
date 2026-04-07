import hashlib
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Challenge, Submission, User, HintUsage, Hint
from app.schemas.challenge import ChallengeOut, FlagSubmit
from app.middleware.jwt_auth import get_current_user
from typing import Optional
from typing import Optional, List


router = APIRouter(prefix="/api/challenges", tags=["challenges"])


@router.get("/", response_model=List[ChallengeOut])
def list_challenges(
    category: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    q = db.query(Challenge)
    if category:
        q = q.filter(Challenge.category == category)
    if difficulty:
        q = q.filter(Challenge.difficulty == difficulty)
    return q.all()


@router.get("/{challenge_id}", response_model=ChallengeOut)
def get_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    ch = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not ch:
        raise HTTPException(404, "Challenge not found")
    return ch


@router.post("/{challenge_id}/submit")
def submit_flag(
    challenge_id: int,
    data: FlagSubmit,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    ch = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not ch:
        raise HTTPException(404, "Challenge not found")

    already = db.query(Submission).filter(
        Submission.user_id == user.id,
        Submission.challenge_id == challenge_id,
        Submission.is_correct == True,
    ).first()
    if already:
        return {"correct": True, "message": "Already solved", "points_awarded": 0}

    flag_hash = hashlib.sha256(data.flag.encode()).hexdigest()
    is_correct = flag_hash == ch.flag_hash

    sub = Submission(user_id=user.id, challenge_id=challenge_id, is_correct=is_correct)
    db.add(sub)

    points_awarded = 0
    if is_correct:
        hint_ids = [
            h.id
            for h in db.query(Hint).filter(Hint.challenge_id == challenge_id).all()
        ]
        penalty = 0
        if hint_ids:
            used = db.query(HintUsage).filter(
                HintUsage.user_id == user.id, HintUsage.hint_id.in_(hint_ids)
            ).all()
            used_hint_ids = [u.hint_id for u in used]
            if used_hint_ids:
                penalty = sum(
                    h.penalty
                    for h in db.query(Hint).filter(Hint.id.in_(used_hint_ids)).all()
                )

        points_awarded = max(ch.points - penalty, 0)
        user.score += points_awarded

    db.commit()
    return {"correct": is_correct, "points_awarded": points_awarded}
