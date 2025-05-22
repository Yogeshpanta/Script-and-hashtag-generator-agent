from typing import List, TypedDict


class HashInput(TypedDict):
    input_list: str


class HashTagOutput(TypedDict):
    hastag: List[str]
