from httpx import AsyncClient
from sqlalchemy import insert, select
from models.models import user
from tests.conftest import async_session_maker


async def test_register(ac: AsyncClient):
    async with async_session_maker() as session:
        register_response = await ac.post(
            "/auth/register",
            json={
                "email": "login",
                "password": "password",
                "is_active": True,
                "is_superuser": False,
                "is_verified": False,
                "first_name": "string",
                "last_name": "string",
                "age": 777,
            },
        )
        query = select(user)
        result = await session.execute(query)
    assert len(result.all()) == 1
    assert register_response.status_code == 201


async def test_login(ac: AsyncClient):
    await ac.post(
        "/auth/register",
        json={
            "email": "login",
            "password": "password",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False,
            "first_name": "string",
            "last_name": "string",
            "age": 1,
        },
    )
    login_response = await ac.post(
        "/auth/jwt/login",
        data={
            "username": "login",
            "password": "password",
        },
    )
    assert login_response.status_code == 204


# async def test_create_profile(ac: AsyncClient):
#     await ac.post("/auth/register", json={
#         "email": "login",
#         "password": "password",
#         "is_active": True,
#         "is_superuser": False,
#         "is_verified": False,
#         "first_name": "string",
#         "last_name": "string",
#         "age": 777
#     })
#
#     login_response = await ac.post('/auth/jwt/login', data={
#         'username': 'login',
#         'password': 'password',
#     })
#     set_cookie_header = login_response.headers.get("set-cookie")
#
#     match = re.search(r"fastapiusersauth=([^;]+)", set_cookie_header)
#     print(set_cookie_header)
#     print(login_response.headers)
#     create_response = await ac.post(
#         '/acc/create',
#         data={
#             'title': 'Profile1',
#             'description': 'Super',
#             'profession': 'Prog',
#             'avatar': None
#         }
#     )
#
#     assert create_response.status_code == 204
