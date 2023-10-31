from uuid import UUID

from fastapi import Depends
from fastapi.security import APIKeyHeader

from ..helpers.router_decorator import add_element_to_api_detail


def auth():
    def decorator(cls):
        add_element_to_api_detail(cls, 'dependencies', Depends(get_current_user_id))
        return cls

    return decorator


def get_current_user_id(user_id: str = Depends(APIKeyHeader(name='auth-user-id', scheme_name='auth-user-id'))):
    return UUID(user_id)


def current_user_id():
    return Depends(get_current_user_id)
