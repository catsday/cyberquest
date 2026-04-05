from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, challenges, hints, teams, leaderboard, admin

# Create tables (dev only — use Alembic in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CyberQuest API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(challenges.router)
app.include_router(hints.router)
app.include_router(teams.router)
app.include_router(leaderboard.router)
app.include_router(admin.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}
