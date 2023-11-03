from pydantic import Field

from .base_model import BaseModel
from .fragments import WindowCreation


class CreateGlobalWindow(BaseModel):
    global_window_create: "CreateGlobalWindowGlobalWindowCreate" = Field(
        alias="globalWindowCreate"
    )


class CreateGlobalWindowGlobalWindowCreate(WindowCreation):
    pass


CreateGlobalWindow.update_forward_refs()
CreateGlobalWindowGlobalWindowCreate.update_forward_refs()
