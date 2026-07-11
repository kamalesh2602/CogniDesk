# CogniDesk

**AI-Powered Workspace for Research and Document Intelligence**

CogniDesk is a multi-agent AI workspace that combines Retrieval-Augmented Generation (RAG), web research, conversational memory, and career-focused AI tools into a unified platform. Users can upload documents, build knowledge workspaces, ask questions grounded in their data, and enrich responses with live web information.

---

## Features

### Workspace Management

* Create and manage multiple workspaces
* Organize documents by workspace
* Recent workspace tracking
* Secure user authentication using JWT

### Document Intelligence

* PDF upload and processing
* Automatic text extraction
* Chunking and embedding generation
* Vector search using Qdrant
* Source-aware document question answering

### Multi-Agent Research System

* **Research Agent**
  * Retrieves relevant document context from Qdrant
  * Searches the web using Tavily when required
  * Collects supporting evidence and sources

* **Writer Agent**
  * Synthesizes research results
  * Generates unified, context-aware responses
  * Combines document knowledge with live web information

### Conversation Memory

* Maintains recent chat history
* Supports follow-up questions
* Enables context-aware conversations

### Career Tools

* Resume Analyzer
* Resume Rewriter
* Interview Preparation Assistant

### Citations

* Document source references
* Web source references
* Transparent answer generation

---

## Tech Stack

### Frontend

* React
* React Router
* Axios

### Backend

* FastAPI
* Python

### Databases

* MongoDB
* Qdrant Vector Database

### AI Services

* OpenRouter
* Tavily Search API

### Authentication

* JWT Authentication

### Infrastructure

* Docker Compose
* MongoDB Docker
* Qdrant Docker / Qdrant Cloud

---

## System Architecture

```text
User
 │
 ▼
Workspace
 │
 ▼
Research Agent
 ├── Qdrant Document Search
 ├── Tavily Web Search
 └── Conversation Memory
 │
 ▼
Writer Agent
 │
 ▼
Final Response
 │
 ▼
Sources & Citations
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/kamalesh2602/CogniDesk.git
cd CogniDesk
```

---

## Docker Setup (Recommended)

### Create Docker Environment Files

Copy the example files:

```bash
cp server/.env.docker.example server/.env.docker
cp client/.env.docker.example client/.env.docker
```

Fill in the required API keys inside:

```text
server/.env.docker
```

Then start the complete application:

```bash
docker compose up --build
```

The application will be available at:

| Service | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend | http://localhost:8000 |
| Qdrant Dashboard | http://localhost:6333/dashboard |
| MongoDB | localhost:27017 |

---

## Backend Setup

```bash
cd server

uv sync

or

python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / Mac
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Frontend Setup

```bash
cd client

npm install

npm run dev
```

---

## Environment Variables

### Local Development

Create the following files from the provided examples:

```text
server/.env
client/.env
```

using

```text
server/.env.example
client/.env.example
```

### Docker

Create the following files:

```text
server/.env.docker
client/.env.docker
```

using

```text
server/.env.docker.example
client/.env.docker.example
```

---

## Required Variables

```env
MONGO_URI=
SECRET_KEY=

OPENROUTER_API_KEY=
TAVILY_API_KEY=

QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION=document_chunks
```

---

## Qdrant Setup

### Option 1 — Local Qdrant (Docker)

Run Qdrant locally:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Dashboard:

```text
http://localhost:6333/dashboard
```

Configuration:

```python
client = QdrantClient(
    host="localhost",
    port=6333
)
```

---

### Option 2 — Qdrant Cloud

Create a free cluster from Qdrant Cloud.

Add the following variables:

```env
QDRANT_URL=
QDRANT_API_KEY=
```

Configuration:

```python
client = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
```

---

## Running the Application

### Docker

```bash
docker compose up --build
```

---

### Backend

```bash
uvicorn main:app --reload
```

### Frontend

```bash
npm run dev
```

---

## Project Highlights

* Multi-Agent Architecture
* Retrieval-Augmented Generation (RAG)
* Qdrant Vector Search
* Tavily Web Research Integration
* Conversation Memory
* JWT Authentication
* Resume Analysis Tools
* Source Citations
* Workspace-Based Knowledge Management
* Full Docker Compose Support

---

## Future Improvements

* Advanced Agent Orchestration
* Workspace Sharing
* Team Collaboration
* Agent Marketplace
* Cloud Deployment
* Enhanced UI/UX

---

Built using **React, FastAPI, MongoDB, Qdrant, OpenRouter, Tavily, and Docker.**