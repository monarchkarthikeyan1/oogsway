# The Lenny Growth Assistant

> **A full-stack, AI-powered conversational web application for Product Managers and Growth Leaders—grounded strictly in transcripts from Lenny's Podcast.**

---

## 🌟 Key Features

- 🎯 **Grounded Conversational Intelligence**: Answers product management and growth questions using hybrid RAG vector search over Lenny's Podcast transcripts with clickable source citations (`[1]`, `[2]`).
- ⚡ **Ship 30 for 30 Content Skill**: Built-in skill generating publication-ready ~1,250 word essays with strong hooks, bold lead-ins, narrative progression, and actionable frameworks.
- 🎨 **Native In-App Artifact Viewer**: Claude-style side-by-side split pane rendering interactive HTML/CSS components and Markdown documents within an isolated, sandboxed `<iframe>`.
- 🔀 **Flexible Multi-LLM Configuration**: Seamless dynamic switching between **Local Ollama** (zero cloud API keys required) and Cloud LLMs (**Anthropic Claude**, **OpenAI GPT-4o**).
- 🛡️ **Security First**: Bleach HTML sanitization, Content Security Policy (CSP) headers, and strict `iframe` sandboxing to isolate untrusted generated HTML.

---

## 🚀 Quickstart: One-Command Docker Setup (Recommended)

Run the entire full-stack application (PostgreSQL + pgvector, Ollama, FastAPI Backend, Vite Frontend) using Docker Compose:

```bash
# 1. Clone the repository
git clone https://github.com/your-username/lenny-growth-assistant.git
cd lenny-growth-assistant

# 2. Launch using Docker Compose
docker-compose up --build
```

Access the application in your browser:
- **Frontend App**: [http://localhost:5173](http://localhost:5173)
- **FastAPI API Docs**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- **System Health Diagnostic**: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## 💻 Manual Local Development Setup

If you prefer to run the backend and frontend locally without Docker:

### Prerequisites
- **Python**: 3.11 or higher
- **Node.js**: v18 or v20
- **Ollama**: (Optional for local LLM demo) Installed from [ollama.ai](https://ollama.ai)

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp ../.env.example .env

# Run seed transcript ingestion pipeline
python data/ingest.py

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install npm dependencies
npm install

# Start Vite dev server
npm run dev
```

The app will be live at [http://localhost:5173](http://localhost:5173).

---

## 🤖 Local LLM Setup (Ollama Demo Target)

To run the mandatory local LLM demo using Ollama:

1. Install Ollama and start the server:
   ```bash
   ollama serve
   ```
2. Pull the default recommended model:
   ```bash
   ollama pull llama3.2
   ```
3. Open the app header LLM selector or click the Settings icon in the UI to confirm Ollama status is **Ready**.

---

## ☁️ Cloud LLM Setup (Anthropic & OpenAI)

To enable Anthropic Claude or OpenAI GPT-4o:

1. Add your API keys to `.env` or set environment variables:
   ```env
   ANTHROPIC_API_KEY=sk-ant-api03-...
   OPENAI_API_KEY=sk-proj-...
   ```
2. Open the **Model Provider Selector** in the UI top navigation bar and select **Anthropic Claude** or **OpenAI GPT-4o**.

---

## 🧪 Automated Testing

The backend includes comprehensive `pytest` test suites covering API endpoints, RAG search, LLM provider fallback, Ship 30 essay generation, and security sanitization:

```bash
cd backend
pytest -v
```

---

## 📽️ Demo Video Script & Evaluator Handoff

A 2-3 minute demo walk-through covers:
1. **The Problem & Framing**: Why PMs need grounded, citation-backed AI without prompt engineering.
2. **Product Walkthrough**: Querying Shreyas Doshi's LNO framework and inspecting citation source quotes.
3. **Ship 30 Skill**: Generating a ~1,250 word publication-ready essay.
4. **Interactive Artifact Viewer**: Rendering HTML Product Canvas inside the sandboxed viewer.
5. **Local Ollama Demo & Technical Trade-offs**: Switching model providers live.

---

## 📂 Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/            # REST API endpoints (chat, sessions, artifacts, providers, health)
│   │   ├── core/           # LLM factory, RAG engine, Ship 30 skill, Artifact generator
│   │   ├── models/         # Database ORM models and Pydantic DTOs
│   │   ├── utils/          # Security sanitization & structured logging
│   │   ├── config.py       # Configuration & env management
│   │   └── database.py     # Database engine & fallback setup
│   ├── data/
│   │   ├── raw_transcripts/ # Bundled Lenny's Podcast transcripts
│   │   └── ingest.py       # Automated ingestion pipeline CLI
│   └── tests/              # Pytest test suite
├── frontend/
│   ├── src/
│   │   ├── components/     # Header, Sidebar, ChatWindow, ChatInput, ArtifactViewer, CitationDrawer
│   │   ├── services/       # Axios API client
│   │   └── store/          # Zustand state store
├── agent_transcripts/       # Development logs of coding agent iterations
├── docker-compose.yml       # One-command orchestration
├── PRD.md                   # Product Requirements & Forward Deployment Brief
├── architecture.md          # Technical Architecture & Security Specification
├── design.md                # UI/UX & Information Architecture Specification
└── README.md                # Evaluator Setup & Handoff Guide
```
