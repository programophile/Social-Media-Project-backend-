from .. import models,schemas,utils
from fastapi import FastAPI, status,Response ,HTTPException, Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import  get_db
from . import oauth2
from typing import Optional
from sqlalchemy import func
router=APIRouter(
    prefix='/posts',
    tags=['Posts']
)

@router.get("/",response_model=list[schemas.PostOut])
def get_posts(db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user),Limit : int=10,skip: int=0, search: Optional[str]="" ):
    # cursor.execute("SELECT * from posts")
    # posts=cursor.fetchall()
    # posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip)
    posts= db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    # print(posts)
    return  posts

@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate,db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user),Limit : int=10):
    # cursor.execute(
    #     """
    #     INSERT INTO posts (title, content, published)
    #     VALUES (%s, %s, %s)
    #     RETURNING *;
    #     """,
    #     (post.title, post.content, post.published)
    # )

    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    new_post=models.Post(owner_id=current_user.id,**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return  new_post
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("Select * from posts where id=%s ",(str(id)))
    # test_post=cursor.fetchone()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    return post


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session=Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    deleted_post=db.query(models.Post).filter(models.Post.id==id).first()

    # cursor.execute("delete from posts where id=%s returning *",(str(id),))
    # deleted_post=cursor.fetchone()
    # print(deleted_post)
    # conn.commit()
    if deleted_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,detail="Post not found"
        )
    if delete_post.owner_id!=current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to  perform this")
    db.delete(deleted_post)
    db.commit()
    return deleted_post

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.Post)
def update_post(
    id: int,
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    db_post = post_query.first()

    if db_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )

    if db_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this"
        )

    post_query.update(
        post.model_dump(),
        synchronize_session=False
    )

    db.commit()

    return post_query.first()