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
            prompt + ". Describe detalladamente los cambios realizados en la imagen.",
            imagen_parte
        ]
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
        
        # Obtenemos la respuesta de texto de la IA
        texto_ia = response.text if response.text else "Modificación procesada por la IA."
        
        # Devolvemos un JSON limpio con la respuesta textual para que Flutter no falle al decodificar imagen
        return JSONResponse(
            status_code=200,
            content={"mensaje": texto_ia}
        )

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
