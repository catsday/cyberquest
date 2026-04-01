# CyberQuest — CTF Learning Platform

A capture-the-flag learning platform built with FastAPI + React + PostgreSQL.

## Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### 1. Database
```bash
createdb cyberquest
```

### 2. Backend
```bash
cd backend
cp .env.example .env        # edit DATABASE_URL / JWT_SECRET
pip install -r requirements.txt
python -m app.seed           # creates admin user + sample challenges
uvicorn app.main:app --reload
```

Backend runs at `http://localhost:8000`. API docs at `/docs`.

### 3. Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:5173` (proxies `/api` to backend).

### Default Credentials
- **Admin:** `admin` / `admin123`

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, PostgreSQL, JWT (python-jose), bcrypt
- **Frontend:** React 18, React Router, Axios, Vite
- **Auth:** JWT Bearer tokens, role-based access (user/admin)

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login, get JWT |
| GET | `/api/auth/me` | Current user info |
| GET | `/api/challenges/` | List challenges (filter by category/difficulty) |
| GET | `/api/challenges/:id` | Challenge detail |
| POST | `/api/challenges/:id/submit` | Submit flag |
| GET | `/api/challenges/:id/hints` | List hints |
| POST | `/api/challenges/:id/hints/:hid/unlock` | Unlock hint (penalty) |
| POST | `/api/teams/create` | Create team |
| POST | `/api/teams/join` | Join team by name |
| GET | `/api/leaderboard/` | Individual leaderboard |
| GET | `/api/teams/leaderboard` | Team leaderboard |
| POST | `/api/admin/challenges` | Create challenge (admin) |
| PUT | `/api/admin/challenges/:id` | Update challenge (admin) |
| DELETE | `/api/admin/challenges/:id` | Delete challenge (admin) |
| POST | `/api/admin/challenges/:id/hints` | Add hint (admin) |

## Project Structure
```
backend/
  app/
    main.py          # FastAPI entry
    config.py        # Settings
    database.py      # SQLAlchemy setup
    seed.py          # Test data seeder
    models/          # SQLAlchemy models
    schemas/         # Pydantic schemas
    routers/         # API routes
    middleware/      # JWT auth
frontend/
  src/
    App.jsx          # Routes
    api/client.js    # Axios instance
    context/         # Auth context
    pages/           # Page components
    components/      # Shared components
    styles/          # CSS
```
