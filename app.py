
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from groq import Groq
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

load_dotenv()

app = FastAPI(title="Nexus AI")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=str(STATIC_DIR)),
    name="static"
)

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str

class ChatRequest(BaseModel):
    messages: list[Message]

@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/api/chat")
def chat(request: ChatRequest):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="Groq API key .env file mein nahi mili."
        )

    try:
        client = Groq(api_key=api_key)

        messages = [
            {
                "role": "system",
                "content": "You are Nexus AI, a helpful, intelligent assistant. Reply in the user's language."
            }
        ]

        messages.extend([
            message.model_dump()
            for message in request.messages
        ])

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=messages
        )

        return {
            "reply": response.choices[0].message.content
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=str(error)
        )
