Aquí tienes el `.md` limpio, estructurado y listo para copiar y pegar:

# 🛡️ ViaRisk: Inteligencia Artificial Aplicada a la Seguridad Vial

**ViaRisk** es un ecosistema avanzado de análisis y predicción de riesgo de accidentes viales en España. Utiliza modelos de **Machine Learning (XGBoost)** entrenados con microdatos abiertos de la **DGT** para transformar datos históricos en herramientas preventivas en tiempo real.

---

## 🎯 El Proyecto

A diferencia de los informes estadísticos tradicionales, **ViaRisk** no solo describe el pasado, sino que estima la probabilidad de riesgo basada en variables contextuales mediante una arquitectura moderna de software.

### Preguntas clave que resuelve:

- **Predicción:** ¿Cuál es la probabilidad de accidente dadas unas condiciones meteorológicas, horarias y geográficas específicas?
- **Patrones:** ¿Cómo influye el tipo de vía y la iluminación en la gravedad del siniestro?
- **Simulación:** Herramienta interactiva para conductores y analistas basada en modelos calibrados.

---

## 🚀 Ejecución Rápida (Docker)

La forma más sencilla de probar el ecosistema completo (Frontend + API) es utilizando Docker, lo que garantiza que todas las dependencias funcionen correctamente.

### 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/viarisk.git
cd viarisk
````

### 2️⃣ Levantar los servicios

```bash
docker compose up --build
```

### 3️⃣ Acceso local

* **Frontend (Astro):** [http://localhost:8080](http://localhost:8080)
* **API (FastAPI):** [http://localhost:8000](http://localhost:8000)
* **Documentación API (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🏗️ Arquitectura del Sistema

El proyecto está dividido en tres capas principales que trabajan de forma coordinada:

### 🔹 Data Science Core (`/notebooks`, `/api`)

* Entrenamiento de modelos **XGBoost** de alta precisión
* Feature Engineering avanzado (nocturnidad, riesgo de visibilidad, estacionalidad)
* API robusta construida con **FastAPI** para inferencia en tiempo real

### 🔹 Frontend Holo-Design (`/web`)

* Interfaz moderna construida con **Astro 5** y **Tailwind CSS 4**
* UX diseñada para la toma de decisiones basada en datos

### 🔹 Infraestructura y Despliegue

* **Contenedores:** Orquestación completa con Docker Compose
* **Cloud:** API preparada para Railway y Frontend optimizado para Vercel / Netlify

---

## 🧠 El Modelo (XGBoost)

El “cerebro” de ViaRisk es un clasificador optimizado que identifica situaciones de riesgo crítico basándose en los microdatos de la DGT.

### Variables clave:

* Hora
* Mes
* Provincia
* Tipo de Vía
* Condiciones Meteorológicas
* Iluminación
* Zona

### Ingeniería de variables:

* Creación de indicadores sintéticos como `ES_NOCTURNO`
* Cálculo de `RIESGO_VISIBILIDAD`

### Salida del modelo:

Probabilidad porcentual categorizada en niveles de riesgo:

🟢 **Bajo**
🟡 **Moderado**
🔴 **Crítico**

---

## 🛠️ Tecnologías Utilizadas

| Capa                  | Tecnologías                                     |
| --------------------- | ----------------------------------------------- |
| **Análisis de Datos** | Python, Pandas, NumPy, Matplotlib, Seaborn      |
| **Machine Learning**  | XGBoost, Scikit-learn, Joblib                   |
| **Backend API**       | FastAPI, Uvicorn, Pydantic                      |
| **Frontend**          | Astro 5, Tailwind CSS 4, JavaScript (ES6+)      |
| **Infraestructura**   | Docker, Docker Compose, Railway, GitHub Actions |

---

## 📁 Estructura del Proyecto

```bash
viarisk/
├── api/               # Backend: API FastAPI y Modelo (.pkl/.json)
├── data/              # Microdatos DGT y datasets procesados
├── notebooks/         # Investigación, EDA y entrenamiento del modelo
├── web/               # Frontend: Proyecto Astro & Tailwind 4
├── docker-compose.yml # Orquestador de contenedores
└── README.md          # Documentación del proyecto
```

---

© 2026 ViaRisk - Inteligencia Artificial para la Seguridad Vial.

```
```
