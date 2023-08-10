from pydantic import BaseModel


# model for token
class Token(BaseModel):
    access_token: str
    token_type: str
