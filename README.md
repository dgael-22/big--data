# Práctica 1 — Análisis de la evolución poblacional mundial

Práctica de **Probabilidad y Estadística**. Se realiza una primera exploración y un análisis
estadístico descriptivo del cambio anual de población a nivel mundial, utilizando Python,
Pandas, NumPy y Jupyter Notebook.

## Fuente de los datos

Los datos provienen de **Our World in Data (OWID)**. La fuente original es
**United Nations, World Population Prospects (2024)**.

> UN, World Population Prospects (2024) – processed by Our World in Data. “Annual change in
> population – UN WPP” [dataset]. United Nations, “World Population Prospects”; United Nations,
> “World Population Prospects - Interim Update” [original data].

La variable principal, *Annual change in population*, representa el **cambio neto anual de la
población** (diferencia entre la población al 1 de julio de años consecutivos), medido en
número de personas. Refleja de forma combinada nacimientos, defunciones y migración.

## Estructura del repositorio

```
.
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── raw/                                 # Datos originales (sin modificar)
│       ├── annual-population-growth/
│       └── births-and-deaths-projected-to-2100/
└── notebooks/
    └── 01_evolucion_poblacional.ipynb       # Notebook con las Actividades 1 a 4
```

## Requisitos e instalación

Se requiere **Python 3.13**. Para reproducir el entorno de la práctica:

```bash
# Crear y activar el entorno virtual
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

# Instalar las dependencias
pip install -r requirements.txt
```

## Cómo ejecutar el análisis

1. Abrir el notebook `notebooks/01_evolucion_poblacional.ipynb` en VS Code o Jupyter.
2. Seleccionar como kernel el entorno virtual `.venv`.
3. Ejecutar todas las celdas desde el inicio (**Run All**).

El notebook está preparado para ejecutarse **de principio a fin sin errores**.

## Contenido del notebook

- **Actividad 1 — Identificación de la fuente:** documentación y cita de la fuente de datos.
- **Actividad 2 — Carga y exploración de datos:** carga del CSV y exploración inicial
  (dimensiones, columnas, tipos de datos, estadísticas, valores faltantes y número de entidades).
- **Actividad 3 — Estadística descriptiva:** medidas estadísticas (media, mediana, varianza,
  desviación estándar, mínimo y máximo) sobre el cambio anual de población de un año histórico.
- **Actividad 4 — Comprobación del entorno:** verificación de las versiones de Python, Pandas y NumPy.
