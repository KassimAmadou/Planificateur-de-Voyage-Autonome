import os
import requests
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.tools import tool

load_dotenv()

# --- SEARCH TOOL ---
search_tool = TavilySearchResults(
    max_results=3,
    description="Useful for searching flights, hotels, activities, visa/currency info, and price estimates."
)

# --- WEATHER TOOL ---
@tool
def get_current_weather(city: str):
    """
    Useful for getting the weather.
    Input should be JUST the city name (e.g., 'Tokyo'), without 'City:' in front.
    """
    api_key = os.getenv("OPENWEATHERMAP_API_KEY")
    if not api_key: return "Error: Weather API key missing."
    
    # Cleaning in case the AI sends "Ville: Paris" (frequent issue)
    city = city.replace("Ville:", "").replace("City:", "").strip()

    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "en"}
    
    try:
        response = requests.get(base_url, params=params)
        data = response.json()
        if response.status_code == 200:
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            return f"Current weather in {city}: {weather_desc}, {temp}°C"
        else:
            return f"Info: Unable to retrieve real-time weather for {city}. Use the search tool to find seasonal averages."
    except Exception as e:
        return f"Weather error: {str(e)}"

def get_tools():
    return [search_tool, get_current_weather]