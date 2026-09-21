# Big Data

Repositorio de prácticas y proyectos desarrollados durante la materia de **Big Data**.

## Descripción

Este repositorio contiene las prácticas, ejercicios y proyectos realizados durante el curso.
Cada práctica se plantea como un proyecto de datos independiente, con sus propios datos,
código, dependencias y entorno de ejecución. El repositorio permite mantener un registro de
la evolución del trabajo mediante Git y GitHub.

## Herramientas utilizadas

- **Python 3.13** — lenguaje de programación empleado en todos los análisis.
- **Pandas** — carga, exploración y manipulación de los conjuntos de datos.
- **NumPy** — operaciones numéricas y cálculo de medidas estadísticas.
- **Jupyter Notebook** — entorno de trabajo donde se documenta y ejecuta cada análisis.
- **Visual Studio Code** — editor utilizado para desarrollar los notebooks.
- **Git y GitHub** — control de versiones y publicación del trabajo.

## Organización del repositorio

Cada carpeta de la raíz corresponde a una práctica independiente. El nombre sigue la
convención `U<unidad>_<número>_<tema>`, de modo que las prácticas quedan ordenadas por
unidad y por orden de realización.

```
bigdata/
├── README.md                            # Este archivo: índice general de la materia
├── .gitignore                           # Reglas de exclusión para todas las prácticas
│
├── U1_1_probabilidad_estadistica/       # Práctica 1
│   ├── README.md                        # Documentación específica de la práctica
│   ├── requirements.txt                 # Dependencias de la práctica
│   ├── data/
│   │   ├── raw/                         # Datos originales, sin modificar
│   │   └── processed/                   # Datos transformados (si se generan)
│   ├── notebooks/                       # Notebooks del análisis
│   └── src/                             # Código auxiliar reutilizable
│
└── U3_1_modelos_ml/                     # Práctica 2
    ├── README.md
    ├── requirements.txt
    ├── data/
    │   ├── raw/
    │   └── processed/
    ├── notebooks/
    └── src/
```

Cada práctica es autónoma: tiene su propio `README.md`, su propio `requirements.txt` y su
propio entorno virtual `.venv`, que no se versiona.

## Prácticas disponibles

| Carpeta | Práctica | Unidad | Tema |
|---|---|---|---|
| [`U1_1_probabilidad_estadistica/`](U1_1_probabilidad_estadistica/) | Análisis de la evolución poblacional mundial | Unidad 1 | Probabilidad y Estadística |
| [`U3_1_modelos_ml/`](U3_1_modelos_ml/) | Comparación de modelos de regresión | Unidad 3 | Aprendizaje supervisado |

### U1_1 — Análisis de la evolución poblacional mundial

Primera exploración y análisis estadístico descriptivo del cambio anual de población a nivel
mundial. Se utiliza el conjunto de datos *Annual change in population* de **Our World in Data**,
elaborado a partir de **United Nations, World Population Prospects (2024)**. El análisis cubre la
identificación y documentación de la fuente, la carga y exploración del CSV, el cálculo de
medidas de estadística descriptiva (media, mediana, varianza, desviación estándar, mínimo y
máximo) sobre el año 2020, y la comprobación de las versiones del entorno de trabajo.

### U3_1 — Comparación de modelos de regresión

Primera práctica de aprendizaje supervisado. Se construyen tres modelos de regresión
—lineal, polinomial de grado 2 y Random Forest— para proyectar los nacimientos y las
defunciones de México hasta el año 2100, utilizando el conjunto de datos *Births and deaths
projected to 2100* de **Our World in Data**. Los tres modelos se entrenan con los mismos datos
históricos (1950–2023) y se comparan visualmente entre sí y contra las proyecciones de la ONU,
para observar los riesgos de la extrapolación.

## Cómo trabajar con una práctica

Cada práctica se ejecuta de forma independiente. Desde la carpeta de la práctica:

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

Los detalles de cada práctica —fuente de los datos, variables utilizadas, actividades y forma
de ejecución— están documentados en el `README.md` de su propia carpeta.
