from threading import Thread
from collections.abc import Callable, Iterable, Mapping
from typing import Any, List, Optional
from enum import Enum

from pydantic import BaseModel, Field
import uuid

from humps.camel import case

class State(str, Enum):
    Waiting = "WAITING"
    Running = "RUNNING"
    Finished = "FINISHED"
    Error = "ERROR"


def create_uuid() -> str:
    return str(uuid.uuid4())


class LoggingRequest(BaseModel):
    id: str = Field(default_factory=create_uuid)
    root_repository: str
    submodule_names: List[str]
    start_ref: str
    end_ref: str
    json_uri: Optional[str] = None
    html_uri: Optional[str] = None
    state: State = State.Waiting
    error_message: Optional[str] = None
    stack_trace: Optional[str] = None

    class Config:
        alias_generator = case
        allow_population_by_field_name = True
        populate_by_name = True



