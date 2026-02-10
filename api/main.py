from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import os

# 1. Configuración de rutas dinámicas para Railway
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'modelo_vial_v3.pkl')

# Cargar el modelo V3
try:
    pipeline = joblib.load(MODEL_PATH)
    print("✅ Modelo cargado exitosamente")
except Exception as e:
    print(f"❌ Error cargando el modelo: {str(e)}")
    pipeline = None

app = FastAPI(title="API Predictor Vial DGT V3")

# Habilitar CORS para que Astro (en Vercel) pueda consultar la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Esquema de datos
class AccidenteData(BaseModel):
    HORA: int
    MES: int
    DIA_SEMANA: str
    PROVINCIA: str         # Se mapeará a COD_PROVINCIA
    TIPO_VIA_NOMBRE: str   # Se mapeará a TIPO_VIA
    CONDICION_METEO: str
    CONDICION_ILUMINACION: str
    ZONA_AGRUPADA: str

# Endpoint de salud para verificar que la API funciona
@app.get("/")
async def root():
    return {
        "status": "online",
        "model_version": "v3",
        "message": "AI Core Vial Operational"
    }

@app.post("/predict")
async def predict(data: AccidenteData):
    if pipeline is None:
        return {"error": "Modelo no cargado en el servidor"}
        
    try:
        # Convertimos el JSON a DataFrame
        df = pd.DataFrame([data.model_dump()])
        
        # --- PROCESAMIENTO INTERNO ---
        # 1. Renombrar columnas
        df = df.rename(columns={
            'PROVINCIA': 'COD_PROVINCIA', 
            'TIPO_VIA_NOMBRE': 'TIPO_VIA'
        })
        
        # 2. Asegurar tipos string
        for col in ['DIA_SEMANA', 'COD_PROVINCIA', 'TIPO_VIA', 'CONDICION_METEO', 'CONDICION_ILUMINACION', 'ZONA_AGRUPADA']:
            df[col] = df[col].astype(str).str.strip()

        # 3. FEATURE ENGINEERING
        df['ES_FIN_SEMANA'] = df['DIA_SEMANA'].isin(['6', '7']).astype(int)
        df['ES_NOCTURNO'] = ((df['HORA'] >= 22) | (df['HORA'] <= 6)).astype(int)
        
        df['RIESGO_VISIBILIDAD'] = ((df['CONDICION_METEO'] != '1') & 
                                    (df['CONDICION_ILUMINACION'] != '1')).astype(int)
        
        # 4. Reordenar según el modelo
        orden = ['HORA', 'MES', 'DIA_SEMANA', 'COD_PROVINCIA', 'TIPO_VIA', 
                 'CONDICION_METEO', 'CONDICION_ILUMINACION', 'ZONA_AGRUPADA',
                 'ES_FIN_SEMANA', 'ES_NOCTURNO', 'RIESGO_VISIBILIDAD']
        df_final = df[orden]

        # --- PREDICCIÓN ---
        prob = pipeline.predict_proba(df_final)[0][1]
        prob_perc = round(float(prob) * 100, 2)
        
        # Clasificación de riesgo
        if prob_perc < 15:
            res, col = "Bajo", "#10b981"
        elif prob_perc < 45:
            res, col = "Moderado", "#f59e0b"
        else:
            res, col = "Crítico", "#ef4444"

        return {
            "probabilidad": prob_perc,
            "categoria": res,
            "color": col
        }

    except Exception as e:
        return {"error": str(e)}