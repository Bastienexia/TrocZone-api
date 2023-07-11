from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr

class OAuth2TokenForm(OAuth2PasswordRequestForm):
    def __init__(
        self,
        grant_type: str = Form(default="password", regex="password|refresh_token"),
        username: str | None = Form(default=None),
        password: str | None = Form(default=None),
        refresh_token: str | None = Form(default=None),
        scope: str = Form(default=""),
        client_id: str | None = Form(default=None),
        client_secret: str | None = Form(default=None)
    ):
        super().__init__(
            grant_type, username, password, scope, client_id, client_secret
        )
        self.refresh_token = refresh_token
        self.validate()

    def validate(self):
        grant_type = self.grant_type
        if grant_type == "password":
            if self.username is None:
                raise ValueError("Username should not be empty")
            if self.password is None:
                raise ValueError("Password should not be empty")
        elif grant_type == "refresh_token":
            if self.refresh_token is None:
                raise ValueError("refresh_token should not be empty")
        else:
            raise ValueError("Invalid grant_type")
        return True


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int


class RefreshToken(BaseModel):
    refresh_token: str
    email: str


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    