from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain.prompts import MessagesPlaceholder
from langchain_core.messages import HumanMessage

def llm_agentexecutor(llm, tools, system_prompt):
# Each worker node will be given a name and some tools.
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                system_prompt,
            ),
            MessagesPlaceholder(variable_name="messages"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    agent = create_openai_tools_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)
    return executor

#We can also define a function that we will use to be the nodes in the graph - it takes care of converting the agent response to a human message. 
#This is important because that is how we will add it the global state of the graph
def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {"messages": [HumanMessage(content=result["output"], name=name)]}