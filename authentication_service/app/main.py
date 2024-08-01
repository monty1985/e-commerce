from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import Token, UserCreate, UserOut
from .crud import create_user, get_user_by_email, get_user_by_id
from .utils.auth_utils import verify_password, get_password_hash, create_access_token, decode_access_token
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
import uuid
import logging

Base.metadata.create_all(bind=engine)

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=UserOut)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    try:
        db_user = create_user(db, user, hashed_password)
        return UserOut(
            user_id=db_user.id,
            email=db_user.email,
            mobile_number=db_user.mobile_number,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            address=db_user.address,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
            auth_provider=db_user.auth_provider,
            provider_id=db_user.provider_id
        )
    except IntegrityError as e:
        db.rollback()
        if "UNIQUE constraint failed: users.email" in str(e.orig):
            raise HTTPException(status_code=400, detail="Email already registered")
        elif "UNIQUE constraint failed: users.mobile_number" in str(e.orig):
            raise HTTPException(status_code=400, detail="Mobile number already registered")
        else:
            raise HTTPException(status_code=400, detail="Registration failed due to an integrity error")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/login", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserOut)
async def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    email = payload.get("sub")
    user = get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return UserOut.from_orm(user)