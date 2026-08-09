from dataclasses import dataclass
from json import tool

from colorama import init
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

@dataclass
class ResponseFormat:
    title: str
    author: str

agent = create_agent(
    model="google_genai:gemini-2.5-flash-lite",
    system_prompt="Clean book title and return only the title and author name",
    response_format=ResponseFormat,
)

def get_clean_book_title(title: str):
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": title,
                }
            ]
        }
    )
    print(response["structured_response"].title, "--", response["structured_response"].author)
    return response["structured_response"].title, response["structured_response"].author