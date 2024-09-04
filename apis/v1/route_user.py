from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from database.session import get_db
from database.repository.user import create_new_user, get_user
from core.hashing import Hasher
from core.security import create_access_token
from schemas.token import Token
from schemas.user import UserCreate

router = APIRouter()


@router.post("/auth", response_model=Token)
def register_or_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = get_user(email=form_data.username, db=db)
    if user:
        if not Hasher.verify_password(form_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password")
        access_token = create_access_token(data={"sub": user.email})
        return {"access_token": access_token, "token_type": "bearer"}

    user_data = UserCreate(email=form_data.username, password=form_data.password)
    new_user = create_new_user(user=user_data, db=db)
    access_token = create_access_token(data={"sub": new_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    access_token = register_or_login(form_data, db)
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return access_token
