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
# Cambiamos al modelo FLUX.1-schnell, que es mucho más estable en la API gratuita
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

@app.get("/")
def read_root():
    return {"status": "Backend de Studio AI activo"}

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
            
            if response.status_code == 503:
                return JSONResponse(
                    status_code=503,
                    content={"error_mensaje": "El modelo se está cargando en los servidores. Vuelve a intentar en 10 segundos."}
                )

            if response.status_code == 200:
                content_type = response.headers.get("content-type", "")
                if "image" in content_type:
                    return Response(content=response.content, media_type="image/jpeg")
                else:
                    return JSONResponse(
                        status_code=400,
                        content={"error_mensaje": f"Respuesta de la API: {response.text}"}
                    )
            else:
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error_mensaje": f"Error externo: {response.text}"}
                )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error_mensaje": str(e)}
        )
