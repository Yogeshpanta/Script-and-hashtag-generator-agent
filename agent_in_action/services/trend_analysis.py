import serpapi

import os
from dotenv import load_dotenv
load_dotenv()

class TrendAnalysis:
    def __init__(self, keywords:str, host_lang:str, geo_location:str):
        self.keywords = keywords
        self.host_lang = host_lang
        self.geo_location = geo_location
        self.api_key = os.getenv("SERPAPI_KEY")

    def __str__(self):
        return "Analysing the trends"
    
    def trending_keyword_generator(self):
        """Generates the top trending keywords based on products and title"""
        client = serpapi.Client(api_key=self.api_key)
        search = client.search(
            engine="google",
            q= self.keywords,
            hl= self.host_lang,
            gl=self.geo_location
        )

        organic_results = search.get("organic_results", [])
        # snippets = []
        # for results in organic_results:
        #     snippet = results.get("snippet")
        #     snippets.append(snippet)
        snippets = [item.get("snippet") for item in organic_results if item.get("snippet")]

        return " ,".join([i for i in snippets])


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
