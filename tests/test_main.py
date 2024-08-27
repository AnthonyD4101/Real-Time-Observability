import pytest, os
from dotenv import load_dotenv
from httpx import AsyncClient, ASGITransport
from unittest.mock import patch, MagicMock
from fastapi_project.main import app

load_dotenv()

def test_environment_variable():
    database_url = os.getenv("DATABASE_URL")
    assert database_url is not None

@pytest.mark.asyncio
async def test_main_root():
    transport = ASGITransport(app = app)
    async with AsyncClient(transport = transport, base_url = "http://test") as ac:
        response = await ac.get("/")
    
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

@pytest.mark.asyncio
async def test_health_check():
    transport = ASGITransport(app = app)
    async with AsyncClient(transport = transport, base_url="http://test") as ac:
        response = await ac.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.asyncio
@patch("fastapi_project.main.collection.insert_one")
async def test_create_user(mock_insert_one):
    mock_insert_one.return_value = MagicMock(inserted_id="mocked_user_id")
    
    user_info = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "testpassword"
    }
    
    transport = ASGITransport(app = app)
    async with AsyncClient(transport = transport, base_url="http://test") as ac:
        response = await ac.post("/addUser", json=user_info)
    
    assert response.status_code == 200
    assert response.json() == {"userID from account creation": "mocked_user_id"}
    
    mock_insert_one.assert_called_once_with(user_info)