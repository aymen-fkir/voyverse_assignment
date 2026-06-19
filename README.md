# Voyverse Assignment

A Python project that combines a local LLM (via **Ollama**) with a **Neo4j** graph database to build and query a knowledge graph — entirely offline, with no external API dependencies.

---

## Overview

This project demonstrates an end-to-end pipeline for:

- **Ingesting and processing data** using Pandas
- **Extracting entities and relationships** using a locally running LLM through Ollama
- **Persisting structured knowledge** into a Neo4j graph database
- **Querying the graph** to surface connections and insights

The codebase is organized under `src/voyverse/` and includes Jupyter Notebooks for exploration alongside the production Python source.

---

## Tech Stack

| Component       | Technology                          |
|-----------------|-------------------------------------|
| Language        | Python ≥ 3.12                       |
| LLM Runtime     | [Ollama](https://ollama.com/) (local models) |
| Graph Database  | [Neo4j](https://neo4j.com/) (Bolt protocol) |
| Data Processing | Pandas                              |
| Config/Validation | Pydantic + pydantic-settings      |
| Package Manager | [uv](https://github.com/astral-sh/uv) |

---

## Project Structure

```
voyverse_assignment/
├── src/
│   └── voyverse/          # Main Python source package
├── logs/                  # Application logs
├── .env                   # Environment variables (Neo4j credentials)
├── .python-version        # Pinned Python version
├── pyproject.toml         # Project metadata and dependencies
└── uv.lock                # Locked dependency versions
```

---

## Prerequisites

- **Python 3.12+**
- **[uv](https://github.com/astral-sh/uv)** — fast Python package manager
- **[Ollama](https://ollama.com/)** — local LLM runtime (must be running)
- **[Neo4j](https://neo4j.com/download/)** — graph database (local instance)

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/aymen-fkir/voyverse_assignment.git
cd voyverse_assignment
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure environment variables

The `.env` file at the root holds Neo4j connection settings. Update it to match your local instance:

```env
neo4j_user=neo4j
neo4j_password=your_password
neo4j_uri=bolt://127.0.0.1:7687
```

### 4. Start Neo4j

Make sure your Neo4j database is running and accessible at the URI specified in `.env`. You can use [Neo4j Desktop](https://neo4j.com/download/) or Docker:

```bash
docker run \
  --publish=7474:7474 --publish=7687:7687 \
  --env NEO4J_AUTH=neo4j/your_password \
  neo4j:latest
```

### 5. Start Ollama and pull a model

```bash
ollama serve
ollama pull llama3   # or any model of your choice
```

---

## Running the Project

```bash
uv run python -m voyverse
```

Or open the Jupyter notebooks for interactive exploration:

```bash
uv run jupyter notebook
```

---

## Dependencies

| Package             | Version   | Purpose                          |
|---------------------|-----------|----------------------------------|
| `neo4j`             | ≥ 6.2.0   | Neo4j Python driver              |
| `ollama`            | ≥ 0.6.2   | Local LLM client                 |
| `pandas`            | ≥ 3.0.3   | Data manipulation                |
| `pydantic`          | ≥ 2.13.4  | Data validation and modeling     |
| `pydantic-settings` | ≥ 2.14.1  | Settings management from `.env`  |

---

## Notes

- All LLM inference runs **locally** via Ollama — no OpenAI or cloud API key required.
- Neo4j is accessed over the **Bolt** protocol at `bolt://127.0.0.1:7687` by default.
- Logs are written to the `logs/` directory.

---

## Author

[aymen-fkir](https://github.com/aymen-fkir)