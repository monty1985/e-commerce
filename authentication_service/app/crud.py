from sqlalchemy.orm import Session
from .database import User
from .models import UserCreate
from datetime import datetime
import uuid

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: bytes):
    return db.query(User).filter(User.user_id == user_id).first()

def create_user(db: Session, user: UserCreate, password_hash: str):
    db_user = User(
        id=str(uuid.uuid4()),  # Ensure this generates a UUID string
        email=user.email,
        mobile_number=user.mobile_number,
        password_hash=password_hash,
        first_name=user.first_name,
        last_name=user.last_name,
        address=user.address,
        auth_provider=user.auth_provider,
        provider_id=user.provider_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user