from agent_in_action.prompts.prompt_templates import SystemPrompts
# from agent_in_action.schemas.hash_tag_schema import HashInput, HashTagOutput
from agent_in_action.schemas.overall_state import AgentState
import logging
# from langchain_core.tools import tool

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage, AIMessage

import os
from dotenv import load_dotenv
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def hash_tag_generator(state:AgentState) -> AgentState:
    """
    Generates a list of relevant hashtags based on the provided trendy keywords 
    in the agent state and updates the agent state with the generated hashtags.

    This function uses a language model (ChatOpenAI) to analyze the `trendy_keywords` 
    provided in the state and returns the top five most suitable and trendy hashtags 
    for a marketing campaign or content topic. The generated hashtags are then stored 
    in the `hashtags` field of the `AgentState`.

    Additionally, the function logs the interaction by appending an AIMessage 
    to the `messages` list within the state for traceability and transparency 
    of communication.

    Args:
        state (AgentState): The current agent state, containing `trendy_keywords` 
                            to generate hashtags from and other workflow-related data.

    Returns:
        AgentState: The updated agent state with newly generated hashtags and 
                    an appended message summarizing the output.

    Raises:
        KeyError: If 'trendy_keywords' is not present in the state.
        Exception: If the language model call fails or returns an unexpected result.
    """

    trendy_keywords = state["trendy_keywords"]
    prompt = f"""Provide the top five hashtags for these topics {trendy_keywords}"""
    logging.info("generating hashtags from trending keyword")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.8, api_key=openai_api_key)
    response = llm(
        [SystemMessage(content=SystemPrompts.has_tag_prompt),
        HumanMessage(content=prompt)]
    )
    state["hashtags"] = response.content
    logging.info("hashtags generated")
    state["messages"].append(AIMessage(content=f"Generated hashtags for given video:{response.content}"))
    return state