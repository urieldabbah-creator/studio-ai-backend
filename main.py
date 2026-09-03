import os
import httpx
import traceback
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
            
            # Devolvemos el estatus y el texto exacto que responde Hugging Face para verlo en la app
            return JSONResponse(
                status_code=200, # Lo mandamos como 200 para que tu app Flutter pueda leer el JSON de error sin crashear
                content={
                    "hf_status": response.status_code,
                    "hf_response": response.text
                }
            )

    except Exception as e:
        # Si hay un error interno de Python, lo devolvemos como texto explicativo
        error_detalles = traceback.format_exc()
        return JSONResponse(
            status_code=200,
            content={"error_python": str(e), "traceback": error_detalles}
        )
