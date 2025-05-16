import logging
from agent_in_action.configs.logging_config import setup_logging

from agent_in_action.graph_builder import graph_builder_agent
from agent_in_action.schemas.overall_state import AgentState


setup_logging()
logger = logging.getLogger(__name__)

# # Example usage of logging
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")


if __name__ == "__main__":
    user_input:AgentState = {
    "user_input": {
        "campaign_type": "social media engagement",
        "product": ["shoes", "sandals", "boots"],
        "rough_theme": "I want to generate top five tags for above fashion in english language and location should be based on UK"
    },
    "structured_data": None,
    "generated_script": None,
    "hashtags": None,
    "messages": [],
    "current_agent": "user"
    }

    app = graph_builder_agent()
    result = app.invoke(user_input, config={"recursion_limit":5})
    print(result["structured_data"])
    print(result["hashtags"])
    print(result["generated_script"])
