from typing import Dict, Union
from http import HTTPStatus
from app.auth.base import UserManager, TokenManager
from app.auth.models import UserBaseModel, TokenBaseModel
from app.auth.process import register_user_process, login_process, logout_process
from logger import logger
from typing import Annotated

from fastapi import Header


async def register_user(user: UserBaseModel) -> Union[UserBaseModel, Dict]:
    try:
        user = await register_user_process(user=user, manager=UserManager)
        logger.info({"success": True, "response": user})
        return {
            "response": {
                "message": f"User {user.username} was registerd",
                "data": user,
            },
            "status_code": HTTPStatus.OK,
        }

    except Exception as e:
        logger.info(
            {
                "success": False,
                "response": "There was an error creating a user. " + str(e),
            }
        )
        return {
            "response": {
                "message": f"Was an error registering user",
            },
            "status_code": HTTPStatus.BAD_REQUEST,
        }


async def login_user(user: UserBaseModel) -> Union[UserBaseModel, Dict]:
    try:
        user = await login_process(user=user, manager=TokenManager)
        logger.info({"success": True, "response": user})
        return {
            "response": {
                "message": f"sucessfull login",
                "data": user,
            },
            "status_code": HTTPStatus.OK,
        }

    except Exception as e:
        logger.info(
            {
                "success": False,
                "response": "There was an error creating a token. " + str(e),
            }
        )
        return {
            "response": {
                "message": f"Was an error registering user",
            },
            "status_code": HTTPStatus.BAD_REQUEST,
        }


async def logout_user(token: Annotated[Union[str, None], Header()]) -> Union[UserBaseModel, Dict]:
    try:
        token = await logout_process(token=token, token_manager=TokenManager)
        print(token)

        if token:
            logger.info({"success": True, "response": token})
            return {
                "response": {
                    "message": f"User was logut",
                    "data": token,
                },
                "status_code": HTTPStatus.OK,
            }
        return {
            "response": {
                "message": f"Was an error logout user",
                "data": token,
            },
            "status_code": HTTPStatus.BAD_REQUEST,
        }

    except Exception as e:
        return {
            "response": {
                "message": f"Was an error logout user",
            },
            "status_code": HTTPStatus.BAD_REQUEST,
        }
