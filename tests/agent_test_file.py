import os
from typing import TypedDict, List, Annotated, Literal, Optional, Dict, Any
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
import json

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


# System prompt templates based on the provided code
class SystemPrompts:
    script_generator_prompt = """You are a professional content writer, who can write scenes, voiceover scripts and background scene for any title for creater. For a given prompt by user
        Generate a scene, voiceover script in a following way ### references###
        {
        scene 1: script,
        voiceover 1: voiceover script,
        scene 2: script,
        voiceover 2: voiceover script
        so on ... 
        }
        """
        
    structure_breakdown_prompt = """
        You are an expert in breaking down prompts into structured JSON.
        Given a prompt, extract the following keys (if available). Use `null` if missing.
        Strictly return a valid JSON object — **no markdown**, **no explanation**, just JSON.

        Expected keys:
        "campaign_type", "products", "location", "language", "Tone", "end_customer"

        Example:
        {
        "campaign_type": "social media",
        "products": ["shoes", "sandals", "boots"],
        "location": "UK",
        "language": "Nepali",
        "Tone": "youthful",
        "end_customer": "Gen Z"
        }
        """
    
    has_tag_prompt = """ You are expert in generating #Hash Tags based on data of recent trends. From a user prompt provide a trending top five Hashtags that should be useful in ranking product from SEO point of view
        can be used while making
        videos using '#" symbol:
        **Example
        #keyword 
    """


# Models for different types of data
class UserInput(TypedDict):
    """User input for campaign creation"""
    campaign_type: str
    product: List[str]
    rough_theme: str


class UserPromptBreakdown(TypedDict):
    """Breakdown of user prompt into structured data"""
    campaign_type: Optional[str]
    products: Optional[List[str]]
    location: Optional[str]
    language: Optional[str]
    Tone: Optional[str]
    end_customer: Optional[str]


class HashInput(TypedDict):
    """Input for hashtag generation"""
    input_list: str


class AgentState(TypedDict):
    """Main state for the entire workflow"""
    # Original user input
    user_input: Optional[UserInput]
    # Structured data from user input
    structured_data: Optional[Dict[str, Any]]
    # Script generated based on structured data
    generated_script: Optional[str]
    # Hashtags generated for the campaign
    hashtags: Optional[List[str]]
    # The messages passed between components
    messages: List[Annotated[HumanMessage | AIMessage, "messages"]]
    # The current agent that is active
    current_agent: Literal["supervisor", "agent_1", "agent_2", "agent_3", "user", END]


# Define the agents and their functionalities
def user(state: AgentState) -> AgentState:
    """User node that provides the initial campaign creation request"""
    # In a real implementation, this would take input from a real user
    # For this example, we're simulating user interaction
    if len(state["messages"]) == 0:
        print("User: I want to create a social media campaign for our new running shoes.")
        state["user_input"] = {
            "campaign_type": "social media",
            "product": ["running shoes", "athletic wear"],
            "rough_theme": "Targeting young athletes aged 18-25 in the UK, using an energetic tone."
        }
        state["messages"].append(HumanMessage(content="I want to create a social media campaign for our new running shoes. "
                                               "Targeting young athletes aged 18-25 in the UK, using an energetic tone."))
    state["current_agent"] = "supervisor"
    return state


def supervisor(state: AgentState) -> AgentState:
    """Supervisor node that routes to different agents based on the task"""
    latest_message = state["messages"][-1].content
    print(f"Supervisor received: {latest_message}")
    
    # Check what stage we're at in the workflow
    if state.get("structured_data") is None:
        # Need to structure the data first
        print("Supervisor: Routing to Agent 1 for structure analysis.")
        state["messages"].append(AIMessage(content="Routing request to structure analyzer."))
        state["current_agent"] = "agent_1"
    elif state.get("generated_script") is None:
        # Next, generate the script
        print("Supervisor: Routing to Agent 2 for script generation.")
        state["messages"].append(AIMessage(content="Routing to script generator."))
        state["current_agent"] = "agent_2"
    elif state.get("hashtags") is None:
        # Finally, generate hashtags
        print("Supervisor: Routing to Agent 3 for hashtag generation.")
        state["messages"].append(AIMessage(content="Routing to hashtag generator."))
        state["current_agent"] = "agent_3"
    else:
        # All done, send back to user
        print("Supervisor: All tasks completed, sending results to user.")
        final_message = f"Campaign creation complete!\n\nScript: {state['generated_script'][:100]}...\n\nHashtags: {', '.join(state['hashtags'])}"
        state["messages"].append(AIMessage(content=final_message))
        state["current_agent"] = "user"
    
    return state


