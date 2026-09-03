import os
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
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
async def editar_con_ia(file: UploadFile = File(...), prompt: str = Form(...)):
  try:
    # Genera una nueva imagen real basada en el prompt del usuario utilizando Imagen
    result = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            output_mime_type="image/jpeg",
            aspect_ratio="1:1",
        ),
    )

    if result.generated_images:
      image_bytes = result.generated_images[0].image.image_bytes
      return Response(content=image_bytes, media_type="image/jpeg")

    return JSONResponse(
        status_code=400,
        content={"error": "El modelo no pudo generar la imagen."},
    )

  except Exception as e:
    return JSONResponse(status_code=500, content={"error_mensaje": str(e)})
