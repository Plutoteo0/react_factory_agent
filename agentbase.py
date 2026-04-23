from typing import TypedDict, Annotated
import operator

class AgentBase(TypedDict):
    specification: str
    generated_code: str
    critique: Annotated[list[str], operator.add]
    iteration_count: int