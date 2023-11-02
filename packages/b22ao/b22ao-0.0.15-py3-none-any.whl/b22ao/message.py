from enum import Enum
from typing import Any, Dict

class State(Enum):
    Idle = "Idle"
    Running = "Running"
    Error = "Error"


class Message:
    def __init__(self, source: Any, state: State, msg: Dict=None):
        self.source = source
        self.state = state
        self.msg = msg
