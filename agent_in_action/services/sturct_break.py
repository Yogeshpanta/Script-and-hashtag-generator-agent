from agent_in_action.schemas.structure_gen import UserInput, StructureBreaker, UserPromptBreakdown
from agent_in_action.prompts.prompt_templates import SystemPrompts
from agent_in_action.schemas.overall_state import AgentState

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import json



import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def structure_generator(state: AgentState) -> AgentState:
    """Agent specialized in structure analysis - breaks down user input into structured data"""
    print("Agent 1: Analyzing and structuring user input.")
    
    # user_input = state["user_input"]
    user_input = state["user_input"]
    prompt = f"""I want to create a video for {user_input['campaign_type']}, which should be suitable for the products {', '.join(user_input['product'])}
You can use the following description to generate a script: {user_input['rough_theme']}
"""
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=openai_api_key)
    response = llm.invoke([
        {"role": "system", "content": SystemPrompts.structure_breakdown_prompt},
        {"role": "user", "content": prompt}
    ])
    
    structured_data = json.loads(response.content)
    state["structured_data"] = structured_data
    state["messages"].append(AIMessage(content=f"Structured data created: {response.content}"))
    # state["current_agent"] = "supervisor"  # Send back to supervisor
    return state