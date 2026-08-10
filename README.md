# SupportCopilot

AI-powered customer support agent for NovaCart.

SupportCopilot combines RAG, hybrid retrieval, LangGraph-based
agent orchestration, and database-backed support tools to answer
customer questions and perform support actions.

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

---

## Architecture

```text
                         User Question
                              |
                              v
                       +--------------+
                       |    Router    |
                       +--------------+
                              |
              +---------------+---------------+
              |               |               |
              v               v               v
             RAG          Order Tools      Fallback
              |               |
              v               v
       Hybrid Retrieval   SQLite Database
              |               |
              v               v
         Policy Docs      Order / Ticket
              |
              v
        Final Response
````

---

## Agent Workflow

The LangGraph agent classifies incoming requests into different
support intents.

### Supported intents

* `rag`
* `order_status`
* `refund`
* `ticket`
* `fallback`

### Tool routing

| Intent         | Tool                       |
| -------------- | -------------------------- |
| `order_status` | `get_order_status`         |
| `refund`       | `check_refund_eligibility` |
| `ticket`       | `create_ticket`            |

---

## RAG Pipeline

The RAG system retrieves relevant NovaCart policy information before
generating an answer.

The retrieval pipeline uses:

* Semantic search
* BM25 / keyword search
* Hybrid retrieval
* Top-k relevant chunks
* LLM-based answer generation

The model is instructed to answer using only the retrieved
NovaCart policy information.

If the information is unavailable, the assistant explicitly states
that it does not have enough information instead of inventing an answer.

---

## Order Support Tools

SupportCopilot connects to a SQLite database containing NovaCart
order information.

### Order Status

Users can ask questions such as:

```text
Where is my order ORD1005?
```

The system retrieves:

* Customer
* Product
* Order date
* Delivery date
* Order status
* Payment status
* Amount

### Refund Eligibility

The system checks:

* Whether the order exists
* Whether the order has been delivered
* Whether it is within the 30-day return window

### Support Tickets

Customers can report issues such as damaged packages.

The system creates a support ticket containing:

* Ticket ID
* Order ID
* Issue
* Status
* Creation timestamp

---

## Example

### Policy Question

```text
User:
How long does delivery take?
```

```text
SupportCopilot:
Metro Cities: 2–4 business days
Tier-2 Cities: 3–5 business days
Remote Areas: 5–7 business days
```

---

### Order Question

```text
User:
Where is my order ORD1005?
```

```text
SupportCopilot:
Your order ORD1005 has been shipped.
```

---

### Refund Question

```text
User:
Can I get a refund for ORD1005?
```

```text
SupportCopilot:
The order is not currently eligible for a refund because it
has not been delivered yet.
```

---

### Support Ticket

```text
User:
My package ORD1005 arrived damaged, create a complaint.
```

```text
SupportCopilot:
A support ticket has been created.
```

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

Checks whether generated responses contain the expected information
without requiring exact wording.

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

```text
SupportCopilot/
│
├── data/
│   ├── database/
│   │   └── orders.db
│   ├── documents/
│   ├── chroma/
│   └── bm25/
│
├── evaluation/
│   ├── test_cases.json
│   ├── hallucination_tests.json
│   ├── edge_case_tests.json
│   ├── evaluate_agent.py
│   ├── evaluate_hallucination.py
│   ├── evaluate_edge_cases.py
│   └── evaluation_report.md
│
├── src/
│   ├── agents/
│   │   └── graph.py
│   │
│   ├── rag/
│   │   ├── rag_pipeline.py
│   │   └── hybrid_retriever.py
│   │
│   └── tools/
│       └── order_tools.py
│
├── .gitignore
├── README.md
└── requirements.txt
```

---

## Running the Project

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file containing:

```text
GROQ_API_KEY=your_api_key
```

Run the agent:

```bash
python -m src.agents.graph
```

---

## Running Evaluations

### Main evaluation

```bash
python -m evaluation.evaluate_agent
```

### Hallucination evaluation

```bash
python -m evaluation.evaluate_hallucination
```

### Edge-case evaluation

```bash
python -m evaluation.evaluate_edge_cases
```

---

## Technologies

* Python
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

---

## Future Improvements

Potential future improvements include:

* LLM-based intent classification
* More sophisticated tool selection
* Conversation memory
* Streaming responses
* Better evaluation metrics
* Larger evaluation datasets
* Authentication
* Customer-facing web interface
* Observability and tracing

````


