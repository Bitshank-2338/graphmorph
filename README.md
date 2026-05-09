# GraphMorph

GraphMorph is an agentic graph intelligence workspace. You upload a CSV, it becomes a live in-memory graph, and the interface morphs based on the intent of the question instead of staying fixed as a static dashboard.

## What it does

- Uploads datasets such as `employees.csv`
- Converts rows into a graph of people, teams, skills, and relationships
- Adapts the UI to the user question
- Supports graph exploration, risk analysis, skill coverage, clustering, and custom generated views

## Core pitch

GraphMorph does not just change the answer. It changes the interface.

## Demo flow

1. Open `http://localhost:5173`
2. Upload `employees.csv`
3. Show the graph explorer view
4. Ask: `Who are the bottlenecks?` and show the risk matrix
5. Ask: `What skills are missing across the org?` and show the skill grid
6. Ask: `Cluster the org by department` and show the cluster view
7. End with the message that GraphMorph is a graph-native agent where the UI is generated from intent and topology

## Runtime

- Frontend: `localhost:5173`
- Backend: `localhost:8001`
- Neo4j is not required for the demo because the uploaded CSV runs as a live in-memory graph