import pandas as pd
import os
import dotenv
import sqlite3
import streamlit as st
from langchain.prompts.prompt import PromptTemplate
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain.agents import AgentExecutor
from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_community.agent_toolkits import create_sql_agent
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_community.utilities import SQLDatabase

def load_env_vars():
    """Load environment variables from .env file."""
    dotenv_path = 'security_keys.env'
    dotenv.load_dotenv(dotenv_path=dotenv_path)
    openai_api_key = os.getenv('OPENAIAPI_KEY')
    return openai_api_key


def create_in_memory_db():
    """Create an in-memory SQLite database and populate it with Olympic data."""
    conn = sqlite3.connect(":memory:")
    return conn

def initialize_database():
    """Initialize SQLDatabase and return it."""
    db = SQLDatabase.from_uri("sqlite:///olympics_db.db")
    print(db.dialect)
    print(db.get_usable_table_names())
    db.run("SELECT * FROM Athletes LIMIT 10;")
    return db

def backup_db_to_file(in_memory_conn):
    """Backup in-memory SQLite database to a file."""
    conn_file = sqlite3.connect("olympics_db.db")
    with conn_file:
        in_memory_conn.backup(conn_file)

def load_data_to_db(conn):
    """Load Olympic data into SQLite database."""
    olympic_athletes = pd.read_csv("datasets/olympic_athletes.csv")
    olympic_hosts = pd.read_csv("datasets/olympic_hosts.csv")
    olympic_medals = pd.read_csv("datasets/olympic_medals.csv")
    olympic_results = pd.read_csv("datasets/olympic_results.csv")

    olympic_athletes.to_sql("Athletes", conn, index=False, if_exists="append")
    olympic_hosts.to_sql("Hosts", conn, index=False, if_exists="append")
    olympic_medals.to_sql("Medals", conn, index=False, if_exists="append")
    olympic_results.to_sql("Results", conn, index=False, if_exists="append")

def setup_agent(openai_api_key, db):
    """Set up the SQL agent."""
    llm = ChatOpenAI(openai_api_key=openai_api_key, model="gpt-3.5-turbo", temperature=0)
    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-tools", verbose=True)
    return llm, agent_executor

def create_chains(llm, db):
    """Create and return the chains for query execution and answer generation."""
    execute_query = QuerySQLDataBaseTool(db=db)
    write_query = create_sql_query_chain(llm, db)
    answer_prompt = PromptTemplate.from_template(
        """Given the following user question, corresponding SQL query, and SQL result, answer the user question. Detail all steps taken by the model to reach the answer.

        Question: {question}
        SQL Query: {query}
        SQL Result: {result}
        Answer: """
    )

    answer = answer_prompt | llm | StrOutputParser()
    chain = (
        RunnablePassthrough.assign(query=write_query).assign(
            result=itemgetter("query") | execute_query
        )
        | answer
    )
    return chain

def display_data_description():
    """Display descriptions of the dataframes available in the database."""
    st.sidebar.header("DataFrames Description")
    st.sidebar.write("""
    **1. Athletes**: Contains information about Olympic athletes, including their full names, games participations, and medals.
    - Columns: `athlete_url`, `athlete_full_name`, `games_participations`, `first_game`, `athlete_year_birth`, `athlete_medals`, `bio`
    
    **2. Hosts**: Contains information about Olympic host cities.
    - Columns: `game_slug`, `game_end_date`, `game_start_date`, `game_location`, `game_name`, `game_season`, `game_year`

    **3. Medals**: Contains information about medals awarded in various events.
    - Columns: `discipline_title`, `slug_game`, `event_title`, `event_gender`, `medal_type`, `participant_type`, `participant_title`, `athlete_url`, `athlete_full_name`, `country_name`, `country_code`, `country_3_letter_code`

    **4. Results**: Contains information about the results of various events.
    - Columns: `discipline_title`, `event_title`, `slug_game`, `participant_type`, `medal_type`, `athletes`, `rank_equal`, `rank_position`, `country_name`, `country_code`, `country_3_letter_code`, `athlete_url`, `athlete_full_name`, `value_unit`, `value_type`
    """)

def main():
    """Main function to run the Streamlit app."""
    st.title("Olympics Data Chatbot")
    
    try:
        openai_api_key = load_env_vars()
    except ValueError as e:
        st.error(str(e))
        return
    
    # Create in-memory database and backup
    conn = create_in_memory_db()
    load_data_to_db(conn)
    backup_db_to_file(conn)
    
    # Initialize database and agent
    db = initialize_database()
    llm, agent_executor = setup_agent(openai_api_key, db)
    
    # Display data descriptions
    display_data_description()

    # Streamlit input and output
    user_question = st.text_input("Enter your question about Olympic data:")
    
    if st.button("Submit"):
        if user_question:
            # Create and run chains
            chain = create_chains(llm, db)
            response = chain.invoke({"question": user_question})
            st.write(response)
        else:
            st.warning("Please enter a question.")

if __name__ == "__main__":
    main()