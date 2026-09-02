import os
import traceback
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ServerError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.get("/")
def read_root():
    return {"status": "Backend de Studio AI activo"}

@retry(
    reraise=True,
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=2, min=2, max=15),
    retry=retry_if_exception_type(ServerError)
)
def llamar_gemini(prompt, imagen_parte):
    return client.models.generate_content(
        model='gemini-3.6-flash',
        contents=[
            prompt + ". Modifica la imagen de entrada de acuerdo al prompt y devuelve la imagen resultante editada.",
            imagen_parte
        ],
    )

@app.post("/editar-con-ia-real/")
async def editar_con_ia(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    try:
        imagen_bytes = await file.read()
        
        imagen_parte = types.Part.from_bytes(
            data=imagen_bytes,
            mime_type=file.content_type or "image/jpeg"
        )
        
        response = llamar_gemini(prompt, imagen_parte)
        
        # Buscamos la parte de imagen en la respuesta de la IA
        imagen_salida_bytes = None
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    imagen_salida_bytes = part.inline_data.data
                    break
        
        # Si el modelo devolvió una imagen editada, la usamos; si devolvió texto, rebotamos a los bytes originales
        if imagen_salida_bytes:
            return Response(content=imagen_salida_bytes, media_type="image/jpeg")
        else:
            return Response(content=imagen_bytes, media_type="image/jpeg")

    except Exception as e:
        error_detalles = traceback.format_exc()
        print("ERROR INTERNO:", error_detalles)
        return JSONResponse(
            status_code=500,
            content={
                "error_mensaje": str(e),
                "traza_completa": error_detalles
            }
        )
