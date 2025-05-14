from pydantic import BaseModel


# class GenerateScript(BaseModel):
#     """This is the model where output is generated"""
#     script:str

class GenerateScript(BaseModel):
    """This is the model where output is generated"""
    script:str
    hashtags:str