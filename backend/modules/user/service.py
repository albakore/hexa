from typing import TypedDict

from .application.service.user import UserService


class UserServiceCollection(TypedDict):
	user_service: UserService
