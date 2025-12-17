from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from tools import get_tools
import os
from dotenv import load_dotenv

load_dotenv()

def get_agent():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    tools = get_tools()

    template = """
    You are an expert Autonomous Travel Planner.
    
    Available tools:
    {tools}
    
    Tool names: {tool_names}
    
    PROCESS (ReAct):
    Question: The travel request
    Thought: I need to analyze the request.
    Action: The action to take [{tool_names}]
    Action Input: The input for the action
    Observation: The result of the action
    ... (Repeat Thought/Action/Observation)
    Thought: I have all the info. I generate the final answer.
    Final Answer: The complete plan respecting the requested format.
    
    Question: {input}
    Thought:{agent_scratchpad}
    """

    prompt = PromptTemplate.from_template(template)
    agent = create_react_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True, 
        handle_parsing_errors=True
    )