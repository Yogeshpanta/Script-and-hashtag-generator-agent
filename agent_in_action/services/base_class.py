from agent_in_action.schemas.overall_state import AgentState
from agent_in_action.prompts.prompt_templates import SystemPrompts
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from agent_in_action.configs.logging_config import setup_logging

from agent_in_action.services.hash_tag_gen import hash_tag_generator
from agent_in_action.services.script_gen import script_generator
from agent_in_action.services.trend_analysis import trending_keyword_generator
from agent_in_action.services.sturct_break import structure_generator
from langgraph.graph import END
import logging

import os
from dotenv import load_dotenv

setup_logging()

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

# def supervisor_node(state: AgentState):
#     """
#     Acts as the central controller that orchestrates the execution of other tool functions
#     (script generation, trending keyword extraction, and hashtag generation) based on the
#     structured data provided in the agent state.
    
#     This function reads key details such as mode, campaign type, and products from the
#     `structured_data` field of the agent state and directly calls the appropriate tools
#     based on the requested mode.
    
#     Args:
#         state (AgentState): The current state of the workflow, including user input,
#         structured data, and message history.
        
#     Returns:
#         AgentState: The updated agent state after executing the requested tools.
        
#     Raises:
#         KeyError: If `structured_data` or its required fields are missing from the state.
#         Exception: If tool invocation fails.
#     """
#     details = state["structured_data"]
#     mode = details.get("mode")  # Default to script if not specified
    
#     # Log the start of supervisor execution
#     state["messages"].append(AIMessage(content=f"Supervisor node executing in {mode} mode"))
    
#     # Execute based on mode
#     if mode == "script" or mode == "scripts":
#         # Generate script
#         state = script_generator(state)
#     elif mode == "hashtag" or mode == "hashtags":
#         # For hashtags, we need to first get trending keywords, then generate hashtags
#         state = trending_keyword_generator(state)
#         if "trendy_keywords" in state and state["trendy_keywords"]:
#             state = hash_tag_generator(state)
#     elif mode == "both" or mode == "all":
#         # Generate both script and hashtags
#         state = script_generator(state)
#         state = trending_keyword_generator(state)
#         if "trendy_keywords" in state and state["trendy_keywords"]:
#             state = hash_tag_generator(state)
#     else:
#         # Log unsupported mode
#         state["messages"].append(AIMessage(content=f"Unsupported mode: {mode}. Please use 'script', 'hashtag', or 'both'."))
    
#     return state

def supervisor_node(state: AgentState):
    """
    Orchestrates the execution of tool functions (script generation, keyword extraction,
    and hashtag generation) based on structured data in the agent state.

    Args:
        state (AgentState): Current workflow state including input, structured data, and history.

    Returns:
        AgentState: Updated state after executing necessary tools.

    Raises:
        ValueError: If steps are missing or all are already marked True.
    """
    
    try:
        details = state["structured_data"]
        mode = details.get("mode")  # Default to 'script' if not specified
        steps = details.get("steps", [])

        # Log the start of supervisor execution
        state["messages"].append(AIMessage(content=f"Supervisor node executing in {mode} mode"))

        if not steps or all(steps):
            raise ValueError("You must specify the steps and set at least one as False.")

        if mode == "script" and len(steps) == 1:
            if not steps[0]:
                state = script_generator(state)
                state["structured_data"]["steps"][0] = True
            else:
                return "All steps are already completed. Cannot generate script again."

        elif mode == "hashtag" and len(steps) == 2:
            if not steps[0]:
                state = trending_keyword_generator(state)
                state["structured_data"]["steps"][0] = True

            if not steps[1] and "trendy_keywords" in state and state["trendy_keywords"]:
                state = hash_tag_generator(state)
                state["structured_data"]["steps"][1] = True
            elif not steps[1]:
                return "Cannot generate hashtags because 'trendy_keywords' are missing."

        elif mode == "both" and len(steps) == 3:
            if not steps[0]:
                state = script_generator(state)
                state["structured_data"]["steps"][0] = True

            if not steps[1]:
                state = trending_keyword_generator(state)
                state["structured_data"]["steps"][1] = True

            if not steps[2] and "trendy_keywords" in state and state["trendy_keywords"]:
                state = hash_tag_generator(state)
                state["structured_data"]["steps"][2] = True
            elif not steps[2]:
                return "Cannot generate hashtags because 'trendy_keywords' are missing."

        else:
            return f"Unsupported mode: {mode}. Please use 'script', 'hashtag', or 'both'."

        return state

    except KeyError as ke:
        raise KeyError(f"Missing required key in structured_data: {ke}")
    except Exception as e:
        raise Exception(f"Supervisor execution failed: {e}")

