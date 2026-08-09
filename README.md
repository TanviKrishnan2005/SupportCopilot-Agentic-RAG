# SupportCopilot

SupportCopilot is an AI-powered customer support assistant for NovaCart.

It can answer questions from company policies, check order details, check refund eligibility, and create support tickets.

## What it can do

- Answer customer questions using NovaCart policies
- Search documents using hybrid retrieval
- Check order status
- Check refund eligibility
- Create support tickets
- Route questions to the correct tool
- Handle missing or invalid order IDs
- Give natural language responses using an LLM
- Avoid making up information when the answer is not in the knowledge base

## How it works

The project uses a simple agent workflow:

Customer Question  
↓  
Router  
↓  
RAG / Order Tool / Refund Tool / Ticket Tool  
↓  
LLM Response  
↓  
Customer

For policy-related questions, the system uses hybrid search with semantic search and BM25.

For order-related questions, it uses a SQLite database.

LangGraph is used to manage the agent workflow.

## Tech Stack

- Python
- LangGraph
- LangChain
- Groq
- Llama 3.3 70B
- Sentence Transformers
- ChromaDB
- BM25
- SQLite
- Python-dotenv

## Project Structure

```text
SupportCopilot/
│
├── data/
│   ├── database/
│   └── policies/
│
├── evaluation/
│
├── src/
│   ├── agents/
│   ├── database/
│   ├── ingestion/
│   ├── rag/
│   ├── tools/
│   └── utils/
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
````

## Example Questions

### Policy questions

```text
How long does delivery take?
Can I return a damaged product after 20 days?
What payment methods are accepted?
```

### Order questions

```text
Where is my order ORD1005?
Can I get a refund for ORD1005?
```

### Support questions

```text
My package ORD1005 arrived damaged, create a complaint
```

## Running the Project

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add:

```text
GROQ_API_KEY=your_api_key
```

Run the agent:

```bash
python -m src.agents.graph
```

Then enter a customer question.

## Example

```text
Ask NovaCart a question: Where is my order ORD1005?

Intent: order_status

Response:
Your order ORD1005 has been shipped. However, we don't have a confirmed delivery date yet.
```

## Current Status

The core agent is working with:

* Hybrid RAG
* Order lookup
* Refund checking
* Support ticket creation
* Intent routing
* Natural language responses
* Error and fallback handling


```
```
