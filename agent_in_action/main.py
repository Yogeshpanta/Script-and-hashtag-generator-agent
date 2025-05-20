import logging
from agent_in_action.configs.logging_config import setup_logging

from agent_in_action.graph_builder import graph_builder_agent
from agent_in_action.schemas.overall_state import AgentState
from fastapi import FastAPI
from agent_in_action.routes import api_routing
import uvicorn

setup_logging()
logger = logging.getLogger(__name__)

# # Example usage of logging
# logger.info("This is an info message.")
# logger.warning("This is a warning message.")
# logger.error("This is an error message.")


# if __name__ == "__main__":
#     user_input:AgentState = {
#     "user_input": {
#         "user_prompt": "I want to generate a scripts and hashtags for about 15 sec video, about the title: 'transformer in deep learning'"
#     },
#     "structured_data": None,
#     "generated_script": None,
#     "hashtags": None,
#     "messages": [],
#     "current_agent": "user"

#     }

#     app = graph_builder_agent()
#     result = app.invoke(user_input, config={"recursion_limit":5})
#     print(result["structured_data"])
#     print(result["hashtags"])
#     print(result["generated_script"])

app = FastAPI(
    title= "Agent for script and hashtag generation",
    description= "API For generating hastag and scripts based on prompts"
)

app.include_router(api_routing.router, prefix="/api")

if __name__ == "__main__":
    logging.info("running a FastAPI APP")
    uvicorn.run(app, host="127.0.0.1", port=8000)
