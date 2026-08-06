"""
Netlify Serverless Handler for Sangat_Sync A2A Server
Adapts FastAPI app to AWS Lambda / Netlify Serverless Functions via Mangum.
"""
import os
import sys

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, PROJECT_ROOT)

from mangum import Mangum
from h_a2a_deployment.server import app

# Serverless handler for Netlify
handler = Mangum(app, api_gateway_base_path="/.netlify/functions/api")
