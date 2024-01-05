from sqlalchemy import select, or_, func, and_
from sqlalchemy.orm import Session
from typing import List, Optional

from piro_api.orm import User

def query_active_user_by_username(session: Session, username: str, register_id: Optional[int]) -> User:
    query = select(User).where(and_(User.username == username, User.isactive == 1))

    if register_id is not None:
        query = query.where(User.id != register_id)

    return session.scalars(query).first()



def query_active_user_by_email(session: Session, email: str, register_id: Optional[int]) -> User:
    query = select(User).where(and_(User.email == email, User.isactive == 1))

    if register_id is not None:
        query = query.where(User.id != register_id)

    return session.scalars(query).first()


def query_active_user_by_phone_number(session: Session, phone_number: str, register_id: Optional[int]) -> User:
    query = select(User).where(and_(User.phone_number == phone_number, User.isactive == 1))

    if register_id is not None:
        query = query.where(User.id != register_id)

    return session.scalars(query).first()
