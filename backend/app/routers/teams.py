from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel
from app.database import get_db
from app.models import Team, User
from app.middleware.jwt_auth import get_current_user

router = APIRouter(prefix="/api/teams", tags=["teams"])


class TeamCreate(BaseModel):
    name: str


class TeamJoin(BaseModel):
    name: str


@router.post("/create", status_code=201)
def create_team(
    data: TeamCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.team_id:
        raise HTTPException(400, "Already in a team")
    if db.query(Team).filter(Team.name == data.name).first():
        raise HTTPException(400, "Team name taken")
    team = Team(name=data.name)
    db.add(team)
    db.flush()
    user.team_id = team.id
    db.commit()
    return {"team_id": team.id, "name": team.name}


@router.post("/join")
def join_team(
    data: TeamJoin,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if user.team_id:
        raise HTTPException(400, "Already in a team")
    team = db.query(Team).filter(Team.name == data.name).first()
    if not team:
        raise HTTPException(404, "Team not found")
    user.team_id = team.id
    db.commit()
    return {"team_id": team.id, "name": team.name}


@router.get("/leaderboard")
def team_leaderboard(db: Session = Depends(get_db)):
    results = (
        db.query(Team.name, func.sum(User.score).label("total_score"))
        .join(User, User.team_id == Team.id)
        .group_by(Team.id)
        .order_by(func.sum(User.score).desc())
        .limit(50)
        .all()
    )
    return [{"team": r.name, "score": r.total_score or 0} for r in results]
