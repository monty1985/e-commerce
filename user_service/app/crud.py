from sqlalchemy.orm import session
from .models import UserCreate, UserUpdate
from .database import User
from uuid import UUID

def create_user(db: session, user: UserCreate, password_hash: str):
    db_user = User(
        email=user.email,
        mobile_number= user.mobile_number,
        password_hash = password_hash,
        first_name = user.first_name,
        last_name = user.last_name,
        address = user.address
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: session, user_id: UUID):
    user_id_bytes = user_id.bytes
    return db.query(User).filter(User.user_id == user_id_bytes).first()

def update_user(db: session, user_id: UUID, user: UserUpdate):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user: # checking its not empty
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: session, user_id: UUID):
    db_user = db.query(User).filter(User.user_id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user