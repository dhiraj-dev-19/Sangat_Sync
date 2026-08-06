"""
Sangat_Sync A2A Client
Demonstrates remote discovery of Sangat_Sync via Agent Card and interacting over HTTP/A2A protocol.
"""
import os
import sys
import json
import urllib.request
from dotenv import load_dotenv

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

DEFAULT_SERVER_URL = os.environ.get("SANGAT_SYNC_A2A_URL", "http://127.0.0.1:8080")


def discover_agent(server_url: str) -> dict:
    """Discovers the remote agent by fetching its Agent Card metadata."""
    card_url = f"{server_url.rstrip('/')}/.well-known/agent.json"
    req = urllib.request.Request(card_url, headers={"User-Agent": "Sangat_Sync_Client/1.0"})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def send_a2a_query(server_url: str, query: str, user_id: str = "demo_user") -> dict:
    """Sends a query to the remote Sangat_Sync A2A server."""
    endpoint = f"{server_url.rstrip('/')}/a2a"
    payload = json.dumps({"query": query, "user_id": user_id}).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "Sangat_Sync_Client/1.0"},
        method="POST"
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    server_url = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SERVER_URL
    print("\n" + "=" * 60)
    print("🤖 Sangat_Sync A2A Remote Client")
    print("=" * 60)
    print(f"Connecting to A2A server: {server_url}")

    try:
        card = discover_agent(server_url)
        print(f"\n✅ Agent Card Discovered!")
        print(f"   Name:        {card.get('name')}")
        print(f"   Description: {card.get('description')}")
        print(f"   Version:     {card.get('version')}")
        print(f"   Skills:      {', '.join([s['name'] for s in card.get('skills', [])])}")
    except Exception as e:
        print(f"⚠️ Could not fetch Agent Card from {server_url}: {e}")
        print("Continuing CLI mode...")

    print("\nType your trip planning query (or 'exit' to quit):")

    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                print("🤖 Sangat_Sync Client Goodbye!")
                break
            if not user_input.strip():
                continue

            res = send_a2a_query(server_url, user_input)
            print(f"\nSangat_Sync: {res.get('response')}")
        except Exception as err:
            print(f"❌ Error communicating with A2A server: {err}")


if __name__ == "__main__":
    main()
