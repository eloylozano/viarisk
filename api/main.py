from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# 1. Cargar el modelo V3
pipeline = joblib.load('../data/processed/modelo_vial_v3.pkl')

app = FastAPI(title="API Predictor Vial DGT V3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Esquema de datos (Tal cual lo pide tu servidor para evitar el 422)
class AccidenteData(BaseModel):
    HORA: int
    MES: int
    DIA_SEMANA: str
    PROVINCIA: str         # Se mapeará a COD_PROVINCIA
    TIPO_VIA_NOMBRE: str   # Se mapeará a TIPO_VIA
    CONDICION_METEO: str
    CONDICION_ILUMINACION: str
    ZONA_AGRUPADA: str

@app.post("/predict")
async def predict(data: AccidenteData):
    try:
        # Convertimos el JSON a DataFrame directamente
        df = pd.DataFrame([data.model_dump()])
        
        # --- PROCESAMIENTO INTERNO ---
        # 1. Renombrar columnas para que coincidan con el entrenamiento
        df = df.rename(columns={
            'PROVINCIA': 'COD_PROVINCIA', 
            'TIPO_VIA_NOMBRE': 'TIPO_VIA'
        })
        
        # 2. Asegurar que los códigos sean strings (como '1', '2'...)
        for col in ['DIA_SEMANA', 'COD_PROVINCIA', 'TIPO_VIA', 'CONDICION_METEO', 'CONDICION_ILUMINACION', 'ZONA_AGRUPADA']:
            df[col] = df[col].astype(str).str.strip()

        # 3. FEATURE ENGINEERING (Aquí es donde daba el error de la hora)
        # Usamos siempre df['COLUMNA'] para evitar errores de variables locales
        df['ES_FIN_SEMANA'] = df['DIA_SEMANA'].isin(['6', '7']).astype(int)
        df['ES_NOCTURNO'] = ((df['HORA'] >= 22) | (df['HORA'] <= 6)).astype(int)
        
        # Riesgo visibilidad: Si meteo no es '1' (Despejado) y luz no es '1' (Pleno día)
        df['RIESGO_VISIBILIDAD'] = ((df['CONDICION_METEO'] != '1') & 
                                    (df['CONDICION_ILUMINACION'] != '1')).astype(int)
        
        # 4. Reordenar según el orden exacto que espera tu modelo
        orden = ['HORA', 'MES', 'DIA_SEMANA', 'COD_PROVINCIA', 'TIPO_VIA', 
                 'CONDICION_METEO', 'CONDICION_ILUMINACION', 'ZONA_AGRUPADA',
                 'ES_FIN_SEMANA', 'ES_NOCTURNO', 'RIESGO_VISIBILIDAD']
        df_final = df[orden]

        # --- PREDICCIÓN ---
        prob = pipeline.predict_proba(df_final)[0][1]
        prob_perc = round(float(prob) * 100, 2)
        
        # Clasificación de riesgo (basada en tu Recall de 0.66)
        # Lógica de respuesta sugerida
        if prob_perc < 15:
            res, col = "Bajo", "#10b981"      # Verde (Escenario 4: 7.41%)
        elif prob_perc < 45:
            res, col = "Moderado", "#f59e0b"  # Ámbar (Escenario 1: 32.08%)
        else:
            res, col = "Crítico", "#ef4444"   # Rojo (Escenarios 2, 3 y 5)

        return {
            "probabilidad": prob_perc,
            "categoria": res,
            "color": col
        }

    except Exception as e:
        return {"error": str(e)}