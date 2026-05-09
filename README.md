# GraphMorph

GraphMorph is an agentic graph intelligence workspace where the interface changes at runtime based on the user's intent and the structure of the uploaded graph.

The core idea is simple:

```txt
GraphMorph does not just change the answer. It changes the interface.
```

Instead of giving every user a static dashboard, GraphMorph turns a dataset into a graph and then chooses the right interface for the question being asked. A bottleneck question becomes a risk matrix. A skills question becomes a coverage grid. A relationship question becomes a graph explorer. The same uploaded data can produce different UI modes from the same conversation.

## Why This Exists

Most analytics products separate three things:

- The dataset
- The analysis
- The interface

GraphMorph combines them into one runtime flow. The user uploads data, asks a natural-language question, and the system decides what interface best represents the answer.

This is useful for messy organizational, operational, and relationship-heavy datasets where a table or a single dashboard is not enough. The project is especially designed for hackathon demos because the visual change from one interface type to another is immediate and easy to understand.

## What It Does

- Uploads CSV or spreadsheet data.
- Converts rows into graph entities and relationships.
- Supports employee, department, skill, collaboration, customer, product, category, and region-style datasets.
- Renders the uploaded graph in a relationship explorer.
- Lets the user ask natural-language questions.
- Classifies the question into a UI type.
- Generates a matching UI schema.
- Renders the result through a dynamic frontend renderer.

## Example Questions

```txt
Who are the bottlenecks?
What skills are missing across the org?
Cluster the org by department
Show relationships across the organization
What happens if a critical person leaves?
Build me a custom dashboard for Engineering risk
```

## Runtime UI Modes

GraphMorph currently supports these interface types:

- `relationship_explorer`: A graph view for nodes and edges.
- `risk_matrix`: A bottleneck and dependency risk view.
- `skill_gap_grid`: A skill coverage view.
- `cluster_explorer`: A grouped view by department, team, or segment.
- `simulation_workspace`: A what-if impact view.
- `generative`: A constrained generated UI tree for custom layouts.

## Architecture

GraphMorph has three main layers:

- Frontend: React, Vite, TailwindCSS, ReactFlow, Framer Motion, Axios.
- Backend: FastAPI, pandas, Neo4j driver, OpenAI API, Pydantic.
- Graph runtime: Neo4j when available, with an in-memory live graph fallback for the demo.

The backend pipeline is:

```txt
CSV upload
  -> parse file
  -> transform rows into nodes and edges
  -> store graph
  -> return initial relationship explorer UI

User query
  -> classify intent
  -> generate Cypher-style query type
  -> execute against graph runtime
  -> shape result into UI schema
  -> frontend renders matching UI
```

## Important Demo Behavior

Neo4j is optional for the current local demo.

If Neo4j Aura is unavailable, GraphMorph stores the uploaded CSV as a live in-memory graph. That means the demo still works with real uploaded data instead of stale mock rows.

Current local runtime:

- Frontend: `http://localhost:5173`
- Backend: `http://localhost:8001`
- Backend health: `http://localhost:8001/health`

The health endpoint may show:

```json
{"ok": true, "neo4j": false}
```

That is acceptable for the demo. It means the app is using the in-memory graph fallback.

## Setup

Install backend dependencies:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Install frontend dependencies:

```powershell
cd frontend
npm install
```

Create a root `.env` file:

```env
NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your_password_here
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
APP_HOST=0.0.0.0
APP_PORT=8001
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000
```

For the demo, OpenAI is used for intent classification and generated UI behavior. If the LLM is unavailable, the app falls back to a keyword classifier.

## Running Locally

Start the backend:

```powershell
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8001
```

Use this from the project root instead if PowerShell has trouble with the relative path:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8001 --app-dir backend
```

Start the frontend:

```powershell
cd frontend
npm run dev -- --host 127.0.0.1
```

Open:

```txt
http://localhost:5173
```

## Demo Script

Use this short explanation while recording:

```txt
GraphMorph is an agentic graph intelligence workspace. I upload a CSV, and it turns the rows into a graph of people, departments, skills, and relationships. Then I can ask natural-language questions. The key idea is that the UI itself changes based on the question. A bottleneck question becomes a risk matrix, a skills question becomes a coverage grid, and a relationship question becomes a graph explorer.
```

Recommended demo flow:

1. Open `http://localhost:5173`.
2. Upload `data/employees.csv`.
3. Show the initial relationship graph.
4. Ask `Who are the bottlenecks?`.
5. Show the risk matrix.
6. Ask `What skills are missing across the org?`.
7. Show the skill grid.
8. Ask `Cluster the org by department`.
9. Show the cluster view.
10. End with: "GraphMorph is a graph-native agent where the UI is generated from intent and topology, not hardcoded as one static dashboard."

## Project Structure

```txt
backend/
  app/
    main.py
    routes/
    services/
    schemas/
    utils/

frontend/
  src/
    components/
    pages/
    renderer/
    services/

data/
  employees.csv
```

## Current Limitations

- Neo4j Aura connectivity may fail locally depending on credentials or network access.
- The local demo handles that by using an in-memory graph runtime.
- Intent classification uses OpenAI when available and a deterministic fallback otherwise.
- The generated UI mode is constrained to known primitives so the frontend can safely render it.

## One-Line Pitch

GraphMorph is a graph-native AI workspace that turns uploaded data into a live graph and morphs the interface based on what the user asks.
