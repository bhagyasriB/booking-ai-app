# Booking AI App

This project uses **LangGraph + LangChain + React + FastAPI** to automatically find the best-rated and normal-priced flights and hotels.

## Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

To install the LangChain package:

pip install -U langchain


======================
Create Agent (sample example)


from langchain.agents import create_agent

def get_weather(city: str) -> str:
    """Get weather for a given city."""
    return f"It's always sunny in {city}!"

agent = create_agent(
    model="claude-sonnet-4-5-20250929",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)

# Run the agent
agent.invoke(
    {"messages": [{"role": "user", "content": "what is the weather in sf"}]}
)

=======================
Model - 
pip install -U "langchain[openai]"

​StandAlone ---

import os
from langchain.chat_models import init_chat_model

os.environ["OPENAI_API_KEY"] = "sk-..."

model = init_chat_model("gpt-4.1")


 With agents ---

import os
from langchain_openai import ChatOpenAI

os.environ["OPENAI_API_KEY"] = "sk-..."

model = ChatOpenAI(model="gpt-4.1")
===========================
response = model.invoke("Why do parrots talk?")

Memory ------

from langgraph.checkpoint.memory import InMemorySaver

agent = create_agent(
    "gpt-5",
    [get_user_info],
    checkpointer=InMemorySaver(),  
)

agent.invoke(
    {"messages": [{"role": "user", "content": "Hi! My name is Bob."}]},
    {"configurable": {"thread_id": "1"}},  
)