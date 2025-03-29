from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import accessability, annotation, support_documentation

app = FastAPI(title="Fig-Copilot")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace * with allowed domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(annotation.router)
app.include_router(accessability.router)
app.include_router(support_documentation.router)
