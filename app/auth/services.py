from fastapi import Depends

from app.auth.use_cases import register_user, login_user, logout_user


def response_message():
    return {"success": True, "data": {}}


def genera_response(response):
    response_body = response_message()
    if response["status_code"] != 200:
        response_body["success"] = False

    response_body["status_code"] = response["status_code"]
    response_body["data"] = response["response"]

    return response_body


async def register_user_service(response: dict = Depends(register_user)):
    return genera_response(response)


async def login_user_service(response: dict = Depends(login_user)):
    return genera_response(response)


async def logout_service(response: dict = Depends(logout_user)):
    return genera_response(response)
