# test.py
from promptmodel import PromptModel, Client

client = Client()

prompt = PromptModel("function_call_test").get_prompts()

from typing import Optional
def get_current_weather(location: str, unit: Optional[str]):
    return "13 degrees celsius"