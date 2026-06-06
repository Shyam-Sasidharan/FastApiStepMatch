from datetime import datetime

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.core.security import verify_password
from app.models.user import User


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.scalar(select(User).where(User.id == user_id))


def authenticate_user(
    db: Session,
    identifier: str,
    password: str,
) -> User | None:
    normalized_identifier = identifier.strip().lower()
    user = db.scalar(
        select(User).where(
            or_(
                User.email == normalized_identifier,
                User.username == normalized_identifier,
            )
        )
    )

    if user is None or not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    user.last_login_at = datetime.now()
    db.commit()
    db.refresh(user)
    return user
