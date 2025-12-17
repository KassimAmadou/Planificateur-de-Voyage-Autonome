def get_travel_prompt(user_input):
    """
    Generates a travel planning prompt based on user input.
    
    Args:
        user_input (str): The user's travel request.
    
    Returns:
        str: The formatted prompt for the agent.
    """
    return f"""
    {user_input}
    
    --------------------------------------------------
    MANDATORY TASKS TO BE PERFORMED BY THE AGENT:
    1. Use the search tool to find real Flights and Hotels.
    2. Use the weather tool (or search) to check the climate.
    3. Find an estimate for car rental (MANDATORY).
    4. Create a coherent day-by-day itinerary.
    
    --------------------------------------------------
    STRICT RESPONSE FORMAT (Respect this order):
    
    [SUMMARY]
    DESTINATION: ...
    PERIOD: ...
    BUDGET: ...
    STYLE: ...
    WEATHER: ...
    
    [PRACTICAL]
    - VISA: ...
    - LUGGAGE: ...
    - CURRENCY: ...
    
    [TRANSPORT]
    - CAR RENTAL: (Estimated price and recommended vehicle type)
    - SUGGESTED FLIGHTS: (Estimated price)
    
    [ITINERARY]
    IMPORTANT: For each activity, create a clickable Markdown link to a Google search.
    Format: [Activity Name](https://www.google.com/search?q=Google+Search)
    
    Day 1: [Day Title]
    - Arrival and check-in
    
    Day 2: [Day Title]
    - Visit [Place A](link...)
    - Lunch
    
    (Etc for all days)
    """