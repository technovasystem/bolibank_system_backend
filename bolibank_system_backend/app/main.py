from fastapi import FastAPI
from app.routes import jugadas, usuarios, premios

app = FastAPI(title="Bolíbank SYSTEM API")

# Registrar rutas
app.include_router(usuarios.router, prefix="/usuarios", tags=["Usuarios"])
app.include_router(jugadas.router, prefix="/jugadas", tags=["Jugadas"])
app.include_router(premios.router, prefix="/premios", tags=["Premios"])

@app.get("/")
def read_root():
    return {"message": "API Bolíbank SYSTEM funcionando 🔥"}