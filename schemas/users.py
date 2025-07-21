from pydantic import BaseModel, Field, EmailStr
from typing import Annotated


class UserSignin(BaseModel):
    email: Annotated[
        EmailStr,
        Field(...,description="Email of the user")
    ]
    password: Annotated[
        str,
        Field(...,min_length=6, description="User Password")
    ]


class UserSignup(BaseModel):
    name: Annotated[
        str,
        Field(...,max_length=50, description="Name of the user")
    ]
    email: Annotated[
        EmailStr,
        Field(...,description="Email of the user")
    ]
    password: Annotated[
        str,
        Field(...,min_length=6, description="Password of the user")
    ]


class SignUpResponse(BaseModel):
    name: Annotated[
        str,
        Field(...,max_length=50, description="Name of the user")
    ]
    email: Annotated[
        EmailStr,
        Field(...,description="Email of the user")
    ]
class SignInResponse(BaseModel):
    access_token: str
    token_type: str
    message: str   # <== This is missing from your actual return





