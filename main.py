import os
import traceback
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from google import genai
from google.genai import types

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
        
        # Usamos gemini-2.5-flash que es el estándar oficial soportado
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[prompt, imagen_parte],
        )
        
        return Response(content=imagen_bytes, media_type="image/jpeg")

    except Exception as e:
        error_detalles = traceback.format_exc()
        print("ERROR INTERNO:", error_detalles)
        # Devolvemos el detalle exacto en el JSON para verlo directo en la app o consola
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "detalles": error_detalles}
        )
