# Setup & Run

## Prerequisites

* Python 3.12+
* Node.js 18+
* UV Package Manager
* Docker Desktop
* MongoDB
* OpenRouter API Key

---

## Clone Repository

```bash
git clone https://github.com/kamalesh2602/AI-workbench
cd AI-workbench
```

---

## Backend Setup

Navigate to the server folder:

```bash
cd server
```

Copy environment variables:

```bash
cp .env.example .env
```

Fill in the required values:

```env
MONGO_URI=
OPENROUTER_API_KEY=
QDRANT_URL=
```

Install dependencies:

```bash
uv sync
```

Start the backend:

```bash
uv run uvicorn main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

## Qdrant Setup

Start Qdrant using Docker:

```bash
docker run -d ^
--name qdrant ^
-p 6333:6333 ^
qdrant/qdrant
```

Qdrant Dashboard:

```text
http://localhost:6333/dashboard
```

---

## Frontend Setup

Navigate to client:

```bash
cd client
```

Copy environment variables:

```bash
cp .env.example .env
```

Install dependencies:

```bash
npm install
```

Start development server:

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## Application Flow

1. Create Workspace
2. Upload PDF
3. Document is automatically:

   * Processed
   * Chunked
   * Embedded
   * Stored in Qdrant
4. Ask questions about uploaded documents
5. View chat history and sources

---

## Tech Stack

### Frontend

* React
* Axios
* React Router

### Backend

* FastAPI
* MongoDB
* Qdrant
* Sentence Transformers
* OpenRouter

### AI Components

* PDF Extraction
* Text Chunking
* Embedding Generation
* Semantic Search
* Retrieval-Augmented Generation (RAG)
