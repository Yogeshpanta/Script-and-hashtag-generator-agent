# from agent_in_action.schemas.structure_gen import UserInput, UserPromptBreakdown
from agent_in_action.prompts.prompt_templates import SystemPrompts
from agent_in_action.schemas.overall_state import AgentState
from agent_in_action.configs.logging_config import setup_logging

from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
import logging
import os
from dotenv import load_dotenv

setup_logging()
logger = logging.getLogger(__name__)

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def script_generator(state: AgentState) -> AgentState:
    """
    Generates a compelling and tailored video script based on the structured input
    provided in the agent state, and updates the state with the generated script.

    This function extracts campaign-related details such as campaign type, products,
    language, location, tone, and target customer demographic from the `structured_data`
    in the agent state. It constructs a prompt for a language model (ChatOpenAI) to
    generate a relevant and engaging script tailored to the provided specifications.

    The generated script is stored in the `generated_script` field of the `AgentState`,
    and the script content is also logged into the `messages` list for workflow tracking.

    Args:
        state (AgentState): The current agent state containing structured campaign data
                            and conversation history.

    Returns:
        AgentState: The updated state containing the generated script and a message
                    reflecting the output.

    Raises:
        KeyError: If `structured_data` is missing from the state.
        Exception: If the language model call fails or produces invalid content.
    """
    print("Generating the scripts for the given title")
    script_detail = state["structured_data"]

    campaign_type = script_detail.get("campaign_title")
    product = script_detail.get("products", " ")
    # product = ",".join([i for i in products])
    Language = script_detail.get("language", "english")
    Location = script_detail.get("location", "united states")
    Tone = script_detail.get("Tone", "general")
    end_customer = script_detail.get("end_customer", "15 to 50 age groups")
    # mode = script_detail.get("mode", "script")

    prompt = f"""I want to create a video for {campaign_type}, which should be suitable for the produts {product}
You can use the following description to generate a script:
Generate script in language: {Language}, should be suitable for location {Location}, tone: {Tone} and must target end customer: {end_customer}
Generate a compelling and engaging video script that aligns with these specifications.

"""

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.9, api_key=openai_api_key)
    response = llm(
        [
            SystemMessage(content=SystemPrompts.script_generator_prompt),
            HumanMessage(content=prompt),
        ]
    )
    logger.info("generating a scripts.....")

    state["generated_script"] = response.content
    state["messages"].append(
        AIMessage(content=f"script generated for video:{response.content}")
    )
    return state
