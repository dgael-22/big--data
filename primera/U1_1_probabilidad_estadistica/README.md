# Práctica 1 — Análisis de la evolución poblacional mundial

## Introducción

Práctica correspondiente a la materia de **Big Data**, en el tema de **Probabilidad y
Estadística** (Unidad 1).

El objetivo de la práctica es realizar una primera exploración y un análisis estadístico
descriptivo del **cambio anual de población a nivel mundial**, documentando correctamente la
procedencia de los datos antes de utilizarlos.

El problema que se analiza es cómo ha variado el número neto de habitantes que gana o pierde
cada país o región de un año a otro: qué tan dispersos están esos valores entre entidades, qué
entidades presentan los cambios extremos y qué representan esas cifras en términos
demográficos.

El análisis se realiza con **Python**, utilizando:

- **Pandas** — carga del CSV, exploración del DataFrame, filtrado y selección de datos.
- **NumPy** — soporte numérico para el cálculo de las medidas estadísticas.
- **Jupyter Notebook** — entorno donde se documenta y ejecuta el análisis paso a paso.

## Fuente de los datos

Los datos provienen de **Our World in Data (OWID)**, del conjunto de datos
**"Annual change in population"**. La fuente original es **United Nations, World Population
Prospects (2024)**.

- **Dataset:** Annual change in population
- **Organización:** Our World in Data — a partir de United Nations, World Population Prospects (2024)
- **URL:** <https://ourworldindata.org/grapher/annual-population-growth>
- **Archivo utilizado:** `data/raw/annual-population-growth/annual-population-growth.csv`

> UN, World Population Prospects (2024) – processed by Our World in Data. “Annual change in
> population – UN WPP” [dataset]. United Nations, “World Population Prospects”; United Nations,
> “World Population Prospects - Interim Update” [original data].

### Contenido del conjunto de datos

Cada fila del CSV es una observación de una entidad en un año determinado. El archivo contiene
**38 400 filas y 5 columnas**.

- **Entidades:** 256 entidades únicas, que incluyen países, regiones, agrupaciones por nivel de
  ingreso y el total mundial.
- **Periodo cubierto:** de **1951 a 2100**. Los valores de **1951 a 2023** corresponden a
  estimaciones históricas y los de **2024 a 2100** a proyecciones basadas en el escenario medio
  de la ONU.

La variable principal, **`Annual change in population`**, representa el **cambio neto anual de
la población**, calculado como la diferencia entre la población al 1 de julio de años
consecutivos. Se mide en número de personas y refleja de forma combinada nacimientos,
defunciones y migración.

## Variables utilizadas

| Variable | Descripción |
|---|---|
| `Entity` | Nombre de la entidad: país, región o agrupación (por ejemplo, "Mexico", "World"). |
| `Code` | Código interno de OWID para la entidad. Para los países coincide con el código ISO alpha-3 de tres letras; las agrupaciones y regiones no tienen código. |
| `Year` | Año de la observación, como número entero. |
| `Annual change in population` | Cambio neto anual de población, en número de personas. Valores estimados del periodo histórico (1951–2023). **Variable principal del análisis.** |
| `Annual population change (Projected)` | Cambio neto anual de población proyectado (2024–2100), según el escenario medio de la ONU. |

## Estructura del repositorio

```
U1_1_probabilidad_estadistica/
├── README.md                                    # Documentación de esta práctica
├── requirements.txt                             # Dependencias necesarias
├── data/
│   ├── raw/                                     # Datos originales, sin modificar
│   │   ├── annual-population-growth/            # Dataset utilizado en el análisis
│   │   └── births-and-deaths-projected-to-2100/ # Dataset descargado como apoyo
│   └── processed/                               # Resultados generados por los pipelines
├── notebooks/
│   ├── 01_evolucion_poblacional.ipynb           # Notebook con las Actividades 1 a 4
│   ├── 01_evolucion_poblacional.html            # Exportación del notebook ejecutado
│   ├── 02_transformaciones.ipynb                # Renombrado, filtrado y agrupación (esperanza de vida)
│   ├── 3_fertilyti_rate.ipynb                   # Tasa de fertilidad: México vs. Japón
│   └── 04_examen.ipynb                          # Notebook de trabajo del examen
└── src/                                         # Pipelines de datos en Python
    ├── 01_pipeline.py                           # Pipeline paso a paso (esperanza de vida)
    ├── 02_pipeline_auto.py                      # Pipeline encapsulado en una función
    └── 03_fertility.py                          # Mismo pipeline aplicado a la tasa de fertilidad
```

