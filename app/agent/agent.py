from langchain_groq import ChatGroq
from langchain.agents import initialize_agent,AgentType
from dotenv import load_dotenv
import os
from agent.tools import debug_tool


load_dotenv()

llm = ChatGroq(
    model="llama-3.1-8b-instant",   # fast + free
    temperature=0,
    api_key=os.getenv("GROQ_API_KEY")
)

def is_code_related(user_input):

    keywords = [
        "error",
        "exception",
        "traceback",
        "bug",
        "print(",
        "def ",
        "class ",
        "syntax"
    ]

    return any(keyword in user_input.lower() for keyword in keywords)


#print(ask_llm("What is the time period of second world war"))
tools = [debug_tool]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

def run_agent(user_input):
    response = agent.run(user_input)
    return response
