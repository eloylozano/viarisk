from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
import os

# 1. Configuración de rutas dinámicas para Railway
# Usamos BASE_DIR para asegurar que encuentre el archivo .pkl en el contenedor
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'modelo_vial_v3.pkl')

# Cargar el modelo V3 de forma robusta
pipeline = None
try:
    if os.path.exists(MODEL_PATH):
        pipeline = joblib.load(MODEL_PATH)
        print("✅ Modelo cargado exitosamente desde:", MODEL_PATH)
    else:
        print(f"❌ Error: No se encuentra el archivo en {MODEL_PATH}")
except Exception as e:
    print(f"❌ Error crítico cargando el modelo: {str(e)}")

app = FastAPI(title="API Predictor Vial DGT V3")

# 2. Configuración de CORS
# Permitimos todos los orígenes para evitar bloqueos con Astro/Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Esquema de datos (Asegúrate de enviar DIA_SEMANA, PROVINCIA, etc. como strings en el fetch)
class AccidenteData(BaseModel):
    HORA: int
    MES: int
    DIA_SEMANA: str
    PROVINCIA: str         
    TIPO_VIA_NOMBRE: str   
    CONDICION_METEO: str
    CONDICION_ILUMINACION: str
    ZONA_AGRUPADA: str

@app.get("/")
async def root():
    return {
        "status": "online",
        "model_loaded": pipeline is not None,
        "message": "AI Core Vial Operational"
    }

@app.post("/predict")
async def predict(data: AccidenteData):
    if pipeline is None:
        return {"error": "Modelo no disponible en el servidor. Revisa los logs de Railway."}
        
    try:
        # Convertimos el JSON a DataFrame
        input_data = data.model_dump()
        df = pd.DataFrame([input_data])
        
        # --- PROCESAMIENTO INTERNO ---
        # 1. Renombrar columnas para que coincidan con el entrenamiento
        df = df.rename(columns={
            'PROVINCIA': 'COD_PROVINCIA', 
            'TIPO_VIA_NOMBRE': 'TIPO_VIA'
        })
        
        # 2. Limpieza y tipado de datos categóricos
        cols_categoricas = ['DIA_SEMANA', 'COD_PROVINCIA', 'TIPO_VIA', 'CONDICION_METEO', 'CONDICION_ILUMINACION', 'ZONA_AGRUPADA']
        for col in cols_categoricas:
            df[col] = df[col].astype(str).str.strip()

        # 3. FEATURE ENGINEERING (Igual al entrenamiento)
        df['ES_FIN_SEMANA'] = df['DIA_SEMANA'].isin(['6', '7']).astype(int)
        df['ES_NOCTURNO'] = ((df['HORA'] >= 22) | (df['HORA'] <= 6)).astype(int)
        
        # Riesgo visibilidad: Si no es despejado (1) y no es pleno día (1)
        df['RIESGO_VISIBILIDAD'] = ((df['CONDICION_METEO'] != '1') & 
                                    (df['CONDICION_ILUMINACION'] != '1')).astype(int)
        
        # 4. Asegurar el orden exacto de las columnas que espera el Pipeline
        orden_columnas = [
            'HORA', 'MES', 'DIA_SEMANA', 'COD_PROVINCIA', 'TIPO_VIA', 
            'CONDICION_METEO', 'CONDICION_ILUMINACION', 'ZONA_AGRUPADA',
            'ES_FIN_SEMANA', 'ES_NOCTURNO', 'RIESGO_VISIBILIDAD'
        ]
        df_final = df[orden_columnas]

        # --- PREDICCIÓN ---
        # Obtenemos la probabilidad de la clase 1 (accidente/mortalidad)
        probabilidades = pipeline.predict_proba(df_final)
        prob = probabilidades[0][1]
        prob_perc = round(float(prob) * 100, 2)
        
        # Clasificación semántica de riesgo
        if prob_perc < 15:
            res, col = "Bajo", "#10b981"
        elif prob_perc < 45:
            res, col = "Moderado", "#f59e0b"
        else:
            res, col = "Crítico", "#ef4444"

        return {
            "probabilidad": prob_perc,
            "categoria": res,
            "color": col,
            "status": "success"
        }

    except Exception as e:
        return {"error": f"Error en la predicción: {str(e)}"}

# 4. Ajuste para Railway (Puerto dinámico)
if __name__ == "__main__":
    import uvicorn
    # Railway inyecta la variable de entorno PORT
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)