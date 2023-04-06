from pydantic import BaseModel
from sqlmodel import Field, SQLModel, Index, ForeignKey, Relationship
from typing import Dict, List, Optional
from datetime import datetime
from passlib.context import CryptContext


class User(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"autoincrement": True},
    )
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_active: bool = Field(
        nullable=False,
        default=False,
        sa_column_kwargs={"server_default": "false"},
        description="Determine if the User is active",
    )
    username: str = Field(unique=True)
    password: str

    def set_password(self, password: str):
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.password = password_context.hash(password)

    def verify_password(self, password: str) -> bool:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        return password_context.verify(password, self.password)

    class Config:
        indexes = [
            Index("idx_user_username", "username", unique=True),
        ]


class UserBaseModel(BaseModel):
    username: str
    id: Optional[int]
    password: Optional[str]


class Token(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        nullable=False,
        sa_column_kwargs={"autoincrement": True},
    )
    token: str
    exp_date: datetime
    user_id: int = Field(
        ForeignKey(User.id, ondelete="CASCADE"),
        nullable=False,
        index=True,
        sa_column_kwargs={"onupdate": "CASCADE"},
    )

class TokenBaseModel(BaseModel):
    token: str
    exp_date: datetime
