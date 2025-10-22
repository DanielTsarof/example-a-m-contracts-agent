# pip install langchain langgraph langchain-openai
import os
import operator
from typing import Annotated, Literal
import dotenv

from typing_extensions import TypedDict
from langchain.messages import AnyMessage, HumanMessage, SystemMessage, ToolMessage
from langchain.tools import tool
from langchain.chat_models import init_chat_model  # провайдер-агностический init
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition  # готовый узел и router

env_file = dotenv.find_dotenv()
os.environ["OPENAI_API_KEY"] = dotenv.get_key(env_file, key_to_get="OPENAI_API_KEY")


# 1) Модель + инструменты
llm = init_chat_model("openai:gpt-5-mini", temperature=0)  # подставьте свой провайдер/модель
@tool
def multiply(a: int, b: int) -> int:
    "Перемножить a и b"
    return a * b

@tool
def add(a: int, b: int) -> int:
    "Сложить a и b"
    return a + b

tools = [add, multiply]
llm_with_tools = llm.bind_tools(tools)  # модель теперь может вызывать tools

# 2) Схема state (список сообщений + счётчик вызовов)
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

# 3) Узел модели: решает, звать ли tool
def llm_call(state: MessagesState):
    resp = llm_with_tools.invoke(
        [SystemMessage(content="Ты помощник по арифметике. Если нужно — зови tool.")]
        + state["messages"]
    )
    return {"messages": [resp], "llm_calls": state.get("llm_calls", 0) + 1}

# 4) Узел инструментов: исполнить все tool_calls из последнего AIMessage
tool_node = ToolNode(tools)

# 5) Граф: LLM -> (tools?) -> LLM -> ... -> END
builder = StateGraph(MessagesState)
builder.add_node("llm_call", llm_call)
builder.add_node("tools", tool_node)
builder.add_edge(START, "llm_call")
builder.add_conditional_edges("llm_call", tools_condition, {"tools": "tools", "__end__": END})
builder.add_edge("tools", "llm_call")

# 6) Персистентность (in-memory) и компиляция
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

# 7) Вызов с thread_id (память между обращениями)
cfg = {"configurable": {"thread_id": "u1"}}
out = graph.invoke({"messages": [HumanMessage(content="Сложи 3 и 4")]}, cfg)
print(out["messages"][-1].content)
