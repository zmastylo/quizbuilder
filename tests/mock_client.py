"""FastAPI client mock."""

from fastapi.testclient import TestClient

from app.server import app
from database.repository import get_repository
from tests.mock_repository import get_mock_repository

app.dependency_overrides[get_repository] = get_mock_repository
test_client = TestClient(app)


def get_auth_client(
    username: str, password: str, endpoint: str = "/token"
) -> TestClient:
    """Creates Fast API test client. If valid credentials are supplied
    the client headers include bearer token, otherwise headers have no
    bearer token.
    :param username: User email
    :param password: Plaintext password
    :param endpoint: URL of the token endpoint
    :return: FastAPI test client"""

    auth_client = TestClient(app)

    response = auth_client.post(
        endpoint,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={"username": username, "password": password},
    )

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        auth_client.headers = {"Authorization": f"Bearer {access_token}"}

    return auth_client
