# SupportCopilot 🤖

AI-powered customer support agent for **NovaCart** that can answer policy questions, retrieve order information, check refund eligibility, and create support tickets.

Built with **LangGraph, Hybrid RAG, FastAPI, SQLite, React, and LLM-based tool calling**.

## 🚀 Live Demo

**Frontend:** https://support-copilot-agentic-rag.vercel.app/

**Backend:** https://supportcopilot-agentic-rag.onrender.com/

**API Docs:** https://supportcopilot-agentic-rag.onrender.com/docs

---

## ✨ Features

- Agentic customer-support workflow using LangGraph
- Intent-based request routing
- Hybrid RAG using semantic search + BM25
- Policy question answering
- Order status lookup
- Refund eligibility checking
- Support ticket creation
- Hallucination-safe fallback handling
- Automated evaluation and edge-case testing
- FastAPI REST API
- React + Vite frontend
- Production deployment on Render + Vercel

---

## 🏗️ Architecture

```text
                    React Frontend
                       (Vercel)
                           |
                           v
                    FastAPI Backend
                       (Render)
                           |
                           v
                    LangGraph Agent
                           |
          +----------------+----------------+
          |                |                |
          v                v                v
         RAG          Order Tools       Fallback
          |                |
          v                v
    Hybrid Retrieval    SQLite DB
       /       \
      v         v
 Semantic      BM25
  Search      Search
      \         /
       \       /
        v     v
      Context
         |
         v
    LLM Response
````

---

## 🧠 Agent Workflow

The agent classifies each request into one of five intents:

| Intent         | Action                              |
| -------------- | ----------------------------------- |
| `rag`          | Retrieve relevant NovaCart policies |
| `order_status` | Query order database                |
| `refund`       | Check refund eligibility            |
| `ticket`       | Create support ticket               |
| `fallback`     | Safely handle unknown requests      |

### Hybrid RAG

The RAG pipeline combines:

* Semantic vector search using **FastEmbed**
* BM25 keyword search
* ChromaDB vector storage
* Top-k context retrieval
* LLM-based answer generation

The model is instructed to answer only from retrieved NovaCart information and avoid fabricating unsupported answers.

---

## 🛠️ Support Tools

### Order Status

```text
Where is my order ORD1005?
```

Retrieves order information from SQLite.

### Refund Eligibility

```text
Can I get a refund for ORD1005?
```

Checks order existence, delivery status, and refund eligibility.

### Support Tickets

```text
My package ORD1005 arrived damaged, create a complaint.
```

Creates a support ticket for the customer issue.

---

## 📊 Evaluation

| Metric                 |    Result |
| ---------------------- | --------: |
| Intent Routing         |      100% |
| Tool Selection         |      100% |
| RAG Retrieval          |      100% |
| Answer Quality         |     87.5% |
| Hallucination Safety   |      100% |
| Edge-Case Handling     |       90% |
| **Overall Evaluation** | **87.5%** |

Tests cover intent routing, tool selection, retrieval quality, hallucination safety, invalid orders, missing IDs, empty input, and other edge cases.

---

## 📁 Project Structure

```text
SupportCopilot/
│
├── data/
│   ├── database/
│   │   └── orders.db
│   └── policies/
│       ├── faq.md
│       ├── payments.md
│       ├── returns.md
│       ├── shipping.md
│       └── warranty.md
│
├── evaluation/
│   ├── test_cases.json
│   ├── hallucination_tests.json
│   ├── edge_case_tests.json
│   └── evaluation scripts
│
├── frontend/
│   └── src/
│       ├── components/
│       ├── utils/
│       ├── App.jsx
│       └── index.css
│
├── src/
│   ├── agents/
│   ├── ingestion/
│   ├── rag/
│   ├── tools/
│   └── api/
│
├── .gitignore
├── .python-version
├── requirements.txt
└── README.md
```

---

## ⚙️ Local Setup

### Backend

```bash
git clone https://github.com/TanviKrishnan2005/SupportCopilot-Agentic-RAG.git
cd SupportCopilot-Agentic-RAG

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

Create `.env`:

```text
GROQ_API_KEY=your_api_key
```

Build the RAG indexes:

```powershell
python src/ingestion/store_chroma.py
python src/ingestion/build_bm25.py
```

Start the API:

```powershell
python -m uvicorn src.api.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Set:

```text
VITE_API_URL=http://127.0.0.1:8000
```

---

## ☁️ Deployment

**Frontend:** Vercel

**Backend:** Render

The backend builds the ChromaDB and BM25 indexes during deployment and runs as a FastAPI service.

The production frontend communicates with the deployed API through `VITE_API_URL`.

---

## 🧰 Tech Stack

**AI / Agent:** Python, LangGraph, LangChain, Groq/Llama

**RAG:** FastEmbed, ONNX Runtime, ChromaDB, BM25

**Backend:** FastAPI, Uvicorn, Pydantic, SQLite

**Frontend:** React, Vite, JavaScript

**Deployment:** Render, Vercel, GitHub

---

## 🔗 Repository

[https://github.com/TanviKrishnan2005/SupportCopilot-Agentic-RAG](https://github.com/TanviKrishnan2005/SupportCopilot-Agentic-RAG)

