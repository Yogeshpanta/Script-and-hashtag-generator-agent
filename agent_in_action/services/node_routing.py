from agent_in_action.schemas.overall_state import AgentState
from langgraph.graph import END


# def node_selector(state:AgentState):
#     """Selects node based on the condition"""
#     mode = state['structured_data']
#     mode_definer = mode.get("mode")
#     if mode_definer == "script":
#         return "script_generator"

#     if mode_definer == "hashtag":
#         return "hashtag_generator"

#     else:
#         return END

# def node_selector(state: AgentState):
#     """Enhanced node selector with progress tracking"""
#     structured_data = state.get("structured_data", {})
#     mode = structured_data.get("mode")

#     # Flow control flags
#     trend_done = "trendy_keywords" in state
#     hashtags_done = "hashtags" in state

#     if mode == "script":
#         return "script_generator"

#     if mode == "hashtag":
#         if not trend_done:  # First cycle: LLM -> trend_analyser
#             return "trend_analyser"
#         elif not hashtags_done:  # Second cycle: LLM -> hashtag_generator
#             return "hashtag_generator"

#     # Final cycle: return to LLM for completion
#     return END


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
