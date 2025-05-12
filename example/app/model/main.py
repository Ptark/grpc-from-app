from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True


class SelectUsersRequest(BaseModel):
    name_regex: str | None = None
    mail_regex: str | None = None
    is_active: bool | None = None


class SelectUsersResponse(BaseModel):
    users: list[User]
