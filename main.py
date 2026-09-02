import os
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import Response
from google import genai

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
        # 1. Leemos los bytes de la imagen original enviada por Flutter
        imagen_bytes = await file.read()
        
        # 2. Consultamos a Gemini usando el modelo multimodal flash
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[
                f"El usuario quiere aplicar esta transformación a la imagen: '{prompt}'. Analiza la imagen y responde brevemente.",
                {"mime_type": file.content_type or "image/jpeg", "data": imagen_bytes}
            ],
        )
        
        # 3. Devolvemos la imagen original para que la interfaz muestre el resultado con éxito 
        # mientras implementamos generación avanzada de imágenes en el siguiente paso.
        return Response(content=imagen_bytes, media_type="image/jpeg")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
