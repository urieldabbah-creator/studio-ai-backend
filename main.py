import os
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import Response
from google import genai
from google.genai import types

app = FastAPI()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
def read_root():
    return {"status": "Backend de Studio AI activo"}

@app.post("/editar-con-ia-real/")
async def editar_con_ia(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        # 1. Leemos los bytes de la imagen enviada desde tu app de Flutter
        imagen_bytes = await file.read()
        
        # 2. Creamos la parte de la imagen usando types.Part.from_bytes como exige el SDK
        imagen_parte = types.Part.from_bytes(
            data=imagen_bytes,
            mime_type=file.content_type or "image/jpeg"
        )
        
        # 3. Enviamos la petición al modelo multimodal de Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, imagen_parte],
        )
        
        # 4. Devolvemos la imagen original para completar el ciclo con éxito 200 en esta fase de pruebas
        return Response(content=imagen_bytes, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
