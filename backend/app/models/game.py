from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text)
    category = Column(String)  # 'memory', 'attention', 'sequence', 'pattern', 'reaction', 'language'
    difficulty_levels = Column(String)  # JSON-like string or comma-separated
    is_active = Column(Integer, default=1)
