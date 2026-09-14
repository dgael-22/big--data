# Big Data

Repositorio de prácticas y proyectos desarrollados durante la materia de **Big Data**.

## Descripción

Este repositorio contiene las prácticas, ejercicios y proyectos realizados
durante el curso. Cada práctica se plantea como un proyecto de datos
independiente, con sus propios datos, código, dependencias y entorno de
ejecución.

El repositorio permite mantener un registro de la evolución del trabajo
mediante Git y GitHub.

## Estructura del repositorio

Cada carpeta corresponde a una práctica o proyecto independiente:

```
big data/
│
├── .gitignore                              # Archivos/carpetas que Git debe ignorar
├── README.md                               # Documentación del curso
│
├── primera/
│   └── U1_1_probabilidad_estadistica/      # Práctica 1: probabilidad y estadística
│       ├── requirements.txt
│       ├── data/
│       │   ├── raw/
│       │   └── processed/
│       ├── notebooks/
│       ├── src/
│       └── README.md
│
└── examen_primer_parcial/                  # Examen del primer parcial
    └── tierra_diego_examen_parcial1.ipynb
```

## Reglas del repositorio

- Un solo repositorio Git y un solo repositorio GitHub para toda la materia.
- Cada práctica es un proyecto independiente con su propio `requirements.txt`.
- Cada práctica tiene su propio entorno virtual (`.venv`), que **nunca** se sube a GitHub.
