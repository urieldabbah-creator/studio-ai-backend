from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import Response
# Asegúrate de incluir las librerías que uses para la IA (ej. PIL, etc.)

app = FastAPI()

@app.get("/")
def read_root():
    return {"status": "Backend de Studio AI activo"}

@app.post("/editar-con-ia-real/")
async def editar_con_ia(
    file: UploadFile = File(...),
    prompt: str = Form(...)
):
    # 1. Leemos los bytes de la imagen que envió Flutter
    imagen_bytes = await file.read()
    
    # 2. Aquí va tu lógica de procesamiento con IA usando el 'prompt' y los 'imagen_bytes'
    # (Por ahora, como prueba, te devolverá la misma imagen procesada con éxito)
    
    # 3. Retornamos la imagen resultante en formato binario con código 200
    return Response(content=imagen_bytes, media_type="image/jpeg")
