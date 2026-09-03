import os
import httpx
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import JSONResponse, Response
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_TOKEN = "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"
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

@app.get("/")
def read_root():
    return {"status": "Backend de Studio AI con Hugging Face activo"}

@app.post("/editar-con-ia-real/")
async def editar_con_ia(
    file: UploadFile = File(None),
    prompt: str = Form(...)
):
    try:
        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        payload = {"inputs": prompt}

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(API_URL, headers=headers, json=payload)
            
            # Si Hugging Face devuelve error 503, el modelo se está cargando en la nube
            if response.status_code == 503:
                return JSONResponse(
                    status_code=503,
                    content={"error_mensaje": "El modelo de IA se está iniciando en los servidores de Hugging Face. Por favor, intenta de nuevo en unos segundos."}
                )

            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                # Verificamos que sea una imagen binaria y no un JSON de error de la API
                if "image" in content_type:
                    return Response(content=response.content, media_type="image/jpeg")
                else:
                    return JSONResponse(
                        status_code=400,
                        content={"error_mensaje": f"Respuesta inesperada de la API: {response.text}"}
                    )
            else:
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error_mensaje": f"Error de la API externa: {response.text}"}
                )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error_mensaje": str(e)}
        )
