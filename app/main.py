from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import login

app = FastAPI()

# CORS para que tu app móvil o web pueda acceder al backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O ajusta a los dominios seguros
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/", methods=["GET", "HEAD", "OPTIONS"])
def inicio():
    return {"mensaje": "BoliBank SYSTEM API funcionando desde cualquier IP🚀"}

# Incluir las rutas del login
app.include_router(login.router)
