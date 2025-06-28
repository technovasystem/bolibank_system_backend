from fastapi import APIRouter
from pydantic import BaseModel
import json
import socket
from datetime import datetime

router = APIRouter(prefix="/login", tags=["login"])

@router.get("/")
def login():
    return {"mensaje": "Login funcionando"}
