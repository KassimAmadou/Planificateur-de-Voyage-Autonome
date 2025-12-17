# Autonomous Travel Planning Agent

## Project Overview
This project consists of an autonomous intelligent agent capable of planning fully customized trips based on a simple textual description provided by the user.

The system understands natural language inputs (destination, dates, budget, preferences) and coordinates various external tools to search for flight prices, check weather conditions, suggest activities, and provide practical information (visas, currencies). The end result is an interactive itinerary displayed on a Streamlit dashboard and downloadable in PDF format.

## Team members
* AMADOU Kassim
* AZEMAR Solene
* BELET Marine
* BENABDELJALIL Yanis

## Technical architecture and reasoning strategy

### Choice of reasoning technique: ReAct (Reason + Act)
In order to achieve high reliability in planning, we implemented the **ReAct** architecture. Unlike a simple text generation model, our agent follows a strict iterative loop:

1.  **Reflection:** the agent analyzes the user's request and identifies any missing information or necessary steps (e.g., “I need to check the weather in Tokyo for April before suggesting activities”).
2.  **Action:** The agent autonomously selects and executes a specific tool (weather API or search API).
3.  **Observation:** The agent receives real data from the outside world.
4.  **Self-correction:** The agent evaluates whether the data matches the user's constraints. For example, if the retrieved flight price exceeds the budget, the agent creates a new “thought” to search for cheaper alternatives.

### Technology stack
* **Framework:** LangChain (to manage the ReAct cycle).
* **LLM:** OpenAI GPT-3.5-turbo (as the reasoning engine).
* **Interface:** Streamlit (with callback handlers to visualize the agent's reasoning process in real time).
* **Tools:**
* `Tavily Search API`: for real-time flight data, hotel prices, and cultural information.
* `OpenWeatherMap API`: to check weather consistency with the itinerary.

## Features
* **Natural language processing:** extracts destination, dates, budget, and travel style from unstructured text.
* **Real-time data:** retrieves current weather and real flight/activity suggestions.
* **Smart itinerary generation:** creates a daily schedule with clickable links to activities.
* **Practical information:** automatically provides visa requirements, exchange rates, and packing lists.
* **PDF export:** generates a downloadable report of the entire trip.

## Installation and usage

1.  **Install dependencies:**
```bash
    pip install -r requirements.txt
```

2.  **Configure Environment Variables:**
    Create a `.env` file at the root of the project. You will need API keys from the following services:

    * [OpenAI Key here](https://platform.openai.com/api-keys)
    * [Tavily Key here](https://tavily.com/)
    * [OpenWeatherMap Key here](https://home.openweathermap.org/api_keys)

    Add them to your `.env` file:
    ```
    OPENAI_API_KEY=your_openai_key
    TAVILY_API_KEY=your_tavily_key
    OPENWEATHERMAP_API_KEY=your_openweather_key
    ```

3.  **Run the application:**
```bash
    streamlit run app.py
 ```
4. [Demonstration video](https://drive.google.com/file/d/1yhb5PtJmwe2pVugNEq8AH3rzT6d8JT1l/view?usp=drive_link)
