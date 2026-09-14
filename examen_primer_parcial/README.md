# Examen Práctico — Primer Parcial

## Tópicos de Big Data

- **Alumno:** Diego Gael Tierra
- **Dataset asignado:** `alcohol`
- **Entregable:** `tierra_diego_examen_parcial1.ipynb`

## Fuente de los datos

Los datos provienen de **Our World in Data (OWID)**, del conjunto **"Share of adults who drank
alcohol in the last year"**. La fuente original es la **World Health Organization (WHO)**. La
notebook los descarga directo desde la API de OWID, así que no hay archivos CSV en esta carpeta.

- **URL:** <https://ourworldindata.org/grapher/share-of-adults-who-drank-alcohol-in-last-year>
- **Variable:** `alcohol__consumers_past_12_months__pct__age_standardized__sex_both_sexes`,
  renombrada a `valor` en la notebook.
- **Contenido:** 3 929 filas, 189 países, años de **2000 a 2020**, sin valores nulos.

| Variable | Descripción |
|---|---|
| `entity` | Nombre del país. |
| `code` | Código ISO de tres letras; se usa para filtrar países reales. |
| `year` | Año de la observación. |
| `valor` | Porcentaje de adultos (15+) que bebieron alcohol en los últimos 12 meses, con edad estandarizada. |

## Contenido de la notebook

0. **Datos del alumno.**
1. **Configuración del entorno virtual.**
2. **Configuración y carga de datos.**
3. **Exploración inicial.**
4. **Preguntas de análisis:**
   1. Filtrado de países reales y ranking.
   2. Filtro por país y rango de años (México y Colombia).
   3. Comparación entre 5 países.
   4. Comparación entre grupos (Latinoamérica vs. Asia).
   5. Tendencia temporal (China).
   6. Cambio porcentual de México.
   7. Estadísticas descriptivas con NumPy.
   8. Gráfica de líneas (México, China y Vietnam).
   9. Top 10 en barras (año de nacimiento vs. año más reciente).
5. **Conclusión general.**
6. **Entrega.**

## Cómo ejecutarlo

Desde esta carpeta:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install pandas numpy ipykernel matplotlib requests
```

Abrir la notebook en VS Code, seleccionar el kernel `.venv` y usar **Run All**.
