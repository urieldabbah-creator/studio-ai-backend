import os
from fastapi import FastAPI, File, Form, UploadFile
import requests

app = FastAPI()

REPLICATE_API_TOKEN = "r8_YkllQG7jfWj9oBeY63bOUbnmWROEN1L22Cbna"


@app.get("/")
def read_root():
  return {
      "estado": "activo",
      "mensaje": "¡El servidor de IA de Studio AI Pro está funcionando a la perfección!",
  }


@app.post("/editar-con-ia-real/")
async def editar_con_ia_real(
    file: UploadFile = File(...), prompt_usuario: str = Form(...)
):
  try:
    imagen_bytes = await file.read()
    return {
        "status": "success",
        "mensaje": (
            "Imagen recibida en el servidor con la instrucción:"
            f" '{prompt_usuario}'"
        ),
    }
  except Exception as e:
    return {"status": "error", "detalle": str(e)}
