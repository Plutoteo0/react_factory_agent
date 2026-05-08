from typing import TypedDict, Annotated
import operator


class AssemblerBase(TypedDict):
    current_file: str
    project_goal: str
    files_to_create: list[str]
    current_file_idx: int
    project_structure: Annotated[list, operator.add]
    iteration_count: int
    specification: str