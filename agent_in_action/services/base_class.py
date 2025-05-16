from agent_in_action.schemas.overall_state import AgentState
from agent_in_action.prompts.prompt_templates import SystemPrompts
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

from agent_in_action.services.hash_tag_gen import hash_tag_generator
from agent_in_action.services.script_gen import script_generator
from agent_in_action.services.trend_analysis import trending_keyword_generator

import os
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# def supervisor_node(state:AgentState):
#     """
#     Acts as the central controller that orchestrates the execution of other tool functions 
#     (script generation, trending keyword extraction, and hashtag generation) based on the 
#     structured data provided in the agent state.

#     This function reads key details such as mode, campaign type, and products from the 
#     `structured_data` field of the agent state to formulate a natural language prompt. 
#     It then invokes a language model (ChatOpenAI) that is configured with access to a set 
#     of tools: `script_generator`, `trending_keyword_generator`, and `hash_tag_generator`.

#     The language model determines the appropriate tools to call and sequences them 
#     accordingly to generate the required output (e.g., scripts, hashtags). The function 
#     appends an `AIMessage` to the `messages` list to log the supervisory action and the 
#     content generated or delegated to tools.

#     Args:
#         state (AgentState): The current state of the workflow, including user input, 
#                             structured data, and message history.

#     Returns:
#         AgentState: The updated agent state with a new AI message indicating that the 
#                     supervisor node has processed the input and triggered tool execution.

#     Raises:
#         KeyError: If `structured_data` or its required fields are missing from the state.
#         Exception: If tool invocation or LLM interaction fails.
#     """
#     details = state["structured_data"]

#     mode = details.get("mode", "scripts")
#     campaign_type = details.get("campaign_type", "marekting")
#     products = details.get("products", [])
#     product = ",".join([i for i in products])
#     # Language = details.get("language", "english")
#     # Location = details.get("location", "united states")
#     # Tone = details.get("Tone", "general")
#     # end_customer = details.get("end_customer", "15 to 50 age groups")
#     tools = [script_generator, hash_tag_generator, trending_keyword_generator]


#     prompt = f"""Hi, assitant. I wan to create {mode} for my video of type {campaign_type} and should based on proudcts like {product} """
#     llm_with_tools = ChatOpenAI(model="gpt-4o-mini", temperature=0.2, api_key=openai_api_key).bind_tools(tools)
#     response = llm_with_tools.invoke([
#         SystemMessage(content=SystemPrompts.node_executer_prompt),
#         HumanMessage(content=prompt)
#     ])
#     state["messages"].append(AIMessage(content=f"received a prompt from user executing node to generate {details.get('mode')}:{response.content}"))
#     return state

def supervisor_node(state: AgentState):
    """
    Acts as the central controller that orchestrates the execution of other tool functions
    (script generation, trending keyword extraction, and hashtag generation) based on the
    structured data provided in the agent state.
    
    This function reads key details such as mode, campaign type, and products from the
    `structured_data` field of the agent state and directly calls the appropriate tools
    based on the requested mode.
    
    Args:
        state (AgentState): The current state of the workflow, including user input,
        structured data, and message history.
        
    Returns:
        AgentState: The updated agent state after executing the requested tools.
        
    Raises:
        KeyError: If `structured_data` or its required fields are missing from the state.
        Exception: If tool invocation fails.
    """
    details = state["structured_data"]
    mode = details.get("mode")  # Default to script if not specified
    
    # Log the start of supervisor execution
    state["messages"].append(AIMessage(content=f"Supervisor node executing in {mode} mode"))
    
    # Execute based on mode
    if mode == "script" or mode == "scripts":
        # Generate script
        state = script_generator(state)
    elif mode == "hashtag" or mode == "hashtags":
        # For hashtags, we need to first get trending keywords, then generate hashtags
        state = trending_keyword_generator(state)
        if "trendy_keywords" in state and state["trendy_keywords"]:
            state = hash_tag_generator(state)
    elif mode == "both" or mode == "all":
        # Generate both script and hashtags
        state = script_generator(state)
        state = trending_keyword_generator(state)
        if "trendy_keywords" in state and state["trendy_keywords"]:
            state = hash_tag_generator(state)
    else:
        # Log unsupported mode
        state["messages"].append(AIMessage(content=f"Unsupported mode: {mode}. Please use 'script', 'hashtag', or 'both'."))
    
    return state