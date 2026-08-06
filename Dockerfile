FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project codebase
COPY . .

# Environment configuration
ENV PORT=8080
ENV GOOGLE_GENAI_USE_VERTEXAI=FALSE
ENV GOOGLE_CLOUD_LOCATION=global

EXPOSE 8080

# Command to start the official Google ADK Web Interface + A2A protocol
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8080", "--a2a", "."]
