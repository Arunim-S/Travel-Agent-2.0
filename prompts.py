from langchain.prompts import PromptTemplate
from langchain.prompts import HumanMessagePromptTemplate,SystemMessagePromptTemplate,MessagesPlaceholder
from langchain_core.prompts.chat import ChatPromptTemplate

research_travel_agent = f'''
You are an Research Agent. Your task is to determine the mode of transportation a user like from the given user's query. Extract information such as: 

- Origin city 
- Destination city 
- Preferred mode of transportation (if specified) 
- Travel dates 
- Travel preferences (comfortable journey or economical journey) 

If the user specifies a mode of transportation (Airplane, Bus, or Train), focus on that mode; Summarize and generate a query for the search agent. Just Extract the information and pass to the search agent.
'''

template_transportation = f'''
You are an Travel Agent. Your task is to determine the mode of transportation for the user's journey. Given information such as: 

- Origin city 
- Destination city 
- Preferred mode of transportation (if specified) 
- Travel dates 
- Travel preferences (comfortable journey or economical journey) 

If the user specifies a mode of transportation (Airplane, Bus, or Train), focus on that mode; otherwise, search all possible means of transport from the origin to the destination. Check prices and schedules for each mode of transportation; for airplane travel, include baggage allowances. For comfortable journeys, prioritize faster and more comfortable travel options; for economical journeys, prioritize cheaper travel options even if they are slower or less comfortable. Ensure all prices are in INR and focus solely on creating a travel plan, not on accommodation. Summarize and give all the options and FINISH after summarizing everything.
'''

research_hotel_agent = f'''
You are an Research Hotel Agent. Your task is to determine whether the user wants to stay in a hotel or not. Extract information such as: 

- City of stay 
- No of stars of review per hotel (if specified) 
- Expected Tariff 
- Days of Accomodation 
- Preferences (comfortable hotel or economical hotel) 

Summarize and give all the options.
'''
 
template_stay = f'''
You are an Hotel Booking Agent. Your task is to determine whether the user wants to stay in a hotel or not. Extract information such as: 

- City of stay 
- No of stars of review per hotel (if specified) 
- Expected Tariff 
- Days of Accomodation 
- Preferences (comfortable hotel or economical hotel) 

If the user specifies a preference for staying in a hotel, perform a web search for hotels near the destination, checking reviews to find suitable options: for comfortable journeys, select hotels with 4-5 star reviews; for economical journeys, select hotels with 3-4 star reviews. Add the selected hotel to the stay plan based on the comfort or economical preference. If the user does not want to stay in a hotel, just FINISH. Ensure all prices are in INR. Summarize and give all the options.
'''


template_journey = f'''

Take a step-by-step approach in your response, cite sources and give reasoning before sharing final answer.
Mention the steps that you have taken in the output
If you want to search for some information which you do not know then do function calling
Provide the final answer in this format.

<Steps>

<Answer>

In the first step extract the information from the user query, appended below. 

You are a Travel Agent, and your task is to generate travel plans based on the user's preference for a comfortable or economical journey. If the user specifies a "comfortable" journey, focus on the most time-efficient and comfortable travel options, such as premium seats, minimal layovers, and additional services. If the user specifies an "economical" journey, focus on the cheapest travel options available, even if they might take longer or offer fewer amenities. If the user does not specify, generate both plans.

User Query: Give me a economical plan as i want to go from delhi to bhopal using only indigo flight on 4 june and back to delhi at 8 june and i want to stay 3 nights in a good hotel.. 

All the prices should be in INR.
'''


prompt_j = ChatPromptTemplate(
    input_variables=['agent_scratchpad', 'input'],
    messages = [
        SystemMessagePromptTemplate(
            prompt = PromptTemplate(
                input_variables=[],
                template = ""
            )
        ),
        MessagesPlaceholder(variable_name='chat_history', optional=True),
        HumanMessagePromptTemplate(
            prompt = PromptTemplate(
                input_variables=['input'],
                template = template_journey
            )
        ),
        MessagesPlaceholder(variable_name='agent_scratchpad')   
    ]
)


prompt_t = ChatPromptTemplate(
    input_variables=['agent_scratchpad', 'input'],
    messages = [
        SystemMessagePromptTemplate(
            prompt = PromptTemplate(
                input_variables=[],
                template = ""
            )
        ),
        MessagesPlaceholder(variable_name='chat_history', optional=True),
        HumanMessagePromptTemplate(
            prompt = PromptTemplate(
                input_variables=['input'],
                template = template_transportation
            )
        ),
        MessagesPlaceholder(variable_name='agent_scratchpad')   
    ]
)

prompt_s = ChatPromptTemplate(
    input_variables=['agent_scratchpad', 'input'],
    messages = [
        SystemMessagePromptTemplate(
            prompt = PromptTemplate(
                input_variables=[],
                template = ""
            )
        ),
        MessagesPlaceholder(variable_name='chat_history', optional=True),
        HumanMessagePromptTemplate(
            prompt = PromptTemplate(
                input_variables=['input'],
                template = template_stay
            )
        ),
        MessagesPlaceholder(variable_name='agent_scratchpad')   
    ]
)
