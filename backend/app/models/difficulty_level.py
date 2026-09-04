from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class DifficultyLevel(Base):
    __tablename__ = "difficulty_levels"

    id = Column(Integer, primary_key=True, index=True)
    game_id = Column(Integer, nullable=False)
    level = Column(String, nullable=False)  # 'easy', 'medium', 'hard'
    parameters = Column(Text)  # JSON string describing parameters for that level
    description = Column(Text)
