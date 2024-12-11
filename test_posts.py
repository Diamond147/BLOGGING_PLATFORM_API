from fastapi.testclient import TestClient
from Blogging_Platform_API.main import app, Blog_data
from datetime import datetime
from unittest.mock import patch 

client = TestClient(app)

Mock_Blog_data = {
    "1": {
  "title": "My First Blog Post",
  "content": "This is the content of my first blog post.",
  "category": "Technology",
  "tags": ["Tech", "Programming"] }
}

@patch("Blogging_Platform_API.main", Mock_Blog_data)
def test_get_blog_post():
    response = client.get("/posts")
    assert response.status_code == 200
    assert response.json() == Mock_Blog_data

@patch("Blogging_Platform_API.main", Mock_Blog_data)
def test_get_blog_post_by_id():

    get_post_by_id = {
        "title": "My First Blog Post",
        "content": "This is the content of my first blog post.",
        "category": "Technology",
        "tags": ["Tech", "Programming"]
    }

    response = client.get("/posts/1")
    assert response.status_code == 200
    assert response.json() == get_post_by_id

@patch("Blogging_Platform_API.main", Mock_Blog_data)
def test_create_blog_post():

    create_post =  {
        "id": len(Mock_Blog_data)+1,
        "title": "title",
        "content": "content",
        "category": "category",
        "tags": "tags",
        "createdAt": datetime.now().isoformat(),
        "updatedAt": datetime.now().isoformat()
        }

    response = client.post("/posts", json = create_post)
    assert response.status_code == 201
    assert response.json() ["title"]== "title"
    assert response.json() ["content"]== "content"
    assert response.json() ["category"]== "category"
    # # assert response.json() == {"message": "Post created successfully", "detail":create_post}

@patch("Blogging_Platform_API.main", Mock_Blog_data)
def test_update_blog_post():
 
    update_post = {
        "title": "title",
        "content": "content",
        "category": "category",
        "tags": "tags"
    }   

    response = client.put("/posts/1", json = update_post)
    assert response.status_code == 200
    assert response.json() == update_post

@patch("Blogging_Platform_API.main", Mock_Blog_data)
def test_delete_blog_post():
    response = client.delete("/posts/1")
    assert response.status_code == 200 #204
    assert response.json() == {"message": "Post deleted successfully"}
    response = client.get("/posts/1")
    print(response.status_code)
    assert response.status_code == 400
    assert response.json() ["detail"]== "post not found"

@patch("Blogging_Platform_API.main", Mock_Blog_data)
def test_get_blog_post_not_found():
    response = client.delete("/posts/3")
    assert response.status_code == 404
    assert response.json() == {"detail": "Post not found"}