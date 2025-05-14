from pydantic import BaseModel
from typing import Optional, List


class UserInput(BaseModel):
    """class where a user input are given"""
    campaign_type:str
    product:list[str]
    rough_theme:str

class StructureBreaker(BaseModel):
    """This is the model where output is generated"""
    structured_data:str

class UserPromptBreakdown(BaseModel):
    """Breakdown the user prompt into below keys and variables"""
    campaign_type:Optional[str] 
    products:Optional[list[str]]
    location:Optional[str]
    language:Optional[str]
    Tone :Optional[str] 
    end_customer :Optional[str]