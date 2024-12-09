from langchain_groq import ChatGroq
from json import loads
from .prompts import *
from .aiTaskModel import *

def generate(user_request,api_key):
    client = ChatGroq(model = "llama-3.1-70b-versatile",api_key=api_key)
    return loads(client.with_structured_output(Task).invoke(get_prompt(user_request)).json())
