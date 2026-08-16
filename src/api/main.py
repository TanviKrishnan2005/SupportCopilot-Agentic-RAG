from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from src.agents.graph import graph


# --------------------------------------------------
# Request Model
# --------------------------------------------------

class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="Customer support question"
    )


# --------------------------------------------------
# Response Model
# --------------------------------------------------

class ChatResponse(BaseModel):
    success: bool
    question: str
    intent: str
    response: str


# --------------------------------------------------
# Create FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="SupportCopilot API",
    description="Backend API for the NovaCart AI customer support agent.",
    version="1.0.0"
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://support-copilot-agentic-rag.vercel.app",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Health Check
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "SupportCopilot API is running"
    }


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    question = request.question.strip()

    if not question:
        return ChatResponse(
            success=False,
            question="",
            intent="fallback",
            response="Please enter a question so I can help you."
        )

    try:

        result = graph.invoke({
            "message": question,
            "response": "",
            "intent": "",
            "tool_result": {},
            "tool_used": "",
            "context": []
        })

        return ChatResponse(
            success=True,
            question=question,
            intent=result["intent"],
            response=result["response"]
        )

    except Exception as error:

        print(f"Agent error: {error}")

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing your request."
        )