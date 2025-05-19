from agent_in_action.schemas.structure_gen import UserInput, StructureBreaker, UserPromptBreakdown
from agent_in_action.prompts.prompt_templates import SystemPrompts
from agent_in_action.schemas.overall_state import AgentState

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import logging
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
#     prompt = f"""I want to create a video for {user_input['campaign_type']}, which should be suitable for the products {', '.join(user_input['product'])}
# You can use the following description to generate a script: {user_input['rough_theme']}
# """
    prompt = user_input.get("user_prompt")
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9, api_key=openai_api_key)
    response = llm.invoke([
        {"role": "system", "content": SystemPrompts.structure_breakdown_prompt},
        {"role": "user", "content": prompt}
    ])
    logging.info("structure has been broken down")
    structured_data = json.loads(response.content)
    # state["structured_data"] = structured_data
    state["messages"].append(AIMessage(content=f"Structured data created: {response.content}"))
    print(structured_data)
    state["structured_data"] = structured_data

    required_keyword = state["structured_data"]
    title = required_keyword.get("campaign_title","")
    print(title)
    # state["current_agent"] = "supervisor"  # Send back to supervisor
    return state


# def structure_generator(state: AgentState) -> AgentState:
#     """Agent specialized in structure analysis - breaks down user input into structured data"""
#     print("Agent 1: Analyzing and structuring user input.")
#     user_input = state["user_input"]
# #     prompt = f"""I want to create a video for {user_input['campaign_type']}, which should be suitable for the products {', '.join(user_input['product'])}
# # You can use the following description to generate a script: {user_input['rough_theme']}
# # """
#     prompt = user_input.get("user_prompt")
#     # Enhanced system prompt that strictly enforces JSON output

#     llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.9, api_key=openai_api_key)  # Lower temperature for more predictable output
#     response = llm.invoke([
#         {"role": "system", "content": SystemPrompts.structure_breakdown_prompt},
#         {"role": "user", "content": prompt}
#     ])
    
#     # Debug - Print raw response
#     print(f"Raw LLM response: {response.content}")
    
#     try:
#         structured_data = json.loads(response.content)
#         state["structured_data"] = structured_data
#         state["messages"].append(AIMessage(content=f"Structured data created: {response.content}"))
#         return state
#     except json.JSONDecodeError as e:
#         print(f"JSON parsing error: {e}")
#         # Attempt to clean and fix the response
#         cleaned_response = clean_json_response(response.content)
        
#         try:
#             structured_data = json.loads(cleaned_response)
#             state["structured_data"] = structured_data
#             state["messages"].append(AIMessage(content=f"Structured data created (after fixing): {cleaned_response}"))
#             return state
#         except json.JSONDecodeError as e2:
#             # If cleaning didn't work, create a fallback minimal structure
#             print(f"Failed to parse JSON even after cleaning: {e2}")
#             fallback_data = {
#                 "campaign_type": None,
#                 "products": None,
#                 "location": None,
#                 "language": None,
#                 "Tone": None,
#                 "end_customer": None,
#                 "mode": None,  # Default to script mode
#                 "steps": [False]
#             }
#             state["structured_data"] = fallback_data
#             state["messages"].append(AIMessage(content=f"Using fallback structure due to parsing error: {fallback_data}"))
#             print(state["structured_data"])
#             return state