from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
# from Blogging_Platform_API.db import Blog_data
from db import Blog_data

app = FastAPI()


class PostBase(BaseModel):
    title: str
    content: str
    category: str
    tags: str

class Post(PostBase):
    id: int
    createdAt: datetime
    updatedAt: datetime

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[str] = None 


@app.get("/posts")
def get_blog_posts():
    return Blog_data

@app.get("/posts/{id}")
def get_blog_post_by_id(id:int):
    if id not in Blog_data:
        raise HTTPException(status_code=400, detail="post not found")
    
    return Blog_data[id]

@app.post("/posts", status_code=201)
def create_blog_post(payload:PostCreate):
    for id, item in Blog_data.items():
        if item["title"] == payload.title or item["category"] == payload.category:
            raise HTTPException(status_code=404, detail="blog_post already exists")

    user_id = len(Blog_data) + 1
    new_user = Post(
        id=user_id,
        createdAt=datetime.now(),
        updatedAt=datetime.now(),
        **payload.model_dump()
    )
    Blog_data[user_id] = new_user.model_dump()
    # return {"message": "User created successfully", "detail":new_user} 
    return new_user


@app.put("/posts/{post_id}", status_code=200)
def update_blog_post(post_id: int, payload:PostUpdate):
    if post_id not in Blog_data:
        raise HTTPException(status_code=400, detail= "Post not Found")
    Blog_data[post_id] = payload.model_dump()
    return Blog_data[post_id]

@app.delete("/posts/{id}", status_code=200)
def delete_blog_post(id: int):
    if id in Blog_data:
        del Blog_data[id]
        return {"message": "Post deleted successfully"}
    raise HTTPException(status_code=404, detail="Post not found")
print("Post not found")