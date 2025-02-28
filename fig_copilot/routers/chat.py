from fastapi import APIRouter
from ..config import client

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/")
async def chat(prompt: str):
    chat_completion = client.chat.completions.create(
        model="grok-2-latest",
        messages=[
            {
                "role": "assistant",
                # TODO: Cutomize the assistant's personality here
                "content": "You are Grok, a chatbot inspired by the Hitchhikers Guide to the Galaxy."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        stream=False,
        temperature=0
    )

    return chat_completion.choices[0].message.content