# def supervisor_node(state: AgentState) -> AgentState:
#     """
#     Intelligent supervisor that decides which tool to call next based on the current state.
#     Uses LLM to make decisions rather than hardcoded rules.
#     """
#     # Check if we have structured data
#     if "structured_data" not in state or not state["structured_data"]:
#         state = structure_generator(state)
    
#     # Get current progress
#     details = state["structured_data"]
#     mode = details.get("mode", "script")  # Default to 'script' if not specified
    
#     # Track what's already been done
#     script_done = "generated_script" in state and state["generated_script"]
#     trend_done = "trendy_keywords" in state and state["trendy_keywords"]
#     hashtags_done = "hashtags" in state and state["hashtags"]
    
#     # Get OpenAI API key from environment variable
#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     if not openai_api_key:
#         raise ValueError("OPENAI_API_KEY environment variable not set")
    
#     # Use LLM to decide next action if there's still work to do
#     if (mode == "script" and not script_done) or \
#        (mode == "hashtag" and (not trend_done or not hashtags_done)) or \
#        (mode == "both" and (not script_done or not trend_done or not hashtags_done)):
        
#         # Create status summary for LLM
#         status = {
#             "mode": mode,
#             "script_generated": script_done,
#             "trending_keywords_generated": trend_done,
#             "hashtags_generated": hashtags_done
#         }
        
#         status_prompt = f"""Current workflow status:
# Mode: {mode}
# Script generated: {script_done}
# Trending keywords generated: {trend_done}
# Hashtags generated: {hashtags_done}

# Based on this status, what is the next action that should be taken? Choose one of:
# 1. "script_generator" - Generate a script (can be done independently)
# 2. "trending_keywords_generator" - Get trending keywords (required before hashtag generation)
# 3. "hash_tag_generator" - Generate hashtags (requires trending keywords to be done first)
# 4. "END" - All required tasks are complete

# Respond with ONLY ONE of these exact options. Do not add any explanation.
# """
        
#         llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.1, api_key=openai_api_key)
#         response = llm.invoke([
#             {"role": "system", "content": SystemPrompts.supervisor_prompt},
#             {"role": "user", "content": status_prompt}
#         ])
        
#         next_action = response.content.strip().lower()
#         state["messages"].append(AIMessage(content=f"Supervisor decided next action: {next_action}"))
        
#         # Execute the chosen action
#         if "script_generator" in next_action and not script_done:
#             state = script_generator(state)
#         elif "trending_keywords_generator" in next_action and not trend_done:
#             state = trending_keyword_generator(state)
#         elif "hash_tag_generator" in next_action and trend_done and not hashtags_done:
#             state = hash_tag_generator(state)
#         elif "end" in next_action or next_action == "end":
#             state["messages"].append(AIMessage(content="All requested tasks completed successfully."))
#             state["current_agent"] = END
#             return state
#         else:
#             state["messages"].append(AIMessage(content=f"Unrecognized or invalid next action: '{next_action}'. Ending workflow."))
#             state["current_agent"] = END
#             return state
        
#         # Recursively call supervisor to continue the workflow
#         return supervisor_node(state)
#     else:
#         # All tasks for the current mode are complete
#         state["messages"].append(AIMessage(content=f"All tasks for mode '{mode}' completed successfully."))
#         state["current_agent"] = END
#         return state
