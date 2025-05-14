from pydantic import BaseModel
from typing import List

class HashInput(BaseModel):
    input_list:str

class HashTagOutput(BaseModel):
    hastag: List[str]