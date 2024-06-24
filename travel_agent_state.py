import operator
from typing import Annotated, TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from model import llm
from agent_executor import llm_agentexecutor, agent_node
from tools import tools
import functools
import operator
from prompts import template_transportation
from supervisor import create_team_supervisor
from langgraph.graph import StateGraph, END


# The agent state is the input to each node in the graph
class TravelAgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[List[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    team_members: List[str]
    next: str
    

search_agent = llm_agentexecutor(
    llm,
    tools,
    template_transportation
)
search_node = functools.partial(agent_node, agent=search_agent, name="Search")

research_agent = llm_agentexecutor(
    llm,
    tools,
    "You are a research agent research from the user query and summarize the requirements of the mode of travel which a user wants from his query. provide the efficient mode of travel and just focus on travel donot include stay.",
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

travel_graph = StateGraph(TravelAgentState)
travel_graph.add_node("Search", search_node)
travel_graph.add_node("Researcher", research_node)
travel_graph.add_node("localsupervisor", supervisor_agent)

travel_graph.add_edge("Search", "localsupervisor")
travel_graph.add_edge("Researcher", "localsupervisor")
travel_graph.add_conditional_edges(
    "localsupervisor",
    lambda x: x["next"],
    {"Search": "Search", "Researcher": "Researcher", "FINISH": END},
)

travel_graph.set_entry_point("localsupervisor")
chain = travel_graph.compile()

def enter_chain(message: str):
    results = {
        "messages": [HumanMessage(content=message)],
    }
    return results


travel_chain = enter_chain | chain

# for s in travel_chain.stream(
#     "when is Taylor Swift's next tour?", {"recursion_limit": 100}
# ):
#     if "__end__" not in s:
#         print(s)
#         print("---")