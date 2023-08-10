from pydantic import BaseModel, validator
from pydantic import EmailStr


# user creation
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    @validator("password", always=True)
    def validate_password1(cls, value):
        password = value
        min_length = 3
        errors = ""
        if len(password) < min_length:
            errors += "Password must be at least 5 characters long. "
        if not any(character.isupper() for character in password):
            errors += (
                "Password should contain at least one lowercase character."
            )
        if errors:
            raise ValueError(errors)
        return value


# returning user
class ShowUser(BaseModel):
    username: str
    email: EmailStr
    # password: str

    class Config:
        orm_mode = True
