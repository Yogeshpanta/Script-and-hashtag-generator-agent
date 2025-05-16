# from typing import TypedDict
from typing_extensions import TypedDict
from typing import Optional, Dict, Any, List, Annotated, Literal
from langchain.schema import HumanMessage, AIMessage
# from agent_in_action.schemas.structure_gen import UserInput, UserPromptBreakdown
from langgraph.graph import END


class UserInput(TypedDict):
    """class where a user input are given"""
    campaign_type:str
    product:list[str]
    rough_theme:str

class AgentState(TypedDict):
    """Main state for the entire workflow"""
    # Original user input
    user_input: Optional[UserInput]
    # Structured data from user input
    structured_data: Optional[Dict[str, Any]]
    # Script generated based on structured data
    generated_script: Optional[str]
    # inputs for hashtag generatiion
    trendy_keywords:Optional[str]
    # Hashtags generated for the campaign
    hashtags: Optional[List[str]]
    # The messages passed between components
    messages: List[Annotated[HumanMessage | AIMessage, "messages"]]
    # The current agent that is active
    current_agent: Literal["supervisor_node", "script_generator", "trending_keywords_generator", "hash_tag_generator", END]