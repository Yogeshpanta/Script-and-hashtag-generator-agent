from agent_in_action.prompts.prompt_templates import SystemPrompts
from agent_in_action.schemas.hash_tag_schema import HashInput, HashTagOutput

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
def hash_tag_generator(state:HashInput):
    prompt = f"""Provide the top hashtags for these topics {state.input_list}"""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8, api_key=openai_api_key)
    response = llm(
        [SystemMessage(content=SystemPrompts.has_tag_prompt),
        HumanMessage(content=prompt)]
    )
    return HashTagOutput(hastag=response.content)