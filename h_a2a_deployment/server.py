"""
Sangat_Sync A2A Server
Wraps the main d_routing_agent hero agent to serve A2A protocol requests over HTTP/JSON-RPC.
Exposes /.well-known/agent.json Agent Card for remote discovery.
"""
import os
import sys
import json
from dotenv import load_dotenv

# Ensure parent directory is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from d_routing_agent.agents import root_agent

# Load Agent Card metadata
AGENT_CARD_PATH = os.path.join(os.path.dirname(__file__), "agent_card.json")
with open(AGENT_CARD_PATH, "r", encoding="utf-8") as f:
    AGENT_CARD = json.load(f)


def get_agent_card():
    """Returns the Sangat_Sync Agent Card for discovery."""
    return AGENT_CARD


def create_a2a_app():
    """Builds FastAPI app for serving Sangat_Sync via A2A protocol."""
    from fastapi import FastAPI, Request
    from fastapi.responses import JSONResponse
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(
        title="Sangat_Sync A2A Service",
        description="A dynamic multi-agent system orchestrating your perfect journey.",
        version="1.0.0"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, app_name="sangat_sync", session_service=session_service)

    @app.get("/.well-known/agent.json")
    async def agent_card_endpoint():
        """Agent Card Discovery Endpoint (A2A Specification)."""
        return JSONResponse(content=AGENT_CARD)

    @app.get("/health")
    async def health_check():
        """Health check endpoint for Cloud Run / load balancers."""
        return {"status": "ok", "service": "Sangat_Sync A2A", "project": os.environ.get("GOOGLE_CLOUD_PROJECT", "adk-dev-496506")}

    @app.post("/a2a")
    async def a2a_handler(request: Request):
        """A2A RPC invocation handler."""
        body = await request.json()
        query = body.get("query") or body.get("message") or ""
        user_id = body.get("user_id", "a2a_user")
        session_id = body.get("session_id", "a2a_session")

        if not query:
            return JSONResponse(status_code=400, content={"error": "Missing 'query' field in request body."})

        # Process message through the Sangat_Sync router agent
        session = await session_service.get_session(app_name="sangat_sync", user_id=user_id, session_id=session_id)
        if not session:
            session = await session_service.create_session(app_name="sangat_sync", user_id=user_id, session_id=session_id)

        responses = []
        async for event in runner.run_async(user_id=user_id, session_id=session.id, new_message=query):
            if hasattr(event, 'content') and event.content:
                responses.append(str(event.content))

        final_answer = "\n".join(responses) if responses else "Query processed successfully."
        return {
            "status": "success",
            "agent": "Sangat_Sync Router",
            "response": final_answer,
            "agent_card": AGENT_CARD["url"]
        }

    return app


app = create_a2a_app()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Sangat_Sync A2A Server running on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
