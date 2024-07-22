from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal, engine, Base
from .models import UserCreate, UserOut, UserUpdate
from .crud import create_user as create_user_crud, update_user as update_user_crud, delete_user as delete_user_crud, get_user as get_user_crud
from .security import get_password_hash
from uuid import UUID

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return "Welcome to e-commerce Application"

@app.post("/users/register_user", response_model=UserOut)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user_crud(db, user, get_password_hash(user.password))
    return db_user

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = get_user_crud(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    return db_user

@app.put("/users/{user_id}", response_model=UserOut)
async def update_user(user_id: UUID, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user_crud(db, user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return db_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    db_user = delete_user_crud(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User Not Found")
    return {"detail": "User Deleted Successfully"}