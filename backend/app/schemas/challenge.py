from pydantic import BaseModel


class ChallengeCreate(BaseModel):
    title: str
    description: str
    category: str
    difficulty: str
    points: int
    flag: str


class ChallengeOut(BaseModel):
    id: int
    title: str
    description: str
    category: str
    difficulty: str
    points: int

    class Config:
        from_attributes = True


class FlagSubmit(BaseModel):
    flag: str
