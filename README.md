# Sangat_Sync — Multi-Agent Trip Planner

> *"A dynamic multi-agent system orchestrating your perfect journey."*

A global AI-powered trip planning system built with Google's Agent Development Kit (ADK). Sangat_Sync uses a team of specialized agents — routing, sequential, parallel, loop, custom, and memory-based — to generate personalized travel plans for any destination worldwide.

## Features

- 🌍 **Global Coverage**: Plan trips for India, Asia, Europe, Americas, Africa, and Oceania
- 🧠 **Intelligent Routing**: Master coordinator agent delegates to the best specialist
- ⚡ **Parallel Research**: Find museums, restaurants, and events simultaneously
- 🔄 **Iterative Refinement**: Plans are critiqued and improved through feedback loops
- 💰 **Budget-Aware**: Custom agent tracks costs against your budget in any currency (₹, $, €, £)
- 📍 **Location-Smart**: Extracts and resolves multiple locations with disambiguation
- 🗄️ **Persistent Memory**: Remembers your preferences across sessions
- 🔍 **Real-Time Search**: Uses Google Search for current events and venues
- 🏛️ **Curated Database**: 107 verified destinations across 23 countries, 6 continents

## Architecture

```
Sangat_Sync (Router Agent)
├── a_single_agent          — Basic day trip planning
├── b1_sequential_agent     — Foodie → Navigation pipeline
├── b2_parallel_agent       — Museum + Concert + Restaurant in parallel
├── b3_loop_agent           — Iterative plan critique/refinement
├── b4_manual_sequential    — Manual router → worker agents
├── c_custom_agent          — Budget-aware planner (BaseAgent)
├── d_routing_agent         — Master orchestrator (hero agent)
├── e_agent_as_tool         — Agents used as tools by other agents
├── f_agent_with_memory     — Session persistence with SQLite
└── g_agents_mcp            — MCP Toolbox with database queries
```

## Prerequisites

- Python 3.9 or higher
- Google Cloud SDK installed and authenticated (`gcloud auth login`)

## Quick Setup

### For Windows Users

```cmd
setup_venv.bat
```

### For Mac/Linux Users

```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

### What the Script Does

1. **Checks for Python**: Ensures you have Python 3.9 or higher.
2. **Creates a Virtual Environment**: Sets up a dedicated `.adk_env` directory.
3. **Installs Dependencies**: Installs the required Python packages from `requirements.txt`.
4. **Prompts for Project ID**: Asks for your Google Cloud Project ID.
5. **Creates `.env` File**: Generates a `.env` file with the following configuration:

    ```env
    GOOGLE_GENAI_USE_VERTEXAI=TRUE
    GOOGLE_CLOUD_PROJECT=your_project_id
    GOOGLE_CLOUD_LOCATION=global
    ```

### Set Up the Destinations Database

```bash
python setup_trip_database.py
```

This creates `destinations.db` with **107 verified global destinations** across:
- 🇮🇳 **76 India destinations** (including 20 Maharashtra)
- 🌏 **31 global destinations** across 22 countries

## Running the Agent

After the setup is complete:

1. **Activate the virtual environment**:

    **Mac/Linux:**
    ```bash
    source .adk_env/bin/activate
    ```

    **Windows:**
    ```cmd
    .adk_env\Scripts\activate
    ```

2. **Run the ADK web interface**:

    ```bash
    adk web
    ```

3. **Or run a specific agent from the command line**:

    ```bash
    adk run d_routing_agent
    ```

## Agent Modules

| Module | Type | What It Does |
|--------|------|-------------|
| `a_single_agent` | LLM Agent | Generates creative day trip plans with Google Search |
| `b1_sequential_agent` | SequentialAgent | Finds a restaurant, then gives directions to it |
| `b2_parallel_agent` | ParallelAgent | Searches for museum + concert + restaurant simultaneously |
| `b3_loop_agent` | LoopAgent | Iteratively refines travel plans based on constraints |
| `b4_manual_sequential` | Manual Router | Demonstrates manual routing logic with Python |
| `c_custom_agent` | CustomAgent (BaseAgent) | Budget-tracking with programmatic decision gates |
| `d_routing_agent` | Router + All Agents | **Hero agent** — orchestrates all sub-agents based on user intent |
| `e_agent_as_tool` | Agent-as-Tool | Uses LocationScout and LogisticsValidator as callable tools |
| `f_agent_with_memory` | Memory Agent | Saves and recalls user preferences across sessions |
| `g_agents_mcp` | MCP Toolbox | Queries SQLite database via MCP Toolbox server |

## Deactivating the Environment

```bash
deactivate
```

## License

Built with ❤️ using Google Agent Development Kit (ADK)