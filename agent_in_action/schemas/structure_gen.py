from typing import Optional, List, TypedDict

class UserInput(TypedDict):
    """class where a user input are given"""
    campaign_type:str
    product:list[str]
    rough_theme:str


class StructureBreaker(TypedDict):
    """This is the model where output is generated"""
    structured_data:str

class UserPromptBreakdown(TypedDict):
    """Breakdown the user prompt into below keys and variables"""
    campaign_type:Optional[str] 
    products:Optional[list[str]]
    location:Optional[str]
    language:Optional[str]
    Tone :Optional[str] 
    end_customer :Optional[str]