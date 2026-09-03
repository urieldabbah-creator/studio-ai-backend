import os
import base64
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse, Response
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
    file: UploadFile = File(None),
    prompt: str = Form(...)
):
    try:
        contents = [prompt]
        
        if file:
            image_bytes = await file.read()
            contents.append(
                types.Part.from_bytes(data=image_bytes, mime_type=file.content_type or "image/jpeg")
            )

        # Usamos el modelo con soporte nativo de imagen
        response = client.models.generate_content(
            model='gemini-2.5-flash-image',
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"]
            )
        )
        
        # Extraemos la imagen binaria resultante
        if response.candidates and response.candidates[0].content.parts:
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    raw_data = part.inline_data.data
                    image_data = base64.b64decode(raw_data) if isinstance(raw_data, str) else raw_data
                    return Response(content=image_data, media_type="image/jpeg")
        
        return JSONResponse(
            status_code=400,
            content={"error": "El modelo no devolvió una imagen en esta respuesta."}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error_mensaje": str(e)}
        )
