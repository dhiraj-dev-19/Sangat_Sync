from google.adk.agents import Agent, SequentialAgent
from google.adk.tools import google_search, ToolContext
import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from b3_loop_agent.agents import iterative_planner_agent
from b2_parallel_agent.agents import parallel_planner_agent
from c_custom_agent.agents import root_agent as custom_agent
from e_agent_as_tool.agents import root_agent as trip_architect_agent
from f_agent_with_memory.agents import root_agent as memory_agent
from d_routing_agent.db_tools import (
    query_destinations_by_city,
    query_destinations_by_type,
    query_affordable_destinations,
    query_destinations_by_country,
)
from dotenv import load_dotenv

load_dotenv()

# --- Agent Definitions for our Specialist Team ---
day_trip_agent = Agent(
    name="day_trip_agent",
    model="gemini-2.5-flash",
    description="Agent specialized in generating spontaneous full-day itineraries based on mood, interests, and budget.",
    instruction="""
    You are the "Spontaneous Day Trip" Generator 🚗 - a specialized AI assistant that creates engaging full-day itineraries.

    Your Mission:
    Transform a simple mood or interest into a complete day-trip adventure with real-time details, while respecting a budget.

    Guidelines:
    1. **Budget-Aware**: Pay close attention to budget hints like 'cheap', 'affordable', or 'splurge'. Use Google Search to find activities (free museums, parks, paid attractions) that match the user's budget.
    2. **Full-Day Structure**: Create morning, afternoon, and evening activities.
    3. **Real-Time Focus**: Search for current operating hours and special events.
    4. **Mood Matching**: Align suggestions with the requested mood (adventurous, relaxing, artsy, etc.).

    RETURN itinerary in MARKDOWN FORMAT with clear time blocks and specific venue names.
    """,
    tools=[google_search]
)

