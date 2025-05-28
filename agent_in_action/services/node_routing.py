from agent_in_action.schemas.overall_state import AgentState
from langgraph.graph import END


def node_selector(state: AgentState):
    """Enhanced node selector with progress tracking"""
    structured_data = state.get("structured_data", {})
    mode = structured_data.get("mode")

    script_done = "generated_script" in state and state["generated_script"]
    trend_done = "trendy_keywords" in state
    hashtags_done = "hashtags" in state

    if mode == "script":
        if not script_done:
            return "script_generator"
        else:
            return END

    if mode == "hashtag":
        if not trend_done:
            return "trend_analyser"
        if trend_done and not hashtags_done:
            return "hashtag_generator"
        if trend_done and hashtags_done:
            return END

    return END
