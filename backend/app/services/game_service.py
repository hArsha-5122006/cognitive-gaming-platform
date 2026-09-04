from sqlalchemy.orm import Session
from app.models.game_session import GameSession
from app.models.game_result import GameResult
from app.schemas.game import GameResultSubmit

def save_game_result(db: Session, patient_id: int, data: GameResultSubmit):
    # Create GameSession
    session = GameSession(
        patient_id=patient_id,
        game_id=data.game_id,
        score=data.score,
        accuracy=data.accuracy,
        time_taken_seconds=data.time_taken_seconds,
        mistakes=data.mistakes,
        attempts=data.attempts,
        difficulty_level=data.difficulty_level,
        status="completed"
    )
    db.add(session)
    db.flush()  # to get session.id

    # Optionally save individual results
    if data.results:
        for item in data.results:
            result = GameResult(
                session_id=session.id,
                question=item.question,
                correct_answer=item.correct_answer,
                user_answer=item.user_answer,
                is_correct=item.is_correct,
                reaction_time_ms=item.reaction_time_ms
            )
            db.add(result)

    db.commit()
    db.refresh(session)
    return session