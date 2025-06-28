from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json

router = APIRouter()

class Credenciales(BaseModel):
    usuario: str
    contrasena: str

@router.post("/login")
def login(credenciales: Credenciales):
    try:
        with open("data/usuarios.json", "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado")

    usuario = credenciales.usuario.upper().strip()
    contrasena = credenciales.contrasena

    for user in data.get("usuarios", []):
        if user["usuario"].upper() == usuario and user["contrasena"] == contrasena:
            return {
                "estado": "ok",
                "rol": user.get("rol", "USUARIO"),
                "fecha_activacion": user.get("fecha_activacion"),
                "terminal_id": user.get("terminal_id")
            }

    raise HTTPException(status_code=401, detail="Usuario o contraseña incorrectos")