# SupportCopilot

AI-powered customer support agent for NovaCart.

SupportCopilot combines RAG, hybrid retrieval, LangGraph-based
agent orchestration, database-backed support tools, and a FastAPI
backend to answer customer questions and perform support actions.

---

## Features

- Policy-based question answering using RAG
- Semantic + keyword/hybrid retrieval
- LangGraph agent workflow
- Intent-based request routing
- Order status lookup
- Refund eligibility checking
- Support ticket creation
- Unknown-information handling
- Hallucination prevention
- Edge-case handling
- Automated evaluation framework
- FastAPI REST API
- Swagger/OpenAPI documentation
- CORS support
- Request validation and error handling

---

## Architecture

                         User / Frontend
                               |
                               v
                         FastAPI API
                               |
                           POST /chat
                               |
                               v
                        LangGraph Agent
                               |
              +----------------+----------------+
              |                |                |
              v                v                v
             RAG          Order Tools        Fallback
              |                |
              v                v
       Hybrid Retrieval    SQLite Database
              |                |
              v                v
        Policy Documents   Orders / Tickets
              |
              v
        Final Response
              |
              v
          FastAPI API
              |
              v
        User / Frontend

---

## Agent Workflow

The LangGraph agent classifies incoming requests into different
support intents.

### Supported intents

- `rag`
- `order_status`
- `refund`
- `ticket`
- `fallback`

### Tool routing

| Intent | Tool |
|---|---|
| `order_status` | `get_order_status` |
| `refund` | `check_refund_eligibility` |
| `ticket` | `create_ticket` |

---

## RAG Pipeline

The RAG system retrieves relevant NovaCart policy information before
generating an answer.

The retrieval pipeline uses:

- Semantic search
- BM25 / keyword search
- Hybrid retrieval
- Top-k relevant chunks
- LLM-based answer generation

The model is instructed to answer using only the retrieved
NovaCart policy information.

If the information is unavailable, the assistant explicitly states
that it does not have enough information instead of inventing an answer.

---

## Order Support Tools

SupportCopilot connects to a SQLite database containing NovaCart
order information.

### Order Status

Example:

    Where is my order ORD1005?

The system retrieves the relevant order information and returns
the current order status.

### Refund Eligibility

The system checks:

- Whether the order exists
- Whether the order has been delivered
- Whether it is within the applicable return window

### Support Tickets

Customers can report issues such as damaged packages.

The system creates a support ticket containing the relevant
order and issue information.

---

## FastAPI Backend

SupportCopilot exposes the agent through a REST API using FastAPI.

### API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health check |
| POST | `/chat` | Send a customer support question |

### Request

