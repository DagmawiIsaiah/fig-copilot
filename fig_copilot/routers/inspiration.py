from fastapi import APIRouter
from ..config import client

router = APIRouter(prefix="/inspiration", tags=["inspiration"])