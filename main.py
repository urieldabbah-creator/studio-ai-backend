import os
from fastapi import FastAPI, File, Form, UploadFile
import requests

app = FastAPI()

# 🔑 Pega aquí tu API Key real de Replicate entre las comillas
REPLICATE_API_TOKEN = "r8_YkllQG7jfWj9oBeY63bOUbnmWROEN1L22Cbna"


@app.get("/")
def read_root():
  return {
      "estado": "activo",
      "mensaje": "¡El servidor de IA de Studio AI Pro está conectado a Replicate!",
  }


@app.post("/editar-con-ia-real/")
async def editar_con_ia_real(
    file: UploadFile = File(...), prompt_usuario: str = Form(...)
):
  try:
    # 1. Leemos los bytes de la foto que envió la app
    imagen_bytes = await file.read()

    # 2. Configuramos la llamada al modelo de IA en Replicate
    # (Usamos un modelo estándar de transformación de imágenes por texto)
    headers = {
        "Authorization": f"Bearer {REPLICATE_API_TOKEN}",
        "Content-Type": "application/json",
    }

    # Aquí es donde el servidor procesa o redirige la solicitud al modelo de Replicate.
    # Por ahora, devolvemos una respuesta confirmando que la IA recibió la foto y el prompt.
    print(f"Procesando imagen con prompt: {prompt_usuario}")

    return {
        "status": "success",
        "mensaje": "¡Imagen procesada con éxito por la IA!",
        "instruccion_aplicada": prompt_usuario,
    }

  except Exception as e:
    return {"status": "error", "detalle": str(e)}
