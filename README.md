
# Olympics Data Chatbot

This project is an interactive chatbot application built with Streamlit, LangChain, and SQLite. The chatbot can handle both conversational inputs and complex SQL queries related to Olympic data from Athens 1896 to Beijing 2022, providing a seamless user experience.

## Features

- **SQL Query Handling**: The chatbot can answer data-specific questions by generating and executing SQL queries on an in-memory SQLite database containing Olympic data. It can interprets natural language queries, converts them into SQL queries, executes them, and returns the results in a user-friendly format.
- **Chain of Thought Prompting**: The chatbot uses a structured approach to reasoning. For each user query, it generates an SQL query, executes it, and then formulates an answer based on the results, ensuring a logical and transparent reasoning process.
- **In-Memory SQLite Database**: Olympic data is loaded into an in-memory SQLite database for fast and efficient querying.
- **Conversational Capabilities**: The chatbot can engage in simple conversation, responding to greetings and casual questions.
- **Streamlit Interface**: The application uses Streamlit to create an interactive web interface, allowing users to input their questions and receive responses in real-time.

## Data
The data is obtained from Kaggle [Olympic Summer & Winter Games, 1896-2022](https://www.kaggle.com/datasets/piterfm/olympic-games-medals-19862018/data).

The project uses the following data tables:

1. **Athletes**: Information about Olympic athletes, including their names, participations, and medals.
2. **Hosts**: Details of Olympic host cities and events.
3. **Medals**: Records of medals awarded in various Olympic events.
4. **Results**: Results from different Olympic events.

### Data Description

- **Athletes**: `athlete_url`, `athlete_full_name`, `games_participations`, `first_game`, `athlete_year_birth`, `athlete_medals`, `bio`
- **Hosts**: `game_slug`, `game_end_date`, `game_start_date`, `game_location`, `game_name`, `game_season`, `game_year`
- **Medals**: `discipline_title`, `slug_game`, `event_title`, `event_gender`, `medal_type`, `participant_type`, `participant_title`, `athlete_url`, `athlete_full_name`, `country_name`, `country_code`, `country_3_letter_code`
- **Results**: `discipline_title`, `event_title`, `slug_game`, `participant_type`, `medal_type`, `athletes`, `rank_equal`, `rank_position`, `country_name`, `country_code`, `country_3_letter_code`, `athlete_url`, `athlete_full_name`, `value_unit`, `value_type`

## Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)
- Environment variables file (`.env`) with your OpenAI API key.

### Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/olympics-data-chatbot.git
    cd olympics-data-chatbot
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Set up your environment variables:**

    Add your OpenAI API key in the `security_keys.env` file:

    ```env
    OPENAPI_KEY=your_openai_api_key_here
    ```

4. **Prepare the datasets:**

    Ensure the following datasets are available in the `datasets/` directory:
    - `olympic_athletes.csv`
    - `olympic_hosts.csv`
    - `olympic_medals.csv`
    - `olympic_results.csv`

5. **Run the application:**

    ```bash
    streamlit run chatbot_data.py
    ```

    This will start the Streamlit server and open the app in your web browser.

## Usage

1. **Ask a Question**: Enter your question about Olympic data in the text input field.
2. **Submit**: Click the "Submit" button to get a response from the chatbot.
3. **Text to SQL**

### Example Queries

- "Which country has the most number of athletes?"
- "Show me the medals table for the 2020 Tokyo Olympics."
- "List all events in which USA won gold medals."

## Acknowledgements

- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [OpenAI](https://www.openai.com/)
- [SQLite](https://www.sqlite.org/)

---
