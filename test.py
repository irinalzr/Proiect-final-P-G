from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import models
from db_conn import get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

models.Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hey"}


def test_create_country():
    response = client.post(
        "/countries/", json={"name": "TestLand", "iso_code": "TL", "short_code": "999"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TestLand"
    assert data["iso_code"] == "TL"


def test_read_countries():
    response = client.get("/countries/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