def agent_1(state: AgentState) -> AgentState:
    """Agent specialized in structure analysis - breaks down user input into structured data"""
    print("Agent 1: Analyzing and structuring user input.")
    
    user_input = state["user_input"]
    prompt = f"""I want to create a video for {user_input['campaign_type']}, which should be suitable for the products {', '.join(user_input['product'])}
You can use the following description to generate a script: {user_input['rough_theme']}
"""
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7, api_key=openai_api_key)
    response = llm.invoke([
        {"role": "system", "content": SystemPrompts.structure_breakdown_prompt},
        {"role": "user", "content": prompt}
    ])
    
    structured_data = json.loads(response.content)
    state["structured_data"] = structured_data
    state["messages"].append(AIMessage(content=f"Structured data created: {response.content}"))
    state["current_agent"] = "supervisor"  # Send back to supervisor
    return state


def agent_2(state: AgentState) -> AgentState:
    """Agent specialized in script generation - creates scripts based on structured data"""
    print("Agent 2: Generating campaign script.")
    
    structured_data = state["structured_data"]
    prompt = f"""I want to create a video for {structured_data.get('campaign_type', 'marketing')}, which should be suitable for the products {', '.join(structured_data.get('products', ['product']))}
Generate script in language: {structured_data.get('language', 'English')}, should be suitable for location {structured_data.get('location', 'global')}, 
tone: {structured_data.get('Tone', 'professional')} and must target end customer: {structured_data.get('end_customer', 'general audience')}
Generate a compelling and engaging video script that aligns with these specifications.
"""
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8, api_key=openai_api_key)
    response = llm.invoke([
        {"role": "system", "content": SystemPrompts.script_generator_prompt},
        {"role": "user", "content": prompt}
    ])
    
    state["generated_script"] = response.content
    state["messages"].append(AIMessage(content=f"Script generated successfully. First 100 chars: {response.content[:100]}..."))
    state["current_agent"] = "supervisor"  # Send back to supervisor
    return state


def agent_3(state: AgentState) -> AgentState:
    """Agent specialized in hashtag generation - creates trending hashtags for the campaign"""
    print("Agent 3: Generating hashtags for the campaign.")
    
    structured_data = state["structured_data"]
    products = ', '.join(structured_data.get('products', ['product']))
    campaign_type = structured_data.get('campaign_type', 'marketing')
    
    prompt = f"Provide the top hashtags for {campaign_type} campaign about {products}"
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.8, api_key=openai_api_key)
    response = llm.invoke([
        {"role": "system", "content": SystemPrompts.has_tag_prompt},
        {"role": "user", "content": prompt}
    ])
    
    # Extract hashtags from response
    hashtags = [tag.strip() for tag in response.content.split() if tag.startswith('#')]
    if not hashtags:
        # Fallback if no hashtags with # were found
        hashtags = ["#" + word for word in response.content.split()[:5]]
    
    state["hashtags"] = hashtags
    state["messages"].append(AIMessage(content=f"Hashtags generated: {', '.join(hashtags)}"))
    state["current_agent"] = "supervisor"  # Send back to supervisor
    return state


def route_based_on_agent(state: AgentState) -> Literal["supervisor", "agent_1", "agent_2", "agent_3", "user", END]:
    """Router function to determine the next node."""
    return state["current_agent"]


# Create the graph
workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("user", user)
workflow.add_node("supervisor", supervisor)
workflow.add_node("agent_1", agent_1)
workflow.add_node("agent_2", agent_2)
workflow.add_node("agent_3", agent_3)

# Add edges based on the current_agent field
workflow.add_conditional_edges(
    "user",
    route_based_on_agent,
    {
        "supervisor": "supervisor",
        "agent_1": "agent_1",
        "agent_2": "agent_2",
        "agent_3": "agent_3",
        END: END
    }
)

workflow.add_conditional_edges(
    "supervisor",
    route_based_on_agent,
    {
        "user": "user",
        "agent_1": "agent_1",
        "agent_2": "agent_2",
        "agent_3": "agent_3",
        END: END
    }
)

# Agents return to supervisor after completing their tasks
for agent in ["agent_1", "agent_2", "agent_3"]:
    workflow.add_conditional_edges(
        agent,
        route_based_on_agent,
        {
            "supervisor": "supervisor",
            "user": "user",
            END: END
        }
    )

# Compile the graph
app = workflow.compile()

# Run the graph with an example starting point
def run_example():
    # Initialize the state
    state = {
        "user_input": None,
        "structured_data": None,
        "generated_script": None,
        "hashtags": None,
        "messages": [],
        "current_agent": "user"
    }
    
    # Run the workflow from start to finish
    result = app.invoke(state)
    print("\n--- Workflow execution complete ---\n")
    
    # Display final results
    if result.get("generated_script") and result.get("hashtags"):
        print("\n=== Final Campaign Results ===")
        print(f"\nGenerated Script (first 200 chars):\n{result['generated_script'][:200]}...\n")
        print(f"Hashtags: {', '.join(result['hashtags'])}\n")


if __name__ == "__main__":
    run_example()