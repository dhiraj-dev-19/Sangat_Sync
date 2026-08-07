"""
Sangat_Sync Unified Server
Serves:
1. Public Landing Page at GET / (public/index.html)
2. Official Google ADK Developer Web UI at GET /dev-ui/
3. A2A Agent Card Discovery at GET /.well-known/agent.json
4. A2A RPC Invocation Endpoint at POST /a2a
5. Health Check at GET /health
"""
import os
import sys
import json
from dotenv import load_dotenv

# Ensure parent directory is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
load_dotenv(os.path.join(PROJECT_ROOT, ".env"))

from fastapi.responses import FileResponse, JSONResponse
from google.adk.cli.fast_api import get_fast_api_app

# Load Agent Card metadata
AGENT_CARD_PATH = os.path.join(os.path.dirname(__file__), "agent_card.json")
with open(AGENT_CARD_PATH, "r", encoding="utf-8") as f:
    AGENT_CARD = json.load(f)


def get_agent_card():
    """Returns the Sangat_Sync Agent Card for discovery."""
    return AGENT_CARD


def create_unified_app():
    """Builds unified FastAPI app serving Landing Page, ADK Web UI, and A2A Protocol."""
    # 1. Initialize ADK's full FastAPI app (includes /dev-ui/, WebSocket, tool tracing, runner)
    app = get_fast_api_app(
        agents_dir=PROJECT_ROOT,
        web=True,
        a2a=True,
        use_local_storage=True
    )
    app.title = "Sangat_Sync A2A Service"

    # 2. Override default root redirect so GET / serves public/index.html landing page
    app.router.routes = [r for r in app.router.routes if getattr(r, "path", "") != "/"]

    @app.get("/")
    async def serve_landing_page():
        """Serves the Sangat_Sync HTML landing page."""
        public_index = os.path.join(PROJECT_ROOT, "public", "index.html")
        if os.path.exists(public_index):
            return FileResponse(public_index)
        return {"status": "Sangat_Sync A2A Server Active", "agent_card": "/.well-known/agent.json"}

    @app.get("/.well-known/agent.json")
    async def agent_card_endpoint():
        """Agent Card Discovery Endpoint (A2A Specification)."""
        return JSONResponse(content=AGENT_CARD)

    @app.get("/health")
    async def health_check():
        """Health check endpoint for Cloud Run / Render / load balancers."""
        return {
            "status": "ok",
            "service": "Sangat_Sync Unified ADK & A2A Server",
            "project": os.environ.get("GOOGLE_CLOUD_PROJECT", "adk-dev-496506")
        }

    return app


app = create_unified_app()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    print(f"🚀 Sangat_Sync Unified ADK & A2A Server running on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port)
