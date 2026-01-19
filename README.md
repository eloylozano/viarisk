# ViaRisk

**ViaRisk** es un proyecto de análisis y predicción del riesgo de accidentes viales en España a partir de datos abiertos de la **DGT**. El objetivo es identificar patrones, zonas y factores de riesgo asociados a siniestros de tráfico para distintos tipos de vehículos (turismos, motocicletas, vehículos pesados, etc.), y presentar esta información de forma clara y útil.

---

## 🎯 Objetivo del proyecto

Responder a preguntas como:

* ¿Dónde se concentran los accidentes de tráfico y de qué tipo?
* ¿Qué factores (hora, tipo de vía, condiciones, vehículo) influyen en la gravedad de un accidente?
* ¿Existen zonas o patrones de riesgo recurrentes que no son evidentes a simple vista?

El proyecto busca ir más allá de un análisis descriptivo básico, aportando **insights accionables** y explorando el uso de **modelos de Machine Learning** cuando estos aporten valor real.

---

## 📊 Datos

Se utilizan **datos abiertos de la Dirección General de Tráfico (DGT)**, principalmente:

* Registros de accidentes de tráfico
* Información sobre localización, tipo de vía y condiciones
* Tipología de vehículos implicados
* Gravedad del siniestro

Los datos se procesan, limpian y analizan para garantizar coherencia y calidad antes de cualquier visualización o modelado.

---

## 🧠 Enfoque

El desarrollo del proyecto sigue estas fases:

1. **Exploratory Data Analysis (EDA)**

   * Limpieza y preparación de datos
   * Análisis estadístico y visual
   * Identificación de patrones y anomalías

2. **Análisis avanzado**

   * Comparación entre tipos de vías y vehículos
   * Estudio de la gravedad de los accidentes
   * Análisis temporal y geográfico

3. **Machine Learning (cuando tenga sentido)**

   * Clasificación o predicción de riesgo
   * Modelos explicables y justificables
   * Evaluación crítica de resultados

4. **Visualización**

   * Dashboards y mapas interactivos
   * Filtros por zona, vehículo y tipo de accidente

---

## 🛠️ Tecnologías

* **Python** (pandas, numpy, matplotlib / seaborn, scikit-learn)
* **Jupyter Notebooks** para análisis y experimentación
* **Backend**: API para servir datos procesados
* **Frontend**: Visualización de datos y mapas interactivos

*(La arquitectura concreta puede evolucionar a lo largo del proyecto)*

---

## 📁 Estructura del repositorio (propuesta)

```
viarisk/
├── data/           # Datos brutos y procesados
├── notebooks/      # EDA y experimentos
├── src/            # Código de procesamiento y modelos
├── api/            # Backend / API
├── frontend/       # Interfaz de usuario
└── README.md
```

---

## 🚧 Estado del proyecto

Proyecto en desarrollo. Actualmente en fase de **exploración y análisis de datos**.

---

## 📌 Nota

Este proyecto tiene un enfoque **educativo y demostrativo**, orientado a mostrar competencias en **Data Analysis, Machine Learning y visualización**, aplicadas a un problema real de seguridad vial.
