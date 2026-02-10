# 🛡️ ViaRisk: Inteligencia Artificial Aplicada a la Seguridad Vial

**ViaRisk** es un ecosistema avanzado de análisis y predicción de riesgo de accidentes viales en España. Utiliza modelos de **Machine Learning (XGBoost)** entrenados con microdatos abiertos de la **DGT** para transformar datos históricos en herramientas preventivas en tiempo real.

---

## 🎯 El Proyecto

A diferencia de los informes estadísticos tradicionales, **ViaRisk** no solo describe el pasado, sino que estima la probabilidad de riesgo basada en variables contextuales mediante una arquitectura moderna de software.

### Preguntas clave que resuelve:
* **Predicción:** ¿Cuál es la probabilidad de accidente dadas unas condiciones meteorológicas, horarias y geográficas específicas?
* **Patrones:** ¿Cómo influye el tipo de vía y la iluminación en la gravedad del siniestro?
* **Simulación:** Herramienta interactiva para conductores y analistas basada en modelos calibrados.

---

## 🏗️ Arquitectura del Sistema

El proyecto está dividido en tres capas principales:

1. **Data Science Core (`/notebooks`, `/api`):** * Entrenamiento de modelos **XGBoost v3**.
   * Feature Engineering avanzado (detección de nocturnidad, riesgo de visibilidad, estacionalidad).
   * API robusta construida con **FastAPI** y desplegada en **Railway**.

2. **Frontend Holo-Design (`/web`):**
   * Interfaz de alta fidelidad construida con **Astro 5** y **Tailwind CSS 4**.
   * Experiencia de usuario (UX) enfocada en la claridad de datos y rendimiento.

3. **Infraestructura:**
   * **API:** Railway (Python 3.11).
   * **Web:** Vercel / Netlify.

---

## 🧠 El Modelo (XGBoost v3)

El "cerebro" de ViaRisk es un clasificador optimizado que alcanza un equilibrio entre precisión y recall para identificar situaciones de riesgo crítico.

* **Variables clave:** Hora, Mes, Provincia, Tipo de Vía, Condiciones Meteo, Iluminación y Zona.
* **Ingeniería de variables:** Creación de indicadores sintéticos como `ES_NOCTURNO` y `RIESGO_VISIBILIDAD`.
* **Salida:** Probabilidad porcentual categorizada en niveles de riesgo (Bajo, Moderado, Crítico).

---

## 🛠️ Tecnologías Utilizadas

| Capa | Tecnologías |
| :--- | :--- |
| **Análisis de Datos** | Python, Pandas, NumPy, Matplotlib, Seaborn |
| **Machine Learning** | XGBoost, Scikit-learn, Joblib |
| **Backend API** | FastAPI, Uvicorn, Pydantic |
| **Frontend** | Astro, Tailwind CSS 4, JavaScript (ES6+) |
| **Deployment** | Railway, GitHub Actions |

---

## 📁 Estructura del Proyecto

```bash
viarisk/
├── api/            # Backend: API FastAPI y Modelo .pkl (Railway)
├── data/           # Microdatos DGT y datasets procesados
├── notebooks/      # Investigación, EDA y entrenamiento del modelo
├── web/            # Frontend: Proyecto Astro & Tailwind 4
└── README.md