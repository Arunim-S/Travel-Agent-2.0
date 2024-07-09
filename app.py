import streamlit as st
from graph2 import generate_travel_plan

st.title("Travel Plan Generator")

query = st.text_input("Enter your travel query:")

# Create a button to submit the query
if st.button("Generate Travel Plan"):
    if query:
        response = generate_travel_plan(query)
        st.write("Travel Plan:")
        for x in response:
            st.write(x["content"])
    else:
        st.error("Please enter a query")
