# Script & Hashtag Generator Agent
An AI-powered content creation system that generates video scripts and trending hashtags based on user prompts. Built with FastAPI and LangGraph for intelligent workflow orchestration.

## Features

- **AI Script Generation**: Create engaging video scripts for any topic
- **Smart Prompt Analysis**: Automatically extract structured data from natural language
- **Trending Hashtags**: Generate relevant hashtags using real-world search data
- **REST API**: Easy integration via FastAPI endpoints
- **Workflow Orchestration**: Intelligent agent routing with LangGraph

## Installation

1. Clone Repo:
`git clone git@github.com:Yogeshpanta/Script-and-hashtag-generator-agent.git`
`cd Script-and-hashtag-generator-agent`

2. Create virtual environment:
- ** install uv 
pip install uv
- ** create environment
uv venv
- ** Activate environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate # Windows

3. Install dependencies:
uv sync

 ## COnfiguration
 Create `.env` file:  
 OPENAI_API_KEY = your_openai_key_here  
 SERPAPI_KEY = your_serpapi_key_here  

 4. Run 
 uv run agent_in_action/main.py

 ### API Request
 curl -X POST "http://localhost:8000/api/script_hashtag"  
-H "Content-Type: application/json"  
-d '{"user_prompt": "Create a script and hashtags for 15-second Instagram reel about AI in healthcare"}'  

## Project Structure

├── agent_in_action/  
│ ├── configs/ # Logging configuration  
│ ├── routes/ # API endpoints  
│ ├── schemas/ # Pydantic models  
│ ├── services/ # Core business logic  
│ └── main.py # FastAPI app entry  
├── tests/ # Test cases  
├── pyproject.toml # Dependencies  
├──  uv.lock   
└── README.md  

## Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add awesome feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Open a Pull Request

## License
MIT License

