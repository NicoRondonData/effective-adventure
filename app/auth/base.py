import datetime
from abc import ABC, abstractmethod
from typing import Optional, Protocol, Union

from pydantic import BaseModel
from sqlalchemy import delete
from app.auth.models import UserBaseModel, User, Token, TokenBaseModel
from sqlmodel import select

from app.auth.token import generate_jwt, decode_jwt, is_valid_token


class UserManagerProtocol(Protocol):
    def __init__(self, session):
        ...

    async def get_by_username(self, username: str) -> Optional[BaseModel]:
        ...

    async def create_user(self, user: UserBaseModel) -> BaseModel:
        ...


class TokenProtocol(Protocol):
    async def create_token(self, user: UserBaseModel) -> BaseModel:
        ...

    async def validate_token(self, token: str) -> bool:
        ...



class UserManager:
    def __init__(self, session):
        self._session = session

    async def create_user(self, user: UserBaseModel) -> BaseModel:
        new_user = User(
            username=user.username,
            password=user.password
        )
        new_user.set_password(user.password)
        self._session.add(new_user)

        await self._session.flush()

        new_user_base_model = UserBaseModel(
            id=new_user.id,
            username=new_user.username
        )
        return new_user_base_model

    async def get_by_username(self, username: str) -> User:
        """
        :param username: username of the user to retrieve.
        :return: A user.
        """
        statement = select(User).where(User.username == username)
        results = (await self._session.execute(statement)).one_or_none()

        if not results:
            return None

        user_record = results[0]
        # user_base_model = UserBaseModel(
        #     username=user_record.username,
        #     id=user_record.id
        # )

        return user_record


class TokenManager:
    def __init__(self, session):
        self._session = session

    async def validate_token(self, token: str):
        return is_valid_token(token)

    async  def delete_tokens(self, user_id: int):
        delete_statement = delete(Token).where(Token.user_id == user_id)
        await self._session.execute(delete_statement)
        await self._session.flush()

    async def create_token(self, user: UserBaseModel) -> Union[TokenBaseModel, None]:
        user_manager = UserManager(self._session)
        get_user = await user_manager.get_by_username(username=user.username)

        if get_user:
            verify = get_user.verify_password(user.password)
            if verify:
                user_dict = user.dict()
                user_dict["id"] = get_user.id
                new_user_jwt = generate_jwt(data=user_dict)
                decode_token = decode_jwt(new_user_jwt)
                exp_datetime = datetime.datetime.utcfromtimestamp(decode_token["exp"])
                new_token = Token(
                    token=new_user_jwt,
                    exp_date=exp_datetime,
                    user_id=get_user.id
                )
                self._session.add(new_token)
                await self._session.flush()
                return TokenBaseModel(token=new_token.token, exp_date=new_token.exp_date)
            else:
                return None
        else:
            return None
