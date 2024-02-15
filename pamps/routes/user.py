from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from pamps.db import ActiveSession
from pamps.models.user import User, UserRequest, UserResponse
from pamps.security import get_password_hash

user_router = APIRouter() #/user

@user_router.get("/", summary="Usuários cadastrados", response_model=List[UserResponse])
async def list_users(*, session: Session = ActiveSession):
    """List all users."""
    users = session.exec(select(User)).all()
    return users

@user_router.get("/{username}/", summary="trás usuário pelo nome", response_model=UserResponse)
async def get_user_by_username(*, session: Session = ActiveSession, username: str):
    """Get user by username"""
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    if not user:
       raise HTTPException(status_code=404, detail="User not found")
    return user

@user_router.post("/", summary="Cadastra usuário", response_model=UserResponse, status_code=201)
async def create_user(*, session: Session = ActiveSession, user: UserRequest):
    """Creates new user"""
    user.password = get_password_hash(user.password)
    print(user.password)
    db_user = User.from_orm(user) # transform UserRequest in User
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user