Cada carpeta `data/raw/<dataset>/` incluye, además del CSV, el archivo `.metadata.json` y el
`readme.md` que proporciona Our World in Data junto con la descarga.

> **Nota:** el dataset `births-and-deaths-projected-to-2100` está descargado en `data/raw/`
> pero **no se utiliza** en el notebook de esta práctica. Se conserva como material de apoyo.

## Requisitos e instalación

Se requiere **Python 3.13**. Para reproducir el entorno de la práctica:

**Windows**

```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

Después, con el entorno activado:

```bash
pip install -r requirements.txt
```

## Cómo ejecutar el análisis

1. Activar el entorno virtual `.venv` de la práctica.
2. Abrir Jupyter Notebook (o abrir la carpeta en Visual Studio Code).
3. Entrar a la carpeta `notebooks/`.
4. Abrir el notebook `01_evolucion_poblacional.ipynb`.
5. Seleccionar como kernel el entorno virtual `.venv`.
6. Ejecutar las celdas en orden, desde el inicio.
7. Utilizar **Run All** para ejecutar el notebook completo.

El notebook está preparado para ejecutarse **de principio a fin sin errores**. Las rutas a los
datos son relativas (`../data/raw/...`), por lo que debe ejecutarse desde la carpeta
`notebooks/` para que el CSV se localice correctamente.

## Contenido del notebook

- **Actividad 1 — Identificación de la fuente:** reconocimiento de la procedencia del conjunto
  de datos antes de utilizarlo, documentación de la fuente original y de la cita oficial.
- **Actividad 2 — Carga y exploración de datos:** carga del CSV con Pandas y exploración
  inicial —primeras y últimas filas, dimensiones, nombres de columnas, tipos de datos,
  estadísticas descriptivas, valores faltantes y cantidad de entidades únicas—, cerrando con
  las preguntas de la actividad respondidas a partir de los resultados obtenidos.
- **Actividad 3 — Estadística descriptiva:** cálculo de media, mediana, varianza, desviación
  estándar, mínimo y máximo del cambio anual de población para el año **2020**, identificación
  de las entidades con el valor mínimo y máximo, y respuesta a las preguntas de la actividad.
- **Actividad 4 — Comprobación del entorno:** verificación de las versiones de Python, Pandas y
  NumPy utilizadas dentro del entorno virtual de la práctica.
- **Ejercicios adicionales de selección y filtrado:** práctica de filtrado por entidad y rango
  de años, identificación del máximo considerando únicamente países (código de tres letras) y
  ejercicios de selección de filas y columnas con `loc` e `iloc`.

### `02_transformaciones.ipynb`

Descarga directa desde la API de OWID del dataset **Life expectancy**, renombrado de columnas
(`Pais`, `Codigo`, `Anio`, `Esperanza de Vida`), uso de `set_index`, filtrado con
`str.contains`, eliminación de agregados sin código (`dropna`), agrupación con `groupby` para
obtener los 10 países con menor esperanza de vida en 2020 y cálculo de la memoria utilizada.

### `3_fertilyti_rate.ipynb`

Comparación de la tasa de fertilidad entre México y Japón: conversión a arreglos NumPy,
estadísticos básicos, filtrado por máscara booleana, `np.intersect1d` para años comunes,
`pd.merge` y gráficas con Matplotlib.

## Pipelines (`src/`)

Un **pipeline** encadena las etapas de un flujo de datos: **extracción → exploración →
limpieza → transformación → filtrado → análisis → resultado**. Los tres scripts descargan los
datos y los metadatos directamente de Our World in Data.

| Script | Dataset | Qué hace | Salida en `data/processed/` |
|---|---|---|---|
| `01_pipeline.py` | Life expectancy | Pipeline lineal: elimina nulos, redondea, filtra desde el año 2000 y promedia por país | `promedio_esperanza_vida_por_pais.csv` |
| `02_pipeline_auto.py` | Life expectancy | Pipeline dentro de la función `ejecutar_pipeline(df)`: exploración, `dropna()` y `drop_duplicates()` | `auto_resultado.csv` |
| `03_fertility.py` | Children born per woman | Reutiliza la misma función con otro dataset, mostrando que el pipeline es reutilizable | `fertility_results.csv` |

Se ejecutan **desde la carpeta de la práctica** (las rutas de salida son relativas):

```bash
python src/01_pipeline.py
python src/02_pipeline_auto.py
python src/03_fertility.py
```
