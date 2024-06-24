import operator
from typing import Annotated, Sequence, TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from model import llm
from agent_executor import llm_agentexecutor, agent_node
from tools import tools
import functools
import operator
from supervisor import create_team_supervisor
from langgraph.graph import StateGraph, END
from prompts import template_stay

# The agent state is the input to each node in the graph
class HotelAgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    # This provides each worker with context on the others' skill sets
    messages: Annotated[List[BaseMessage], operator.add]
    team_members: List[str]
    # The 'next' field indicates where to route to next
    next: str

search_agent = llm_agentexecutor(
    llm,
    tools,
    template_stay,
)

search_node = functools.partial(agent_node, agent=search_agent, name="Search")

research_agent = llm_agentexecutor(
    llm,
    tools,
    "You are a research agent research from the user query and summarize the requirements of the hotel which a user wants from his query. If user doesnot specify anything take best requirements a hotel should have and just focus on stay donot include travel options.",
)
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")

supervisor_agent = create_team_supervisor(
    llm,
    "You are a local supervisor tasked with managing a conversation between the"
    " following workers:  Search, Researcher. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. If both the workers are done with the job and finished,"
    " respond with FINISH.",
    ["Search", "Researcher"]
)

stay_graph = StateGraph(HotelAgentState)
stay_graph.add_node("Search", search_node)
stay_graph.add_node("Researcher", research_node)
stay_graph.add_node("localsupervisor", supervisor_agent)

stay_graph.add_edge("Search", "localsupervisor")
stay_graph.add_edge("Researcher", "localsupervisor")
stay_graph.add_conditional_edges(
    "localsupervisor",
    lambda x: x["next"],
    {"Search": "Search", "Researcher": "Researcher", "FINISH": END},
)

stay_graph.set_entry_point("localsupervisor")
chain = stay_graph.compile()

def enter_chain(message: str):
    results = {
        "messages": [HumanMessage(content=message)],
    }
    return results


stay_chain = enter_chain | chain

# for s in stay_chain.stream(
#     "when is Taylor Swift's next tour?", {"recursion_limit": 100}
# ):
#     if "__end__" not in s:
#         print(s)
#         print("---")