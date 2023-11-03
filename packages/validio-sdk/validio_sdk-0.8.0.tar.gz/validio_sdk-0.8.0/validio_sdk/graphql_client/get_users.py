from typing import List

from .base_model import BaseModel
from .fragments import UserDetails


class GetUsers(BaseModel):
    users: List["GetUsersUsers"]


class GetUsersUsers(UserDetails):
    pass


GetUsers.update_forward_refs()
GetUsersUsers.update_forward_refs()
