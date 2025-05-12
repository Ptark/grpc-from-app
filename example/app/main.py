import re

from fastapi import FastAPI

from example.app.model.main import SelectUsersRequest, SelectUsersResponse

from .model import User


app = FastAPI()
my_users = [
    User(id=1, name="Max Mustermann", email="mm@example.de"),
    User(id=2, name="Helga Hedenhof", email="hh@example.at"),
    User(id=3, name="Captain Jack", email="js@piratebay.nl"),
    User(id=4, name="Herbert Hoover", email="hh@wh.com"),
]


@app.get("/")
def home() -> str:
    return "Hi, this app is for managing users."


@app.get("/users")
def users() -> list[User]:
    return my_users


@app.get("/users/{user_id}", response_model=User)
def user(user_id: int) -> User | None:
    for user in my_users:
        if user.id == user_id:
            return user
    return None


@app.post("/create_user", response_model=User)
def create_user(user: User) -> User | None:
    for my_user in my_users:
        if user == my_user:
            return None
    my_users.append(user)
    return user


@app.get("/select_users/", response_model=SelectUsersResponse)
def select_users(request: SelectUsersRequest) -> list[User]:
    def _is_selected(user: User, name_re, mail_re, is_active) -> bool:
        if name_re is not None and not name_re.search(user.name):
            return False
        if mail_re is not None and not mail_re.search(user.email):
            return False
        return is_active is None or is_active

    name_re = None
    if request.name_regex is not None:
        name_re = re.compile(request.name_regex)
    mail_re = None
    if request.mail_regex is not None:
        mail_re = re.compile(request.mail_regex)

    return [
        user
        for user in my_users
        if _is_selected(user, name_re, mail_re, request.is_active)
    ]
