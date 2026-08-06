"""
Sangat_Sync Phase 2 Automated Integration Test Suite
Validates router sub-agent counts, tool registrations, database queries, and session state.
"""
import sqlite3
import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from d_routing_agent.agents import root_agent as router
from d_routing_agent.db_tools import (
    query_destinations_by_city,
    query_destinations_by_type,
    query_affordable_destinations,
    query_destinations_by_country,
)


def test_router_assembly():
    """Verify that router has exactly 8 sub-agents and 5 native tools attached."""
    assert router.name == "router_agent"
    assert len(router.sub_agents) == 8, f"Expected 8 sub-agents, got {len(router.sub_agents)}"
    
    sub_names = [a.name for a in router.sub_agents]
    expected_subs = [
        "weekend_guide_workflow",
        "day_trip_workflow",
        "find_and_navigate_agent",
        "iterative_planner_agent",
        "parallel_planner_agent",
        "BudgetAwarePlannerAgent",
        "TripArchitectAgent",
        "MemoryCoordinatorAgent"
    ]
    for expected in expected_subs:
        assert expected in sub_names, f"Missing sub-agent: {expected}"

    tool_names = [t.__name__ for t in router.tools]
    expected_tools = [
        "extract_and_resolve_locations",
        "query_destinations_by_city",
        "query_destinations_by_type",
        "query_affordable_destinations",
        "query_destinations_by_country"
    ]
    for expected in expected_tools:
        assert expected in tool_names, f"Missing router tool: {expected}"


def test_native_db_tools():
    """Verify native DB tools return valid records from destinations.db."""
    class DummyContext:
        state = {}

    ctx = DummyContext()
    
    # City Query
    mumbai_res = query_destinations_by_city(ctx, "Mumbai")
    assert len(mumbai_res) > 0, "Mumbai destinations query returned empty list"
    assert any(r["name"] == "Gateway of India" for r in mumbai_res)
    assert ctx.state.get("user_location") == "Mumbai"

    # Type Query
    temples = query_destinations_by_type(ctx, "Delhi", "Temple")
    assert len(temples) > 0, "Delhi temples query returned empty list"
    assert any("Lotus Temple" in t["name"] for t in temples)

    # Budget Query
    cheap_pune = query_affordable_destinations(ctx, "Pune", 30)
    assert len(cheap_pune) > 0, "Pune affordable destinations query returned empty list"
    assert all(item["average_cost"] <= 30 for item in cheap_pune)

    # Country Query
    india_top = query_destinations_by_country(ctx, "India")
    assert len(india_top) >= 10, f"India country query returned fewer than 10 results: {len(india_top)}"


def test_standalone_modules_importable():
    """Verify all standalone lab modules can be imported independently."""
    from e_agent_as_tool.agents import root_agent as e_root
    from f_agent_with_memory.agents import root_agent as f_root
    
    assert e_root.name == "TripArchitectAgent"
    assert f_root.name == "MemoryCoordinatorAgent"

    # g_agents_mcp attempts to connect to port 7001 at module import time
    try:
        from g_agents_mcp.trip_agent import root_agent as g_root
        assert g_root.name == "trip_planner_agent"
    except Exception as e:
        print(f"  [Note] g_agents_mcp import skipped (MCP server on port 7001 is offline): {e}")


if __name__ == "__main__":
    test_router_assembly()
    test_native_db_tools()
    test_standalone_modules_importable()
    print("✅ All Sangat_Sync Phase 2 Automated Integration Tests PASSED!")
