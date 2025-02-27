import os

from fastapi import FastAPI
from openai import OpenAI
from dotenv import load_dotenv

from .routers import chat, accessability, inspiration

# Load environment variables from .env file
load_dotenv()

app = FastAPI(title="Fig-Copilot")

client = OpenAI(
    api_key=os.environ.get("XAI_API_KEY"),
    base_url="https://api.x.ai/v1",
)

app.include_router(chat.router)
app.include_router(accessability.router)
app.include_router(inspiration.router)

@app.get("/")
async def root():
    return {"message": "Fig-Copilot Backend"}
