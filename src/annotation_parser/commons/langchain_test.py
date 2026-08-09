import requests
from dotenv import load_dotenv

load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool

@tool('get_weather', description="Get weather for a given city.")
def get_weather(city: str) -> str:
    """Get weather for a given city."""
    resopnse = requests.get(f"https://wttr.in/{city}?format=j1")
    return resopnse.json()

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    tools=[get_weather],
    system_prompt="You are a helpful assistant that provides weather information.",
)

result = agent.invoke(
    {"messages": [{"role": "user", "content": "What's the weather in Vienna?"}]}
)
print(result["messages"][-1].content)

