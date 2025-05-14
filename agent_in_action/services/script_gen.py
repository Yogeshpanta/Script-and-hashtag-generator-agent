from agent_in_action.schemas.structure_gen import UserInput, UserPromptBreakdown
from agent_in_action.schemas.script_schema import GenerateScript
from agent_in_action.prompts.prompt_templates import SystemPrompts

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

import os
from dotenv import load_dotenv
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def script_generator(state:UserPromptBreakdown):
    """Generates script based on userinput"""
    prompt = f"""I want to create a video for {state.campaign_type}, which should be suitable for the produts {"".join([i for i in state.products])}
You can use the following description to generate a script:
Generate script in language: {state.language}, should be suitable for location {state.location}, tone: {state.Tone} and must target end customer: {state.end_customer}
Generate a compelling and engaging video script that aligns with these specifications.

"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9, api_key=openai_api_key)
    response = llm([HumanMessage(content=prompt), SystemMessage(content=SystemPrompts.script_generator_prompt)])
    return GenerateScript(script=response.content)