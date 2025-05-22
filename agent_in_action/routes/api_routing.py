from agent_in_action.schemas.overall_state import (
    GenerateResponse,
    UserInput,
    AgentState,
)

from fastapi import APIRouter

from agent_in_action.services.sturct_break import structure_generator
from agent_in_action.services.base_class import supervisor_node
import json

router = APIRouter()


def initialize_state(user_prompt: str) -> AgentState:
    return {
        # Original user input
        "user_input": {"user_prompt": user_prompt},
        # Structured data from user input
        "structured_data": None,
        # steps generation
        "steps_genaration": None,
        # Script generated based on structured data
        "generated_script": None,
        # inputs for hashtag generatiion
        "trendy_keywords": None,
        # Hashtags generated for the campaign
        "hashtags": None,
        # The messages passed between components
        "messages": [],
        # The current agent that is active
        "current_agent": None,
    }


@router.post("/script_hashtag", response_model=GenerateResponse)
def script_hashtag_generator(request: UserInput):
    state = initialize_state(request.user_prompt)

    # structuring the input
    state = structure_generator(state)

    # letting supervisor node to decide
    state = supervisor_node(state)

    # generate response
    script = state.get("generated_script")

    hashtags = state.get("hashtags")

    if hashtags and isinstance(hashtags, str):
        try:
            parsed = json.loads(hashtags)
            hashtags = parsed.get("hashtags", [])  # safely extract list
        except json.JSONDecodeError:
            hashtags = []
    # If hashtags is a string, split to list
    # if hashtags and isinstance(hashtags, str):
    #     hashtags = [tag.strip() for tag in hashtags.split(",") if tag.strip()]

    return GenerateResponse(generated_script=script, hashtags=hashtags)