```json
{
  "question": "Where is my order ORD1005?"
}
````

### Response

```json
{
  "success": true,
  "question": "Where is my order ORD1005?",
  "intent": "order_status",
  "response": "Your order ORD1005 has been shipped..."
}
```

### Validation

The API validates incoming requests using Pydantic.

An empty question is rejected with HTTP `422`.

Whitespace-only questions are handled by the agent as a fallback
request.

### Error Handling

Unexpected agent errors are caught by the API and returned as an
HTTP `500` response without exposing internal implementation details.

### CORS

CORS middleware is enabled so that a separate frontend application
can communicate with the backend API.

---

## Swagger / OpenAPI

FastAPI automatically provides interactive API documentation.

After starting the server, open:

```
http://127.0.0.1:8000/docs
```

The OpenAPI specification is available at:

```
http://127.0.0.1:8000/openapi.json
```

The API exposes schemas for:

* `ChatRequest`
* `ChatResponse`
* Validation errors

---

## Example Requests

### Policy Question

```
How long does delivery take?
```

The agent retrieves the relevant shipping policy and returns the
estimated delivery timelines.

---

### Order Question

```
Where is my order ORD1005?
```

The request is routed to the order status tool.

---

### Refund Question

```
Can I get a refund for ORD1005?
```

The request is routed to the refund eligibility tool.

---

### Support Ticket

```
My package ORD1005 arrived damaged, create a complaint.
```

The request is routed to the ticket creation tool.

---

### Unknown Order

```
Where is my order ORD9999?
```

The system checks the database and reports that the order could not
be found.

---

## Evaluation

SupportCopilot includes an automated evaluation framework covering
multiple aspects of agent performance.

### Evaluation Results

| Metric               | Result |
| -------------------- | -----: |
| Intent Routing       |   100% |
| Tool Selection       |   100% |
| RAG Retrieval        |   100% |
| Answer Quality       |  87.5% |
| Hallucination Safety |   100% |
| Edge-Case Handling   |    90% |
| Overall Evaluation   |  87.5% |

### Evaluation Categories

#### Intent Routing

Tests whether questions are correctly classified into:

* RAG
* Order status
* Refund
* Ticket
* Fallback

#### Tool Selection

Tests whether the correct backend tool is selected for each
action-oriented request.

#### RAG Retrieval

Tests whether the relevant policy document is retrieved for
policy-based questions.

#### Answer Quality

Checks whether generated responses contain the expected information.

#### Hallucination Safety

Tests questions for which the knowledge base does not contain an
answer.

The assistant is expected to acknowledge insufficient information
rather than fabricate an answer.

#### Edge Cases

Tests include:

* Empty questions
* Whitespace-only input
* Missing order IDs
* Invalid order IDs
* Unknown orders
* Unknown refund requests
* Unknown ticket requests
* Random input

---

## Project Structure

```
SupportCopilot/
|
+-- data/
|   +-- database/
|   |   +-- orders.db
|   +-- documents/
|   +-- chroma/
|   +-- bm25/
|
+-- evaluation/
|   +-- test_cases.json
|   +-- hallucination_tests.json
|   +-- edge_case_tests.json
|   +-- evaluate_agent.py
|   +-- evaluate_hallucination.py
|   +-- evaluate_edge_cases.py
|   +-- evaluation_report.md
|
+-- src/
|   +-- agents/
|   |   +-- graph.py
|   |
|   +-- rag/
|   |   +-- rag_pipeline.py
|   |   +-- hybrid_retriever.py
|   |
|   +-- tools/
|   |   +-- order_tools.py
|   |
|   +-- api/
|       +-- __init__.py
|       +-- main.py
|
+-- .gitignore
+-- .env
+-- requirements.txt
+-- README.md
```

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file containing the required API key:

```text
GROQ_API_KEY=your_api_key
```

The `.env` file is excluded from Git using `.gitignore`.

---

## Running the Agent Directly

```powershell
python -m src.agents.graph
```

---

## Running the FastAPI Backend

Start the development server:

```powershell
python -m uvicorn src.api.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

## Running Evaluations

### Main evaluation

```powershell
python -m evaluation.evaluate_agent
```

### Hallucination evaluation

```powershell
python -m evaluation.evaluate_hallucination
```

### Edge-case evaluation

```powershell
python -m evaluation.evaluate_edge_cases
```

---

## Technologies

* Python
* FastAPI
* Uvicorn
* Pydantic
* LangGraph
* LangChain
* Groq / Llama
* RAG
* BM25
* Vector Search
* SQLite
* ChromaDB
* Sentence Transformers

---

## Key Learning Outcomes

This project demonstrates practical implementation of:

* Retrieval-Augmented Generation
* Hybrid information retrieval
* Agentic workflows
* Intent routing
* Tool calling
* Database integration
* LLM response generation
* Hallucination prevention
* Automated agent evaluation
* Edge-case testing
* REST API development
* FastAPI request validation
* API documentation with OpenAPI
* CORS configuration
* Backend integration with an AI agent

---

## Future Improvements

Potential future improvements include:

* Frontend interface
* Conversation memory
* Streaming responses
* Authentication
* Better evaluation metrics
* Larger evaluation datasets
* Improved tool selection
* Production deployment
* Observability and tracing

