import pandas as pd
import streamlit as st
from datetime import datetime

# Page config
st.set_page_config(page_title="IT Ticket Bot", page_icon="🤖")

st.title("IT Ticket Analysis Chatbot 🤖")

# Load data - wrap in a try/except to catch file errors
try:
    df = pd.read_csv(r'C:\Users\naveena.mk\Downloads\Code_v5\tickets.csv')
    df['CreatedDate'] = pd.to_datetime(df['CreatedDate'])
    
    # Create Aging column
    today = pd.to_datetime(datetime.today())
    df['Aging'] = (today - df['CreatedDate']).dt.days

    # User input
    user_input = st.text_input("Ask your question (e.g., 'show open tickets' or 'p1'):")

    if user_input:
        query = user_input.lower()

        if "open tickets" in query:
            result = df[df['status'] == 'Open']
            st.write(f"### Open Tickets: {len(result)}")
            st.dataframe(result)

        elif "p1" in query:
            result = df[(df['Priority'] == 'P1') & (df['Status'] == 'Open')]
            st.write(f"### P1 Pending Tickets: {len(result)}")
            st.dataframe(result)

        elif "aging" in query:
            result = df[df['Aging'] > 5]
            st.write(f"### Tickets Aging > 5 days: {len(result)}")
            st.dataframe(result)

        elif "team" in query:
            result = df.groupby('Team').size().reset_index(name='Count')
            st.write("### Tickets by Team")
            st.bar_chart(result.set_index('Team')) # Added a little visual flair!
            st.dataframe(result)

        else:
            st.warning("Sorry, I didn't understand. Try asking about 'open tickets', 'p1', 'aging', or 'team'.")

except FileNotFoundError:
    st.error("Error: 'tickets.csv' not found. Please make sure the file is in the same folder as this script.")
    
import streamlit as st
import pandas as pd

@st.cache_data(ttl=60)  # refresh every 60 seconds
def load_data():
    return pd.read_csv(r'C:\Users\naveena.mk\Downloads\Code_v5\tickets.csv')

df = load_data()

import streamlit as st
from openai import OpenAI
client = OpenAI(api_key="YOUR_API_KEY")

def ask_ai(question):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are IT ticket analysis assistant"},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content

user_input = st.text_input("Ask question")

if user_input:
    ai_response = ask_ai(user_input)
    st.write(ai_response)

    #if "critical" in user_input.lower():
    result = df[(df['Priority'] == 'P1') & (df['Status'] == 'Open')]
    st.write(result)

# Option A: Streamlit Charts
import matplotlib.pyplot as plt

# Count by priority
priority_count = df['Priority'].value_counts()

st.bar_chart(priority_count)
# Option B: Show KPIs
st.metric("Total Tickets", len(df))
st.metric("Open Tickets", len(df[df['Status']=="Open"]))
st.metric("P1 Tickets", len(df[df['Priority']=="P1"]))
# Option C: Combine Chat + Dashboard
st.title("IT Ticket Dashboard + Chatbot")

# Dashboard
st.subheader("Overview")
st.bar_chart(df['Priority'].value_counts())

# Chatbot
st.subheader("Ask Questions")
user_input = st.text_input("Type here")

if user_input:
    if "p1" in user_input.lower():
        st.write(df[df['Priority']=="P1"])
   