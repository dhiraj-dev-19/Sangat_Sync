"""
Sangat_Sync Native Database Tools
Direct SQLite tools for querying destinations.db (107 curated global destinations).
Provides clean, fast access to curated trip destinations without external server dependencies.
"""
import sqlite3
import os
from google.adk.tools import ToolContext

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "destinations.db")


def query_destinations_by_city(tool_context: ToolContext, city: str) -> list[dict]:
    """Search for top-rated destinations in a specific city (e.g. 'Mumbai', 'Paris', 'Tokyo')."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, type, rating, average_cost, currency, best_season, description "
        "FROM destinations WHERE LOWER(city) = LOWER(?) ORDER BY rating DESC LIMIT 5",
        (city,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    if rows:
        tool_context.state["user_location"] = city
        return rows
    return [{"message": f"No curated database entries found for '{city}'. Suggest using web search."}]


def query_destinations_by_type(tool_context: ToolContext, city: str, dest_type: str) -> list[dict]:
    """Search destinations of a specific type in a city (e.g. 'Museum', 'Temple', 'Beach', 'Heritage')."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, type, rating, average_cost, currency, description "
        "FROM destinations WHERE LOWER(city) = LOWER(?) AND LOWER(type) = LOWER(?) ORDER BY rating DESC",
        (city, dest_type)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows if rows else [{"message": f"No {dest_type} entries found in '{city}'."}]


def query_affordable_destinations(tool_context: ToolContext, city: str, max_cost: int) -> list[dict]:
    """Find destinations in a city under a maximum average cost in local currency."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, type, rating, average_cost, currency, description "
        "FROM destinations WHERE LOWER(city) = LOWER(?) AND average_cost <= ? ORDER BY average_cost ASC",
        (city, max_cost)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows if rows else [{"message": f"No options under cost {max_cost} in '{city}'."}]


def query_destinations_by_country(tool_context: ToolContext, country: str) -> list[dict]:
    """Find top destinations across an entire country (e.g. 'India', 'Japan', 'France')."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT name, city, type, rating, average_cost, currency, best_season "
        "FROM destinations WHERE LOWER(country) = LOWER(?) ORDER BY rating DESC LIMIT 15",
        (country,)
    )
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return rows if rows else [{"message": f"No destinations found for country '{country}'."}]
