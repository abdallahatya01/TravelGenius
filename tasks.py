from crewai import Task

def create_travel_planning_task(agent, web_search_tool):
    return Task(
        description=(
            "Based on the following travel requirements, create a fully formatted, human-readable travel plan "
            "in Markdown. Include actual details for flights, hotels, attractions, and restaurants. "
            "Provide prices, dates, durations, and budget breakdowns.\n\n"
            "Destination: {destination}\n"
            "Budget: ${budget}\n"
            "Duration: {days} days\n"
            "Travelers: {travelers}\n\n"
            "The output MUST be a ready-to-display travel itinerary, not instructions."
        ),
        expected_output=(
"""
You are an expert travel planner. You will receive web search results containing 
information about flights, hotels, attractions, and restaurants. Your job is to 
transform that information into a complete and polished Markdown travel itinerary.

Guidelines:
1. You may freely rewrite, reformat, and combine the useful information from the search results.
2. Do NOT include URLs.
3. Do NOT copy raw search result text.
4. If information is missing, use realistic estimates based on common travel prices.
5. You MUST return a final human-ready travel plan.

Your final itinerary MUST include:

### ✈️ Flights
- Best available flight options
- Airline name
- Dates & duration
- Estimated price per person

### 🏨 Hotels
- 2–4 recommended hotels
- Price per night & total stay cost
- Short pros/cons
- Area description

### 🏛️ Attractions
- 5–10 top attractions
- Entry fees (if any)
- Best visit time
- How long to spend at each place

### 🍽️ Restaurants
- 5 recommended places
- Expected meal cost
- Type of cuisine

### 💰 Budget Breakdown
- Flights cost
- Hotel cost
- Daily spending
- Total per person
- Check if the final plan is within the user’s budget

### 🧭 Final Recommendation
- Summary of the trip
- Note if budget is exceeded or not

Your output MUST be clean, formatted, readable, and structured as a complete Markdown travel plan.
Return ONLY the final itinerary.
"""
        ),
        agent=agent,
        tools=[web_search_tool],
    )
