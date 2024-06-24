from supervisor import create_team_supervisor
import operator
from typing import Annotated, Sequence, TypedDict, List
from langchain_core.messages import BaseMessage, HumanMessage
from model import llm
import operator
from supervisor import create_team_supervisor
from langgraph.graph import StateGraph, END
from hotel_agent_state import stay_chain
from travel_agent_state import travel_chain
from pydantic import BaseModel
import json

class State(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str
    team_members: List[str]

def get_last_message(state: State) -> str:
    return state["messages"][-1].content


def join_graph(response: dict):
    return {"messages": [response["messages"][-1]]}


team_members = ["TravelTeam", "HotelTeam"]


supervisor_node = create_team_supervisor(
    llm,
    "You are a super supervisor tasked with managing a conversation between the"
    " following teams: {team_members} in which travelteam will take care of the travel arrangements like tickets and hotelTeam will take care of the hotel arrangements such as stay and etc. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. If there is no input from user, just finish donot respond to a question produced by agent. If both the workers are done with the job check the generated output if team has generated the correct output as user need and finished,"
    " respond with FINISH. if previous output is same then just Finish.",
    team_members
)

# Define the graph.
super_graph = StateGraph(State)

super_graph.add_node("TravelTeam", get_last_message | travel_chain | join_graph)
super_graph.add_node(
    "HotelTeam", get_last_message | stay_chain | join_graph
)
super_graph.add_node("supersupervisor", supervisor_node)
super_graph.add_edge("TravelTeam", "supersupervisor")
super_graph.add_edge("HotelTeam", "supersupervisor")
super_graph.add_conditional_edges(
    "supersupervisor",
    lambda x: x["next"],
    {
        "HotelTeam": "HotelTeam",
        "TravelTeam": "TravelTeam",
        "FINISH": END,
    },
)

super_graph.set_entry_point("supersupervisor")
super_graph = super_graph.compile()

# for s in super_graph.stream(
#     {
#         "messages": [
#             HumanMessage(
#                 content="Give me a economical plan as i want to go from delhi to bhopal using only indigo flight on 10 june and back to delhi at 16 june and i want to stay in a good hotel."
#             )
#         ],
#     },
#     {"recursion_limit": 150},
# ):
#     if "__end__" not in s:
#         print(s)
#         print("---")

def generate_travel_plan(query):
    output=[]
    for s in super_graph.stream(
        {
            "messages": [
                HumanMessage(
                    content=query
                )
            ],
        },
        {"recursion_limit": 150},
    ):
        for x in s:
            if x == 'TravelTeam':
                # print(s["TravelTeam"])
                output.append(s["TravelTeam"])
            if "__end__" not in s:
                print(s)
                print("---")
    return output[len(output)-1]['messages'][0].dict()

print(generate_travel_plan("Give me a economical plan as i want to go from delhi to bhopal using only indigo flight on 2 july and back to delhi at 8 july and i want to stay in a good hotel."))