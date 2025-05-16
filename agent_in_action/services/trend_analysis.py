import serpapi
from agent_in_action.schemas.overall_state import AgentState
from langchain.schema import AIMessage
# from langchain_core.tools import tool

import os
from dotenv import load_dotenv
load_dotenv()

# class TrendAnalysis:
#     def __init__(self, keywords:str, host_lang:str, geo_location:str):
#         self.keywords = keywords
#         self.host_lang = host_lang
#         self.geo_location = geo_location
#         self.api_key = os.getenv("SERPAPI_KEY")

#     def __str__(self):
#         return "Analysing the trends"
    
#     def trending_keyword_generator(self):
#         """Generates the top trending keywords based on products and title"""
#         client = serpapi.Client(api_key=self.api_key)
#         search = client.search(
#             engine="google",
#             q= self.keywords,
#             hl= self.host_lang,
#             gl=self.geo_location
#         )

#         organic_results = search.get("organic_results", [])
#         # snippets = []
#         # for results in organic_results:
#         #     snippet = results.get("snippet")
#         #     snippets.append(snippet)
#         snippets = [item.get("snippet") for item in organic_results if item.get("snippet")]

#         return " ,".join([i for i in snippets])
    


def trending_keyword_generator(state:AgentState)->AgentState:
    """
    Extracts and generates trending keywords related to the product(s) provided 
    in the structured data, and updates the agent state with those keywords.

    This function uses the SerpAPI to perform a Google search based on the product 
    names, language, and location specified in the `structured_data` of the agent state. 
    It collects the snippets from the top organic search results, which are assumed to 
    contain popular and contextually relevant phrases or keywords.

    These extracted keywords are combined into a single comma-separated string and stored 
    in the `trendy_keywords` field of the `AgentState`. The function also appends an 
    AIMessage to the state’s `messages` to log the generated keywords.

    Args:
        state (AgentState): The current state of the agent, including structured user input 
                            with products, language, and location.

    Returns:
        AgentState: The updated state with extracted trending keywords and an appended message 
                    containing those keywords.

    Raises:
        KeyError: If required fields like 'structured_data' or 'products' are missing in the state.
        Exception: If the SerpAPI search fails or returns no usable results.
    """
    required_keyword = state["structured_data"]
    products = required_keyword.get("products", "marketing")
    product = " ".join([i for i in products])
    client = serpapi.Client(api_key=os.getenv("SERPAPI_KEY"))
    search = client.search(
                engine = "google",
                q = product,
                # hl = required_keyword.get("language", "en"),
                # gl = required_keyword.get("location","us"),
                hl = "en",
                gl = "us"
        )

    organic_results = search.get("organic_results", [])
    snippets = [item.get("snippet") for item in organic_results if item.get("snippet")]
    state["trendy_keywords"] = " ,".join([i for i in snippets])
    state["messages"].append(AIMessage(content= f"trendy keyword generated: {state['trendy_keywords']}"))
    return state



# class TrendAnalysis:
#     def __init__(self, keywords: str, host_lang: str, geo_location: str, api_key: str):
#         self.keywords = keywords
#         self.host_lang = host_lang
#         self.geo_location = geo_location
#         self.api_key = os.getenv("SERPAPI_KEY")

#     def __str__(self):
#         return "Analyzing the trends"

#     def trending_keyword_generator(self) -> str:
#         """Fetches top trending snippets based on the search keyword"""
#         params = {
#             "engine": "google",
#             "q": self.keywords,
#             "hl": self.host_lang,
#             "gl": self.geo_location,
#             "api_key": self.api_key
#         }

#         try:
#             search = GoogleSearch(params)
#             results = search.get_dict()
#             organic_results = results.get("organic_results", [])
#             snippets = [item.get("snippet") for item in organic_results if item.get("snippet")]

#             return ", ".join(snippets) if snippets else "No trending snippets found."
#         except Exception as e:
#             return f"An error occurred while fetching trends: {e}"
