import os
import httpx
import io
from fastapi import FastAPI, Form, UploadFile, File
from fastapi.responses import Response, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

HF_TOKEN = "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"
# Cambiamos al modelo especializado en Inpainting
API_URL = "https://api-inference.huggingface.co/models/diffusers/stable-diffusion-xl-1.0-inpainting-0.1"

@app.get("/")
def read_root():
    return {"status": "Backend de Inpainting activo"}

@app.post("/editar-con-ia-real/")
async def editar_con_ia(
    file: UploadFile = File(..., description="La imagen original a editar"),
    prompt: str = Form(..., description="La instrucción de edición, ej: 'agrega un sol'")
):
    try:
        # Leemos la imagen original y la convertimos a bytes para enviarla a HF
        image_bytes = await file.read()
        
        # Abrimos la imagen para verificar que sea válida (opcional, pero ayuda a depurar)
        # img = Image.open(io.BytesIO(image_bytes))

        headers = {"Authorization": f"Bearer {HF_TOKEN}"}
        
        # Preparamos el payload para la API de Inpainting
        payload = {
            "inputs": {
                "image": image_bytes, # Enviamos la imagen binaria cruda
                "prompt": prompt,     # La instrucción de texto
                # Nota: Este modelo XL funciona bien sin máscara explícita si el prompt es claro.
                # Si el resultado no es preciso, tendríamos que implementar una máscara en el frontend.
            }
        }

        async with httpx.AsyncClient(timeout=120.0) as client:
            # Usamos POST para enviar datos binarios complejos en el cuerpo (multipart/form-data no funcionaba bien con este modelo)
            # Para el modelo de inpainting, necesitamos enviar el json con los campos incrustados.
            # Haremos la llamada usando bytes directos en el cuerpo.
            
            # IMPORTANTE: Para enviar archivos en el payload a HF Inference API, se suele usar application/octet-stream o multipart.
            # La forma más fácil es pasar los bytes directamente.
            
            response = await client.post(API_URL, headers=headers, content=image_bytes, params={"prompt": prompt})
            
            if response.status_code == 200:
                # El modelo devuelve la imagen editada
                return Response(content=response.content, media_type="image/jpeg")
            else:
                return JSONResponse(
                    status_code=response.status_code,
                    content={"hf_error_detalle": response.text, "status_code_hf": response.status_code}
                )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error_interno": str(e)}
        )
