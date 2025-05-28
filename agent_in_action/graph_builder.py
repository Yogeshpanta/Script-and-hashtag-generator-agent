from langgraph.graph import StateGraph, START, END

# from agent_in_action.schemas.structure_gen import UserInput, StructureBreaker, UserPromptBreakdown
from agent_in_action.services.sturct_break import structure_generator
from agent_in_action.services.script_gen import script_generator

# from agent_in_action.schemas.script_schema import GenerateScript
from agent_in_action.configs.logging_config import setup_logging
from agent_in_action.services.hash_tag_gen import hash_tag_generator

# from agent_in_action.services.trend_analysis import TrendAnalysis
from agent_in_action.schemas.overall_state import AgentState
from agent_in_action.services.trend_analysis import trending_keyword_generator
from agent_in_action.services.base_class import supervisor_node
from agent_in_action.services.node_routing import node_selector


setup_logging()


graph = StateGraph(AgentState)


def graph_builder_agent():
    graph.add_node("script_generator", script_generator)
    graph.add_node("trend_analyser", trending_keyword_generator)
    graph.add_node("hashtag_generator", hash_tag_generator)
    graph.add_node("structure_break", structure_generator)
    graph.add_node("supervisor_node", supervisor_node)

    graph.add_edge(START, "structure_break")
    graph.add_edge("structure_break", "supervisor_node")
    graph.add_conditional_edges(
        "supervisor_node",
        node_selector,
        {
            "script_generator": "script_generator",
            "trend_analyser": "trend_analyser",
            "hashtag_generator": "hashtag_generator",
            END: END,
        },
    )
    graph.add_edge("trend_analyser", "supervisor_node")
    graph.add_edge("script_generator", "supervisor_node")
    graph.add_edge("hashtag_generator", "supervisor_node")

    app = graph.compile()
    return app
