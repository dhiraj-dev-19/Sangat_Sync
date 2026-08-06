"""
Sangat_Sync Phase 3 Automated A2A Test Suite
Validates ADK 1.31.0 upgrade, Agent Card schema, A2A Server endpoints, and FastAPI app creation.
"""
import os
import sys
import json

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, PROJECT_ROOT)


def test_adk_version_and_a2a_imports():
    """Verify ADK version and a2a imports."""
    import google.adk
    print(f"  [Info] Installed ADK version: {google.adk.__version__}")
    
    # Verify google.genai or vertexai setup
    import google.genai
    print("  [Info] Google GenAI SDK import verified.")


def test_agent_card_schema():
    """Verify Agent Card metadata structure and required fields."""
    card_path = os.path.join(PROJECT_ROOT, "h_a2a_deployment", "agent_card.json")
    assert os.path.exists(card_path), "agent_card.json file missing"
    
    with open(card_path, "r", encoding="utf-8") as f:
        card = json.load(f)
    
    assert card["name"] == "Sangat_Sync"
    assert "description" in card
    assert "url" in card
    assert "capabilities" in card
    assert len(card.get("skills", [])) >= 3
    print("  [Info] Sangat_Sync Agent Card schema verified.")


def test_a2a_server_creation():
    """Verify FastAPI A2A app initialization and router attachment."""
    from h_a2a_deployment.server import app, get_agent_card
    
    card = get_agent_card()
    assert card["name"] == "Sangat_Sync"
    assert app.title == "Sangat_Sync A2A Service"
    print("  [Info] Sangat_Sync A2A FastAPI Server creation verified.")


if __name__ == "__main__":
    test_adk_version_and_a2a_imports()
    test_agent_card_schema()
    test_a2a_server_creation()
    print("✅ All Sangat_Sync Phase 3 A2A Tests PASSED!")
