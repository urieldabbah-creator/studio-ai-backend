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

# Token integrado directamente
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
        
        payload = {
            "inputs": prompt,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(API_URL, headers=headers, json=payload)
            
            if response.status_code == 200:
                return Response(content=response.content, media_type="image/jpeg")
            else:
                return JSONResponse(
                    status_code=response.status_code,
                    content={"error": f"Error en la API externa: {response.text}"}
                )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error_mensaje": str(e)}
        )
