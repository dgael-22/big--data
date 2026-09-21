# Práctica — Comparación de modelos de regresión

## Introducción

Práctica correspondiente a la materia de **Big Data**, en el tema de **Introducción al
aprendizaje supervisado** (Unidad 3).

El objetivo es construir tres modelos de aprendizaje supervisado para proyectar el número de
**nacimientos** y **defunciones** de México, utilizando como única variable predictora el año, y
observar cómo tres modelos distintos generan predicciones distintas a partir de exactamente los
mismos datos históricos.

Los modelos construidos son:

1. **Regresión lineal** — ajusta una recta.
2. **Regresión polinomial** (grado 2) — permite representar una curva.
3. **Random Forest Regressor** — conjunto de árboles de decisión.

En esta práctica los modelos únicamente se construyen y se comparan visualmente. La evaluación
formal mediante métricas corresponde a la siguiente práctica.

El análisis se realiza con **Python**, utilizando:

- **Pandas** — carga del CSV, renombrado de columnas, filtrado por país y separación de periodos.
- **NumPy** — generación de los años futuros y manejo de arreglos.
- **Matplotlib** — visualización de los datos históricos y de las proyecciones.
- **Scikit-learn** — construcción y entrenamiento de los tres modelos.
- **Jupyter Notebook** — entorno donde se documenta y ejecuta la práctica.

## Fuente de los datos

Los datos provienen de **Our World in Data (OWID)**, del conjunto de datos **"Births and deaths
projected to 2100"**, elaborado a partir de las estimaciones y proyecciones de la ONU.

- **Dataset:** Births and deaths projected to 2100
- **Organización:** Our World in Data — a partir de United Nations, World Population Prospects (2024)
- **URL:** <https://ourworldindata.org/grapher/births-and-deaths-projected-to-2100>
- **Archivo utilizado:** `data/raw/births-and-deaths-projected-to-2100.csv`

Cada fila del CSV corresponde a una **entidad (país o región) en un año determinado**, e incluye
los nacimientos y las defunciones de ese año. Los datos históricos y las proyecciones de la ONU
vienen en columnas separadas, por lo que en el notebook se unifican en las columnas `births` y
`deaths`.

El notebook descarga el archivo directamente desde OWID. Si no hay conexión, utiliza la copia
guardada en `data/raw/`.

## Datos utilizados

- **País analizado:** México
- **Datos de entrenamiento:** 74 registros, de 1950 a 2023 (último año con dato histórico).
- **Años proyectados:** 77 años, de 2024 a 2100.
- **Variable predictora (X):** `Year`
- **Variables objetivo (y):** `births` y `deaths`

## Resultados

| Modelo | Ajuste al histórico | Proyección de nacimientos en 2100 |
|---|---|---|
| Regresión lineal | Bajo: una recta no capta el cambio de tendencia de 1993 | 3,139,315 (sigue subiendo) |
| Regresión polinomial | Bueno: la parábola sí capta subida y bajada | −4,401,123 (valor imposible) |
| Random Forest | Casi perfecto, memoriza los años de entrenamiento | 2,054,207 (constante desde 2024) |

La conclusión de la práctica es que ningún modelo entrenado solo con el año extrapola bien hasta
2100: la recta ignora el cambio de tendencia, la parábola se desploma hasta valores negativos y el
Random Forest se queda plano porque los modelos de árboles no pueden predecir fuera del rango de
años con el que fueron entrenados.

## Estructura de la carpeta

```
U3_1_modelos_ml/
├── README.md              # Este archivo
├── requirements.txt       # Dependencias de la práctica
├── data/
│   ├── raw/               # CSV original descargado de OWID
│   └── processed/         # Datos transformados (si se generan)
├── notebooks/
│   └── U3_1_modelos_regresion_demografia.ipynb
└── src/                   # Código auxiliar reutilizable
```

## Cómo ejecutar la práctica

Desde esta carpeta:

```bash
# Crear y activar el entorno virtual
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
source .venv/bin/activate

# Instalar las dependencias
pip install -r requirements.txt

# Abrir el notebook
jupyter notebook notebooks/U3_1_modelos_regresion_demografia.ipynb
```

Después basta con ejecutar las celdas en orden, de arriba hacia abajo.
