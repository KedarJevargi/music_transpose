from pydantic import BaseModel, Field, EmailStr
from typing import Annotated, Optional


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
    name: str
    token_type: str
    message: str



class ForgotPasswordRequest(BaseModel):
    email: Annotated[
        EmailStr,
        Field(..., description="Email of the user requesting password reset")
    ]

class ResetPasswordRequest(BaseModel):
    token: Annotated[
        str,
        Field(..., description="Password reset token received by email")
    ]
    new_password: Annotated[
        str,
        Field(..., min_length=6, description="New password for the user")
    ]

class MessageResponse(BaseModel):
    message: str