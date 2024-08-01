from sqlalchemy import create_engine, Column, String, JSON, DateTime
from sqlalchemy.dialects.sqlite import BLOB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:////Users/mohanakarthikeyan/Documents/Mohan/Projects/e-commerce/user_service/test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    user_id = Column(BLOB, primary_key=True, default=lambda: uuid.uuid4().bytes)
    email = Column(String, unique=True, index=True, nullable=False)
    mobile_number = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    address = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    auth_provider = Column(String, nullable=True)
    provider_id = Column(String, nullable=True)

Base.metadata.create_all(bind=engine)
