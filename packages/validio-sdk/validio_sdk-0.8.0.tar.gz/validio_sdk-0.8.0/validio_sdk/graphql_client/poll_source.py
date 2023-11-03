from typing import List, Optional

from pydantic import Field

from .base_model import BaseModel
from .enums import SourceState
from .fragments import ErrorDetails


class PollSource(BaseModel):
    source_poll: Optional["PollSourceSourcePoll"] = Field(alias="sourcePoll")


class PollSourceSourcePoll(BaseModel):
    errors: List["PollSourceSourcePollErrors"]
    state: Optional[SourceState]


class PollSourceSourcePollErrors(ErrorDetails):
    pass


PollSource.update_forward_refs()
PollSourceSourcePoll.update_forward_refs()
PollSourceSourcePollErrors.update_forward_refs()
