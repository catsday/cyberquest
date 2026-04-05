"""
Seed script: creates an admin user and sample challenges.
Run: python -m app.seed
"""
import hashlib
from app.database import SessionLocal, engine, Base
from app.models import User, Challenge, Hint
from passlib.context import CryptContext

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Admin user
if not db.query(User).filter(User.username == "admin").first():
    admin = User(
        username="admin",
        email="admin@cyberquest.local",
        hashed_password=pwd_ctx.hash("admin123"),
        is_admin=True,
    )
    db.add(admin)

# Sample challenges
sample_challenges = [
    {
        "title": "Hello Flag",
        "description": "This is a warm-up. The flag is: FLAG{hello_cyberquest}",
        "category": "web",
        "difficulty": "easy",
        "points": 50,
        "flag": "FLAG{hello_cyberquest}",
        "hints": [
            {"content": "Read the description carefully.", "penalty": 10, "order": 1},
        ],
    },
    {
        "title": "Base64 Decode",
        "description": "Decode this: RkxBR3tiYXNlNjRfaXNfbm90X2VuY3J5cHRpb259",
        "category": "crypto",
        "difficulty": "easy",
        "points": 100,
        "flag": "FLAG{base64_is_not_encryption}",
        "hints": [
            {"content": "It's a common encoding, not encryption.", "penalty": 20, "order": 1},
            {"content": "Try CyberChef or the base64 command.", "penalty": 30, "order": 2},
        ],
    },
    {
        "title": "Hidden Header",
        "description": "The flag is hidden in the HTTP response headers of /api/health. Can you find it?",
        "category": "web",
        "difficulty": "medium",
        "points": 150,
        "flag": "FLAG{check_your_headers}",
        "hints": [
            {"content": "Use curl -v or browser DevTools.", "penalty": 30, "order": 1},
        ],
    },
    {
        "title": "ROT13 Classic",
        "description": "Decrypt: SYNT{ebg13_vf_abg_frpher}",
        "category": "crypto",
        "difficulty": "easy",
        "points": 75,
        "flag": "FLAG{rot13_is_not_secure}",
        "hints": [
            {"content": "Caesar would approve this cipher.", "penalty": 15, "order": 1},
        ],
    },
    {
        "title": "SQL Injection 101",
        "description": "A login form is vulnerable. The flag is in the 'secrets' table. Flag format: FLAG{...}. (Simulated — the flag is FLAG{sql_injection_basics})",
        "category": "web",
        "difficulty": "medium",
        "points": 200,
        "flag": "FLAG{sql_injection_basics}",
        "hints": [
            {"content": "Try ' OR 1=1 --", "penalty": 40, "order": 1},
            {"content": "Use UNION SELECT to read other tables.", "penalty": 50, "order": 2},
        ],
    },
]

for ch_data in sample_challenges:
    if not db.query(Challenge).filter(Challenge.title == ch_data["title"]).first():
        ch = Challenge(
            title=ch_data["title"],
            description=ch_data["description"],
            category=ch_data["category"],
            difficulty=ch_data["difficulty"],
            points=ch_data["points"],
            flag_hash=hashlib.sha256(ch_data["flag"].encode()).hexdigest(),
        )
        db.add(ch)
        db.flush()
        for hint_data in ch_data.get("hints", []):
            hint = Hint(
                challenge_id=ch.id,
                content=hint_data["content"],
                penalty=hint_data["penalty"],
                order=hint_data["order"],
            )
            db.add(hint)

db.commit()
db.close()
print("Seed complete: admin/admin123, 5 sample challenges created.")
