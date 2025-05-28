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
import json
import logging

import os
from dotenv import load_dotenv

setup_logging()
logger = logging.getLogger(__name__)

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def supervisor_node(state: AgentState):
    """
    Orchestrates execution of tool functions based on user input and LLM-decided execution plan.

    Args:
        state (AgentState): Workflow state containing input, structured data, etc.

    Returns:
        AgentState: Updated workflow state after executing required tools.
    """

    try:
        # Step 1: Ask LLM which nodes should be executed
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_api_key)
        planning_response = llm.invoke(
            [
                SystemMessage(content=SystemPrompts.node_executer_agent),
                HumanMessage(content=state["user_input"]["user_prompt"]),
            ]
        )

        # Step 2: Parse the LLM response and extract the execution plan
        plan = json.loads(planning_response.content)
        # mode = plan.get("mode") or plan.get("objective")  # alias support
        mode = plan.get("objective")
        logger.info(f"Supervisor mode: {mode}")

        # Save mode to structured data for traceability
        # state["structured_data"] = {
        #     "mode": mode
        # }

        # Step 3: Execute specific tools based on the mode
        if mode == "script":
            logger.info("Executing script generator node...")
            state = script_generator(state)

        elif mode == "hashtag":
            logger.info("Executing trending keyword and hashtag generator nodes...")
            state = trending_keyword_generator(state)

            if "trendy_keywords" in state and state["trendy_keywords"]:
                state = hash_tag_generator(state)
            else:
                return "Trending keywords missing. Cannot generate hashtags."

        elif mode == "script_and_hashtag":
            logger.info("Executing full pipeline: script ➝ keywords ➝ hashtags...")
            state = script_generator(state)
            state = trending_keyword_generator(state)

            if "trendy_keywords" in state and state["trendy_keywords"]:
                state = hash_tag_generator(state)
            else:
                return "Trending keywords missing. Cannot generate hashtags."

        else:
            return f"Unsupported mode: {mode}. Use 'script', 'hashtag', or 'script_and_hashtag'."

        return state

    except json.JSONDecodeError:
        raise ValueError(
            "LLM response is not a valid JSON. Check the system prompt formatting."
        )
    except KeyError as ke:
        raise KeyError(f"Missing expected field in plan: {ke}")
    except Exception as e:
        raise Exception(f"Supervisor execution failed: {e}")
