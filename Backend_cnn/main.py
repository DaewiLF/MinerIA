# main.py - VERSIÓN FASTAPI
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from models.cnn_model import copper_model
import os
import uuid
from datetime import datetime

app = FastAPI(title="MinerIA API", description="API para clasificación de cobre")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "MinerIA API funcionando"}

@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Validar tipo de archivo
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            raise HTTPException(status_code=400, detail="Tipo de archivo no permitido")
        
        # Guardar archivo temporal
        file_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{uuid.uuid4().hex}{file_extension}"
        file_path = f"static/uploads/{unique_filename}"
        
        os.makedirs("static/uploads", exist_ok=True)
        
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Realizar predicción
        prediction, confidence = copper_model.predict(file_path)
        
        if prediction is None:
            raise HTTPException(status_code=500, detail="Error en la predicción")
        
        return JSONResponse({
            "filename": unique_filename,
            "resultado": prediction,
            "probabilidad": confidence
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error del servidor: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)