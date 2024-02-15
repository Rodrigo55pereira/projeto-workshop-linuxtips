from typing import List
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from pamps.auth import AuthenticatedUser
from pamps.db import ActiveSession
from pamps.models.post import (
Post,
PostRequest,
PostResponse,
PostResponseWithReplies,
)
from pamps.models.user import User

post_router = APIRouter()

@post_router.get("/", summary="Posts cadastrados", response_model=List[PostResponse])
async def list_post(*, session: Session = ActiveSession):
    """List all post without replies"""
    query = select(Post).where(Post.parent == None)
    posts = session.exec(query).all()
    return posts

@post_router.get("/{post_id}/", summary="Trazer post pelo ID", response_model=PostResponseWithReplies)
async def get_post_by_post_id(
    *,
    session: Session = ActiveSession,
    post_id:int,
):
    """Get post by post_id"""
    query = select(Post).where(Post.id == post_id)
    post = session.exec(query).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@post_router.get("/user/{username}/", summary="Receba postagens por nome de usuário", response_model=List[PostResponse])
async def get_posts_by_username(
    *,
    session: Session = ActiveSession,
    username: str,
    include_replies: bool = False,
):
    """ Get post by username """
    filters = [User.username == username]
    if not include_replies:
        filters.append(Post.parent == None)
    query = select(Post).join(User).where(*filters)
    posts = session.exec(query).all()
    return posts

@post_router.post("/", response_model=PostResponse, summary="Cadastar post" ,status_code=201)
async def create_post(
    *,
    session: Session = ActiveSession,
    user: User = AuthenticatedUser,
    post: PostRequest
):
    
    """ Creates new Post """

    post.user_id = user.id

    db_post = Post.from_orm(post) # transform PostRequest in Post
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post
