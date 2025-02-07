from fastapi import FastAPI  
from pydantic import BaseModel  
from typing import List  
from langchain_community.tools.tavily_search import TavilySearchResults  
from dotenv import load_dotenv
import os  
from langgraph.prebuilt import create_react_agent  
from langchain_groq import ChatGroq  

load_dotenv()

groq_api_key=os.getenv("GROQ_API_KEY")  

MODEL_NAMES = [
    "llama-3.3-70b-versatile",  
    "deepseek-r1-distill-llama-70b",
    "gemma2-9b-it"  
]

tool_tavily = TavilySearchResults(tavily_api_key=os.getenv("TAVILY_API_KEY"), max_results=2)

tools = [tool_tavily, ]

app = FastAPI(title='LangGraph AI Agent ChatBot')

class RequestState(BaseModel):
    model_name: str  
    system_prompt: str  
    messages: List[str] 

@app.post("/chat")
def chat_endpoint(request: RequestState):
    if request.model_name not in MODEL_NAMES:
        return {"error": "Invalid model name. Please select a valid model."}

    llm = ChatGroq(groq_api_key=groq_api_key, model_name=request.model_name)

    agent = create_react_agent(llm, tools=tools, state_modifier=request.system_prompt)

    state = {"messages": request.messages}

    result = agent.invoke(state) 

    return result

if __name__ == '__main__':
    import uvicorn  
    uvicorn.run(app, host='127.0.0.1', port=(int)(os.getenv("PORT"))) 