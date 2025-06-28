from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import json
import socket
from datetime import datetime

router = APIRouter()

class Credenciales(BaseModel):
    usuario: str
    contrasena: str

@router.post("/login")
def login(credenciales: Credenciales):
    usuario_ingresado = credenciales.usuario.strip().upper()
    contrasena_ingresada = credenciales.contrasena.strip()

    try:
        with open("app/data/usuarios.json", "r", encoding="utf-8") as archivo:
            data = json.load(archivo)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Archivo de usuarios no encontrado.")

    for user in data.get("usuarios", []):
        if user["usuario"].strip().upper() == usuario_ingresado:
            # Verificamos contraseña
            if user["contrasena"] != contrasena_ingresada:
                raise HTTPException(status_code=401, detail="Contraseña incorrecta.")

            # Validamos terminal
            terminal_actual = socket.gethostname()
            terminal_registrada = user.get("terminal_id", "")
            if terminal_actual != terminal_registrada:
                raise HTTPException(
                    status_code=403,
                    detail=f"Acceso denegado. Terminal registrada: {terminal_registrada}. Terminal actual: {terminal_actual}"
                )

            # Validamos vencimiento de licencia
            fecha_str = user.get("fecha_activacion")
            if not fecha_str:
                raise HTTPException(status_code=400, detail="Este usuario no tiene fecha de activación.")
            try:
                fecha_activacion = datetime.strptime(fecha_str, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(status_code=400, detail="Formato de fecha inválido.")

            dias_transcurridos = (datetime.now() - fecha_activacion).days
            if dias_transcurridos > 90:
                raise HTTPException(
                    status_code=403,
                    detail=f"Licencia vencida hace {dias_transcurridos - 90} días."
                )

            # Todo bien
            return {
                "estado": "ok",
                "rol": user.get("rol", "USUARIO"),
                "terminal": terminal_actual,
                "dias_restantes": 90 - dias_transcurridos
            }

    raise HTTPException(status_code=404, detail="Usuario no encontrado.")
