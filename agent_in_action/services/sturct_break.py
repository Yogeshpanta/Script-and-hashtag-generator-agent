from agent_in_action.schemas.structure_gen import UserInput, StructureBreaker, UserPromptBreakdown
from agent_in_action.prompts.prompt_templates import SystemPrompts

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json



import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

def structure_generator(state:UserInput):
    """Generates script based on userinput"""
    prompt = f"""I want to create a video for {state.campaign_type}, which should be suitable for the produts {"".join([i for i in state.product])}
You can use the following description to generate a script {state.rough_theme}
"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9, api_key=openai_api_key)
    response = llm([HumanMessage(content=prompt), SystemMessage(content=SystemPrompts.structure_breakdown_prompt)])

    return StructureBreaker(structured_data=response.content)


def parse_script_output(state: StructureBreaker) -> UserPromptBreakdown:
    """Parses JSON string into structured model"""
    parsed_dict = json.loads(state.structured_data)
    return UserPromptBreakdown(**parsed_dict)