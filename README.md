# Career Conversations AI

[![Python](https://img.shields.io/badge/python-3.12+-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-📡-turquoise)](https://fastapi.tiangolo.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-LLM-purple)](https://openai.com/)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-red)](https://qdrant.tech/)
[![Redis](https://img.shields.io/badge/Redis-Memory-red)](https://redis.io/)
[![Upstash](https://img.shields.io/badge/Upstash-Redis-orange)](https://upstash.com/)
[![Gradio](https://img.shields.io/badge/Gradio-UI-yellow)](https://gradio.app/)

**Career Conversations AI** is a conversational assistant that answers questions about a person’s professional background using **Retrieval-Augmented Generation (RAG)**.

It ingests knowledge sources (resumes, profiles, summaries), stores them as vector embeddings, and uses those documents to ground answers with accurate, personalized context.

### What it does

- **Answers resume-style questions** (skills, experience, industries, tools, etc.)
- **Uses retrieval** (vector search) to ground answers in your own documents
- **Stores chat history in Redis** to preserve conversation context
- **Notifies you via Pushover** when a question can’t be answered or a user wants to contact you

---

## 🧠 Core Features

#### Retrieval Augmented Generation (RAG)

Documents are embedded and stored in a vector database (Qdrant). When a user asks a question, relevant text chunks are retrieved and used as LLM context.

#### Persistent Conversation Memory

Chat history is stored in Redis so the agent can remember earlier turns in the same session.

#### Tooling (Pushover)

When the agent can’t answer a question or a user asks to contact you, it can trigger a **Pushover notification** so you don’t miss important messages.

#### Web UI + API

- **Gradio chat interface** for interactive use
- **FastAPI backend** powering chat and agent endpoints

---

## 🛠️ Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **AI/LLM:** OpenAI API, Retrieval-Augmented Generation (RAG)
- **Vector Database:** Qdrant
- **Memory:** Upstash Redis
- **UI:** Gradio
- **Tooling:** Pushover API
- **Package Manager:** uv

---

## 🚀 Getting Started

#### 1) Clone

```bash
git clone https://github.com/waseemansar/career-conversations-ai.git
cd career-conversations-ai
```

#### 2) Install (uv)

```bash
uv sync
```

#### 3) Configure environment

Create a `.env` file next to `pyproject.toml` in the root directory based on the `.env.example` file, and set up your environment variables:

```bash
cp .env.example .env
```

#### 4) Add knowledge documents

Place any `.pdf` or `.txt` files into the `data/knowledge/` directory. The system will automatically load all files with these extensions for embedding and retrieval.

Examples:

- `linkedin.pdf` (your LinkedIn profile or resume)
- `summary.txt` (a text summary of your professional background)
- `resume.pdf` (additional resume files)
- `projects.txt` (project descriptions)

All documents will be processed and made available for the AI to answer questions about your professional background.

#### 5) Index knowledge into vector database

```bash
uv run python -m app.cli.index
```

This loads your documents, chunks them, embeds them, and stores in Qdrant.

#### 6) Add your profile picture (optional)

Place your profile picture in `app/ui/assets/` and set the path in `.env`:

```bash
AVATAR_PATH=app/ui/assets/profile.jpeg
```

#### 7) Run the app

```bash
uv run python -m app.main
```

Visit:

- **Web UI**: `http://localhost:8000`
- **API docs**: `http://localhost:8000/docs`

---

## 🏗️ Architecture

```
User
  │
  ▼
Gradio UI
  │
  ▼
FastAPI API
  │
  ▼
AI Agent
  ├── RAG Service (Qdrant)
  ├── Redis Memory (History)
  └── Tools (Pushover)
```

---

## 🧩 Project Structure

```
career-conversations-ai/
├── app/
│   ├── agents/                   # AI agent logic
│   ├── api/                      # FastAPI routes
│   ├── cli/                      # Command-line scripts
│   ├── config/                   # Settings and configuration
│   ├── core/                     # Core utilities and handlers
│   ├── infrastructure/           # Infrastructure clients
│   ├── knowledge/                # Knowledge loader script
│   ├── schemas/                  # Pydantic schemas
│   ├── services/                 # Core services (RAG, storage, etc.)
│   ├── tools/                    # Tool integrations (Pushover)
│   ├── ui/                       # Gradio UI
│   ├── dependencies.py           # Dependency injection setup
│   └── main.py                   # FastAPI app entrypoint
├── data/
│   └── knowledge/                # Documents for embedding
├── .env.example                  # Example environment file
├── .gitignore                    # Git ignore rules
├── pyproject.toml                # Project dependencies and config
├── README.md                      # Project documentation
└── uv.lock                       # Dependency lock file
```

---

## ✅ Requirements

- Python **3.12+**
- **uv** package manager
- OpenAI API key
- Qdrant instance
- Redis instance
- Pushover account
