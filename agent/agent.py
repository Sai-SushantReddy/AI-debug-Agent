from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from agent.tools import analyze_code_tool


load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",   # fast + free
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def ask_llm(query):
    response = llm.invoke(query)
    return response.content

def debug_agent(user_input):
    tool_prompt = analyze_code_tool(user_input)
    response = llm.invoke(tool_prompt)
    return response.content
#print(ask_llm("What is the time period of second world war"))
