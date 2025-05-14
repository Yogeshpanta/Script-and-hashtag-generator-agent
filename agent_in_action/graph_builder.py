from langgraph.graph import StateGraph, START, END

from agent_in_action.schemas.structure_gen import UserInput, StructureBreaker, UserPromptBreakdown
from agent_in_action.services.sturct_break import structure_generator, parse_script_output
from agent_in_action.services.script_gen import script_generator
from agent_in_action.schemas.script_schema import GenerateScript
from agent_in_action.configs.logging_config import setup_logging
from agent_in_action.services.hash_tag_gen import hash_tag_generator
from agent_in_action.services.trend_analysis import TrendAnalysis
import logging

setup_logging()


# graph = StateGraph(input=UserInput, output=StructureBreaker)

# graph.add_node("structure_gen", structure_generator)
# graph.add_edge(START, "structure_gen")
# graph.add_edge("structure_gen", END)


# graph = StateGraph(input=UserInput, output=UserPromptBreakdown)
# graph.add_node("structure_generator", structure_generator)
# graph.add_node("user_prompt", parse_script_output)
# graph.add_edge(START , "structure_generator")
# graph.add_edge("structure_generator", "user_prompt")
# graph.add_edge("user_prompt", END)

# graph = StateGraph(input=UserInput, output=GenerateScript)
# graph.add_node("structure_generator", structure_generator)
# graph.add_node("prompt_breakdown", parse_script_output)
# graph.add_node("script_gen", script_generator)


# graph.add_edge(START , "structure_generator")
# graph.add_edge("structure_generator", "prompt_breakdown")
# graph.add_edge("prompt_breakdown", "script_gen")
# graph.add_edge("script_gen", END)

# app = graph.compile()

graph = StateGraph(input=UserInput, output=GenerateScript)
graph.add_node("structure_generator", structure_generator)
graph.add_node("prompt_breakdown", parse_script_output)
graph.add_node("script_gen", script_generator)
graph.add_node("hash_generator", hash_tag_generator)

graph.add_edge(START , "structure_generator")
graph.add_edge("structure_generator", "prompt_breakdown")
graph.add_edge("prompt_breakdown", "script_gen")
graph.add_edge("script_gen", END)

app = graph.compile()



# compaign = "I want to increase user engagement in my social media page"
# product_list = ["shoes", "sandles", "boots"]
# description = """I want to create a 15 second video to increase user engagement for my products in a store. Scripts should be so that , it tells about the store, their producst and reviews. YOu should use
# Nepali language and must target genz. i.e , tone should match with genz customers."""

input_data = UserInput(
    campaign_type="social media engagement",
    product=["shoes", "sandals", "boots"],  # Must provide list
    rough_theme="Gen Z targeted video"
)

# result = app.invoke(UserInput(campaign_type=compaign, product=product_list, rough_theme=description))
result = app.invoke(input_data.model_dump())
# print(str(result))
# print(type(result["structured_data"]))
# print(result["structured_data"])
print(result["script"])
