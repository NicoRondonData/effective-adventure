from app.auth.base import UserManagerProtocol, TokenProtocol
from app.auth.models import UserBaseModel
from contextlib import asynccontextmanager
from logger import logger

from app.auth.token import decode_jwt
from app.db.base import get_session


async def register_user_process(user: UserBaseModel, manager: UserManagerProtocol):
    async with asynccontextmanager(get_session)() as db_session:
        user_record = await manager(db_session).create_user(user)

        if not user_record:
            logger.error(f"The {user.dict()} was not created")
            return

        await db_session.commit()
        return user_record


async def login_process(user: UserBaseModel, manager: TokenProtocol):
    async with asynccontextmanager(get_session)() as db_session:
        token_record = await manager(db_session).create_token(user)

        if not token_record:
            logger.error(f"The token for the user_id:  {user.id}  was not created")
            return

        await db_session.commit()
        return token_record


async def logout_process(token:str, token_manager: TokenProtocol):
    async with asynccontextmanager(get_session)() as db_session:
        validate_record = await token_manager(db_session).validate_token(token)
        decode_token = decode_jwt(token)
        user_id = decode_token["id"]
        delete_tokens = await token_manager(db_session).delete_tokens(user_id)
        if validate_record:
            pass



        await db_session.commit()
        return validate_record
