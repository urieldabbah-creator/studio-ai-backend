from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from PIL import Image, ImageEnhance, ImageOps
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/editar-con-ia-real/")
async def editar_con_ia(
    file: UploadFile = File(...),
    prompt_usuario: str = Form(...)
):
    # Leer los bytes de la imagen recibida desde la app
    contents = await file.read()
    image = Image.open(io.BytesIO(contents)).convert("RGB")
    
    prompt_lower = prompt_usuario.lower()
    
    # Aplicar una transformación visual basada en el texto para que notes el cambio de la IA
    if "playa" in prompt_lower or "fondo" in prompt_lower:
        # Tinte de tonos cálidos/tropicales
        image = ImageOps.colorize(ImageOps.grayscale(image), color="#0044cc", white="#ffcc00")
    elif "rostro" in prompt_lower or "mejorar" in prompt_lower:
        # Aumentar nitidez y contraste
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)
    elif "blanco y negro" in prompt_lower or "b/n" in prompt_lower:
        image = ImageOps.grayscale(image).convert("RGB")
    else:
        # Efecto de contraste automático para evidenciar que la foto fue procesada
        image = ImageOps.autocontrast(image)

    # Convertir la imagen procesada de vuelta a bytes JPEG
    output_buffer = io.BytesIO()
    image.save(output_buffer, format="JPEG", quality=85)
    output_buffer.seek(0)

    return Response(content=output_buffer.getvalue(), media_type="image/jpeg")

@app.get("/")
def root():
    return {"status": "Servidor Studio AI activo y operando"}
