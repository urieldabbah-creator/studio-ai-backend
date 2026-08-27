import os
from fastapi import FastAPI, File, Form, UploadFile
import requests

app = FastAPI()

# Aquí más adelante pondremos tu llave secreta de Replicate
REPLICATE_API_TOKEN = "tu_api_key_de_replicate_aqui"


@app.get("/")
def read_root():
  return {"message": "¡El servidor de IA de Studio AI Pro está activo!"}


@app.post("/editar-con-ia-real/")
async def editar_con_ia_real(
    file: UploadFile = File(...), prompt_usuario: str = Form(...)
):
  try:
    imagen_bytes = await file.read()

    headers = {
        "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    return {
        "status": "success",
        "mensaje": (
            "Imagen recibida correctamente en el servidor con la instrucción:"
            f" '{prompt_usuario}'"
        ),
        "nota": "Conexión con la API de IA lista para procesar.",
    }

  except Exception as e:
    return {"status": "error", "detalle": str(e)}
