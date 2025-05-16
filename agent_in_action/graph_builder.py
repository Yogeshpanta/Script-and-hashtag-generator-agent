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
import logging

from IPython.display import Image, display
from langchain_core.runnables.graph import MermaidDrawMethod
import nest_asyncio

setup_logging()


graph = StateGraph(AgentState)

# graph.add_node("structure_gen", structure_generator)
# graph.add_edge(START, "structure_gen")
# graph.add_edge("structure_gen", END)

# graph.add_node("structure_break", structure_generator)
# graph.add_node("trendy_keyword", trending_keyword_generator)

# graph.add_edge(START, "structure_break")
# graph.add_edge("structure_break", "trendy_keyword")
# graph.add_edge("trendy_keyword", END)

# graph.add_node("structure_break", structure_generator)
# graph.add_node("script_generator", script_generator)

# graph.add_edge(START, "structure_break")
# graph.add_edge("structure_break", "script_generator")
# graph.add_edge("script_generator", END)



# graph.add_node("structure_break", structure_generator)
# graph.add_node("trendy_keyword", trending_keyword_generator)
# graph.add_node("hash_tag_gen", hash_tag_generator)

# graph.add_edge(START, "structure_break")
# graph.add_edge("structure_break", "trendy_keyword")
# graph.add_edge("trendy_keyword", "hash_tag_gen")
# graph.add_edge("hash_tag_gen", END)

# graph.add_node("script_generator", script_generator)
# graph.add_node("trend_analyser", trending_keyword_generator)
# graph.add_node("hashtag_generator", hash_tag_generator)
# graph.add_node("structure_break", structure_generator)
# graph.add_node("supervisor_node", supervisor_node)

# graph.add_edge(START, "structure_break")
# graph.add_edge("structure_break", "supervisor_node")
# graph.add_conditional_edges("supervisor_node", node_selector,{"script_generator":"script_generator", "trend_analyser":"trend_analyser",
#                                                               "hashtag_generator":"hashtag_generator", END:END})
# graph.add_edge("trend_analyser","supervisor_node")
# graph.add_edge("script_generator", "supervisor_node")
# graph.add_edge("hashtag_generator", "supervisor_node")




# app = graph.compile()

def graph_builder_agent():
    graph.add_node("script_generator", script_generator)
    graph.add_node("trend_analyser", trending_keyword_generator)
    graph.add_node("hashtag_generator", hash_tag_generator)
    graph.add_node("structure_break", structure_generator)
    graph.add_node("supervisor_node", supervisor_node)

    graph.add_edge(START, "structure_break")
    graph.add_edge("structure_break", "supervisor_node")
    graph.add_conditional_edges("supervisor_node", node_selector,{"script_generator":"script_generator", "trend_analyser":"trend_analyser",
                                                                "hashtag_generator":"hashtag_generator", END:END})
    graph.add_edge("trend_analyser","supervisor_node")
    graph.add_edge("script_generator", "supervisor_node")
    graph.add_edge("hashtag_generator", "supervisor_node")

    app = graph.compile()
    return app




# user_input:AgentState = {
#     "user_input": {
#         "campaign_type": "social media engagement",
#         "product": ["shoes", "sandals", "boots"],
#         "rough_theme": "I want to generate  scripts for above fashion in english language and location should be based on UK"
#     },
#     "structured_data": None,
#     "generated_script": None,
#     "hashtags": None,
#     "messages": [],
#     "current_agent": "user"
# }



# result = app.invoke(user_input, config={"recursion_limit":5})
# print(result["structured_data"])
# print(result["hashtags"])
# print(result["generated_script"])
# nest_asyncio.apply()
# graph_img = Image(app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER))
# graph_img.save("graph.png")

# from PIL import Image
# from io import BytesIO

# nest_asyncio.apply()

# # Get the image bytes from your graph drawing method
# image_bytes = app.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.PYPPETEER)

# # Open the image from bytes
# graph_img = Image.open(BytesIO(image_bytes))

# # Save the image
# graph_img.save("graph.png")


# compaign = "I want to increase user engagement in my social media page"
# product_list = ["shoes", "sandles", "boots"]
# description = """I want to create a 15 second video to increase user engagement for my products in a store. Scripts should be so that , it tells about the store, their producst and reviews. YOu should use
# Nepali language and must target genz. i.e , tone should match with genz customers."""

# user_input:AgentState = (
#     campaign_type="social media engagement",
#     product=["shoes", "sandals", "boots"],  # Must provide list
#     rough_theme="Gen Z targeted video"
# )
