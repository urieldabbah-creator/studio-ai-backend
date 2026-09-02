import os
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import Response
from google import genai

app = FastAPI()

# Inicializamos el cliente oficial de Google GenAI usando la variable de entorno de Render
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
def read_root():
    return {"status": "Backend de Studio AI activo con IA real"}

@app.post("/editar-con-ia-real/")
async def editar_con_ia(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        # 1. Leemos los bytes de la imagen enviada desde tu app de Flutter
        imagen_bytes = await file.read()
        
        # 2. Enviamos la imagen y el texto (prompt) al modelo multimedia de Gemini
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                prompt,
                {"mime_type": file.content_type or "image/jpeg", "data": imagen_bytes}
            ],
        )
        
        # 3. Verificamos si el modelo devolvió una imagen editada/generada directamente
        for part in response.candidates[0].content.parts:
            if part.inline_data:
                return Response(content=part.inline_data.data, media_type="image/jpeg")
                
        # Si por alguna razón el modelo devolvió texto u otra respuesta, 
        # devolvemos la imagen original temporalmente para que la app no se detenga
        return Response(content=imagen_bytes, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
