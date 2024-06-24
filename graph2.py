import functools
from langgraph.graph import StateGraph, END
from prompts import template_stay, template_transportation
from tools import tools
from agent_executor import llm_agentexecutor, agent_node
from model import llm
from agent_state import AgentState
from supervisor import create_team_supervisor
from langchain_core.messages import HumanMessage
members = ["HotelAgent", "TravelAgent"]
supervisor_node = create_team_supervisor(
    llm,
    "You are a super supervisor tasked with managing a conversation between the"
    " following teams: {members} in which travelteam will take care of the travel arrangements like tickets and hotelTeam will take care of the hotel arrangements such as stay and etc. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. If there is no input from user, just finish donot respond to a question produced by agent. If both the workers are done with the job check the generated output if team has generated the correct output as user need and finished,"
    " respond with FINISH. if previous output is same then just Finish.",
    members
)

hotel_agent = llm_agentexecutor(llm, tools, template_stay)
hotel_node = functools.partial(agent_node, agent=hotel_agent, name="HotelAgent")

travel_mode = llm_agentexecutor(llm, tools, template_transportation)
travel_node = functools.partial(agent_node, agent=travel_mode, name="TravelAgent")


workflow = StateGraph(AgentState)

workflow.add_node("HotelAgent", hotel_node)
workflow.add_node("TravelAgent", travel_node)
workflow.add_node("supervisor", supervisor_node)



for member in members:
    # We want our workers to ALWAYS "report back" to the supervisor when done
    workflow.add_edge(member, "supervisor")
# The supervisor populates the "next" field in the graph state
# which routes to a node or finishes34196

conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END

workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)
# Finally, add entrypoint
workflow.set_entry_point("supervisor")

graph = workflow.compile()



def generate_travel_plan(query):
    output=[]
    for s in graph.stream(
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
            if x == 'HotelAgent':
                # print(s3003["TravelTeam"])
                output.append(s["HotelAgent"]['messages'][0].dict())
            if x == 'TravelAgent':
                # print(s["TravelTeam"])
                output.append(s["TravelAgent"]['messages'][0].dict())
            if "__end__" not in s:
                print(s)
                print("---")
    return output

# for s in graph.stream(
#     {
#         "messages": [
#             HumanMessage(content="Give me a economical plan as i want to go from delhi to bhopal using only indigo flight on 10 june and back to delhi at 16 june and i want to stay in a good hotel.")
#         ]
#     }
# ):
#     if "__end__" not in s:
#         print(s)
#         print("----")

# print(generate_travel_plan("Give me a economical plan as i want to go from delhi to bhopal using only indigo flight on 2 july and back to delhi at 8 july and i want to stay in a good hotel."))