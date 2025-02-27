from fastapi import FastAPI

from .routers import chat, accessability, inspiration

app = FastAPI(title="Fig-Copilot")

app.include_router(chat.router)
app.include_router(accessability.router)
app.include_router(inspiration.router)

@app.get("/")
async def root():
    return {"message": "Fig-Copilot Backend"}