foodie_agent = Agent(
    name="foodie_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""You are an expert food critic. Your goal is to find the best restaurant based on a user's request.

    When you recommend a place, you must output *only* the name of the establishment and nothing else.
    For example, if the best sushi is at 'Jin Sho', you should output only: Jin Sho
    """,
    output_key="destination"
)

transportation_agent = Agent(
    name="transportation_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="""You are a navigation assistant. Given a destination, provide clear directions.
    The user wants to go to: { destination? }.

    Analyze the user's full original query to find their starting point.
    Then, provide clear directions from that starting point to { destination? }.
    """,
)

find_and_navigate_agent = SequentialAgent(
    name="find_and_navigate_agent",
    sub_agents=[foodie_agent, transportation_agent],
    description="A workflow that first finds a location and then provides directions to it."
)

weekend_guide_agent = Agent(
    name="weekend_guide_agent",
    model="gemini-2.5-flash",
    tools=[google_search],
    instruction="You are a local events guide. Your task is to find interesting events, concerts, festivals, and activities happening on a specific weekend."
)

day_trip_workflow = SequentialAgent(
    name="day_trip_workflow",
    sub_agents=[day_trip_agent],
    description="A workflow that plans a full day itinerary."
)

weekend_guide_workflow = SequentialAgent(
    name="weekend_guide_workflow",
    sub_agents=[weekend_guide_agent],
    description="A workflow that finds weekend events."
)


# --- Location Extraction Tool ---
def extract_and_resolve_locations(
    tool_context: ToolContext,
    locations: list[dict]
) -> dict:
    """Extracts and classifies locations from user input.

    Args:
        locations: List of dicts with 'name' and 'role' keys.
                   Role must be one of: 'origin', 'destination', 'stopover', 'ambiguous'.
                   Example: [{"name": "Delhi", "role": "origin"},
                             {"name": "Mumbai", "role": "destination"}]

    Returns:
        dict with status and resolved locations.
    """
    origins = [loc for loc in locations if loc.get("role") == "origin"]
    destinations = [loc for loc in locations if loc.get("role") == "destination"]
    stopovers = [loc for loc in locations if loc.get("role") == "stopover"]
    ambiguous = [loc for loc in locations if loc.get("role") == "ambiguous"]

    if ambiguous:
        return {
            "status": "needs_clarification",
            "message": f"Multiple locations detected. Please clarify the role of: {[l['name'] for l in ambiguous]}"
        }

    # Store in session state
    if destinations:
        tool_context.state["user_destination"] = destinations[0]["name"]
    if origins:
        tool_context.state["user_origin"] = origins[0]["name"]
    if stopovers:
        tool_context.state["user_stopovers"] = [s["name"] for s in stopovers]

    # Set primary location for sub-agents to use
    primary = destinations[0]["name"] if destinations else (origins[0]["name"] if origins else "")
    tool_context.state["user_location"] = primary

    return {"status": "resolved", "primary_location": primary}


# --- The Brain of the Operation: The Sangat_Sync Coordinator ---
new_router_instruction = """
You are the Sangat_Sync Coordinator — a master orchestrator for a dynamic team of specialist AI travel agents.

Tagline: "A dynamic multi-agent system orchestrating your perfect journey."

CRITICAL FIRST STEP:
Before delegating to any sub-agent, you MUST:
1. Extract locations using 'extract_and_resolve_locations'.
2. Query the curated database using 'query_destinations_by_city' or 'query_destinations_by_country' if looking for verified local recommendations.
If 'extract_and_resolve_locations' returns 'needs_clarification', ask the user to clarify before proceeding.

--- Decision-Making Process ---
Think step-by-step to make the most accurate choice. Follow this priority order:

1.  **Is there a BUDGET?** If the user mentions money, cost, or a price (e.g., "$", "₹", "€", "dollars", "rupees", "cheap", "under 100"), you MUST use the `BudgetAwarePlannerAgent`.
2.  **Does the user want PERSONALIZED recommendations or mention past preferences?** Use `MemoryCoordinatorAgent`.
3.  **Does the user need a VALIDATED itinerary with travel times checked & self-corrected?** Use `TripArchitectAgent`.
4.  **Is there a specific CONSTRAINT requiring iteration?** Use `iterative_planner_agent`.
5.  **Are there MULTIPLE, DIVERSE requests at once?** Use `parallel_planner_agent`.
6.  **Simple day trip request?** Use `day_trip_workflow`.
7.  **Weekend events request?** Use `weekend_guide_workflow`.
8.  **Find a place and get directions?** Use `find_and_navigate_agent`.

--- Agent Capabilities ---

- `BudgetAwarePlannerAgent`: Plans a full trip while staying under a specific monetary budget.
- `MemoryCoordinatorAgent`: Remembers and updates user preferences across sessions.
- `TripArchitectAgent`: Autonomous architect that finds activities, validates travel logistics, and self-corrects.
- `iterative_planner_agent`: Workflow that iteratively refines travel plans based on constraints until optimal.
- `parallel_planner_agent`: High-speed research assistant that finds multiple things simultaneously.
- `day_trip_workflow`: Simple single-day planner.
- `weekend_guide_workflow`: Local guide for finding weekend events and festivals.
- `find_and_navigate_agent`: Finds a location and provides navigation directions.

--- Direct Database Tools ---
- `query_destinations_by_city`: Gets top-rated attractions in a city from the curated 107-destination database.
- `query_destinations_by_type`: Filters attractions by type (Museum, Temple, Beach, Heritage, Park).
- `query_affordable_destinations`: Finds attractions under a max cost threshold in local currency.
- `query_destinations_by_country`: Lists top destinations across an entire country.

--- Global Awareness ---
- Support ALL countries and cities worldwide
- Understand currency context: ₹ = INR, $ = USD, € = EUR, £ = GBP, ¥ = JPY
- Respect seasonal and cultural travel contexts

--- Examples ---
- User: "Plan a day in Mumbai for me for under ₹5000." -> `BudgetAwarePlannerAgent`
- User: "I love art museums and spicy food, remember that." -> `MemoryCoordinatorAgent`
- User: "Plan a trip in Delhi and check travel times between places." -> `TripArchitectAgent`
- User: "Plan a trip to Jaipur, but minimize travel time." -> `iterative_planner_agent`
- User: "Find me a temple, a local market, and a place for biryani." -> `parallel_planner_agent`
- User: "What are some fun things I can do today in Bangalore?" -> `day_trip_workflow`

Now, analyze the user's request and orchestrate the correct agent or tool.
"""

router_agent = Agent(
    name="router_agent",
    model="gemini-2.5-flash",
    instruction=new_router_instruction,
    tools=[
        extract_and_resolve_locations,
        query_destinations_by_city,
        query_destinations_by_type,
        query_affordable_destinations,
        query_destinations_by_country,
    ],
    sub_agents=[
        weekend_guide_workflow,
        day_trip_workflow,
        find_and_navigate_agent,
        iterative_planner_agent,
        parallel_planner_agent,
        custom_agent,
        trip_architect_agent,
        memory_agent,
    ],
)

print("🤖 Sangat_Sync agent team assembled with 8 sub-agents and 5 native tools!")
root_agent = router_agent