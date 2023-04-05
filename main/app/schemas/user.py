from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    name: str

    class Config:
        orm_mode = True


class UserRequest(BaseUserSchema):
    pass


class UserResponse(BaseUserSchema):
    id: int
    balance: float = 0.0


class UserBalanceResponse(BaseModel):
    balance: float = 0.0
