import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import google.generativeai as genai

# Read data from CSV
df = pd.read_csv("sales_data_sample.csv")

# Function to create in-memory SQLite database and execute SQL query
def execute_sql_query(df, sql_query):
    temp_db = create_engine('sqlite:///:memory:', echo=False)
    df.to_sql(name='Sales', con=temp_db, index=False)
    with temp_db.connect() as conn:
        result = conn.execute(text(sql_query))
        rows = result.fetchall()
    return rows

# Function to create a prompt for GPT-3
def create_prompt(df, nlp_text):
    prompt = f'''Given the following sqlite SQL definition, write queries based on the request:
### sqlite SQL table, with its properties:
# Sales({",".join(str(x) for x in df.columns)})
A query to answer: {nlp_text}
'''
    return prompt

# Streamlit app
def main():
    st.title("SQL Query Generator & Data Viewer")

    # User input for information to obtain
    nlp_text = st.text_input("Enter information you want to obtain:", "")

    # Generate SQL query based on user input
    prompt = create_prompt(df, nlp_text)
    
    response = model.generate_content([prompt])
    sql_query = response.text.strip()
    sql_query=sql_query.strip('`sql \n')
    sql_query=sql_query.replace("\n",' ')

    # Execute SQL query and display result
    if st.button("Execute SQL Query"):
        st.write(sql_query)
        rows = execute_sql_query(df, sql_query)
        st.table(pd.DataFrame(rows))

if __name__ == "__main__":
    # Configure GenAI API
    genai.configure(api_key='AIzaSyCTPVa3Co4s8Xf2rnn77BOP8iw642Z1_8E')
    
    # Initialize GenerativeModel
    model = genai.GenerativeModel('gemini-pro')

    main()