# Actividad 1 — Exploración de NYC Open Data

**Fecha de consulta:** 13 de noviembre de 2026 (17:30 hora del centro de México, 23:30 UTC).
**Método:** visita al portal y consultas a la API pública del catálogo (Socrata). Para el número de filas
se usó una consulta `count(*)`: el servidor cuenta y devuelve un solo número. **No se descargó ningún
conjunto de datos completo.**

## 1. Qué es el portal y para qué sirve

[NYC Open Data](https://www.nyc.gov/opendata) es el portal oficial donde las dependencias de la Ciudad
de Nueva York publican sus datos de forma abierta y gratuita. El catálogo vive en
[data.cityofnewyork.us](https://data.cityofnewyork.us/browse) y permite:

- buscar por tema, palabra clave o [dependencia](https://www.nyc.gov/opendata/browse-data-by-agency);
- ver los datos en tabla, filtrarlos y graficarlos desde el navegador;
- consultarlos por API (SODA) o exportarlos (CSV, JSON, etc.).

Sirve para transparencia, investigación, periodismo, aplicaciones y, en esta materia, para ver datos
reales de gran volumen.

## 2. Tamaño del catálogo (consulta del 13/11/2026)

| Medida | Valor | Fuente |
|---|---|---|
| Recursos totales (datasets, mapas, gráficos, vistas filtradas) | **3,028** | API del catálogo |
| De ellos, conjuntos de datos (`datasets`) | **2,410** | API del catálogo |
| Datasets que contienen la palabra "taxi" | **100** | API del catálogo |

Datasets por categoría:

| Categoría | Datasets |
|---|---|
| City Government | 685 |
| Education | 581 |
| **Transportation** | **280** |
| Housing & Development | 177 |
| Social Services | 148 |
| Environment | 139 |
| Public Safety | 121 |
| Health | 70 |
| Business | 65 |
| Recreation | 58 |

## 3. Conjuntos de datos reales encontrados

| Dataset | Filas (count(*)) | Columnas | Categoría | Enlace |
|---|---|---|---|---|
| 2018 Yellow Taxi Trip Data | **112,234,626** | 17 | Transportation | https://data.cityofnewyork.us/d/t29m-gskq |
| 2023 Yellow Taxi Trip Data | **38,310,226** | 19 | Transportation | https://data.cityofnewyork.us/d/4b4i-vvec |
| Motor Vehicle Collisions – Crashes | **2,305,239** | 29 | Public Safety | https://data.cityofnewyork.us/d/h9gi-nx95 |
| NYC Taxi Zones (zonas geográficas) | 263 | 6 | Transportation | https://data.cityofnewyork.us/d/8meu-9t5y |
| 311 Service Requests from 2020 to Present | (no se contó: la consulta excedió 2 min) | — | — | https://data.cityofnewyork.us/d/erm2-nwe9 |

Otros relacionados con taxis que aparecen en el catálogo:

- Yellow Taxi Trip Data por año: 2014 ([gkne-dk5s](https://data.cityofnewyork.us/d/gkne-dk5s)),
  2016 ([uacg-pexx](https://data.cityofnewyork.us/d/uacg-pexx)), 2017 ([biws-g3hs](https://data.cityofnewyork.us/d/biws-g3hs)),
  2019 ([2upf-qytp](https://data.cityofnewyork.us/d/2upf-qytp)), 2020 ([kxp8-n2sj](https://data.cityofnewyork.us/d/kxp8-n2sj)),
  2021 ([m6nq-qud6](https://data.cityofnewyork.us/d/m6nq-qud6)), 2022 ([qp3b-zxtp](https://data.cityofnewyork.us/d/qp3b-zxtp)).
- Green Taxi Trip Data 2015 ([gi8d-wdg5](https://data.cityofnewyork.us/d/gi8d-wdg5)) y 2016 ([hvrh-b6nb](https://data.cityofnewyork.us/d/hvrh-b6nb)).
- Medallion Taxi Initial Inspection Schedule ([sp7n-275u](https://data.cityofnewyork.us/d/sp7n-275u)) — actualizado el mismo 13/11/2026.
- Taxi Improvement Fund (TIF) Medallion Payments ([ht4t-wzcm](https://data.cityofnewyork.us/d/ht4t-wzcm)).
- Taxi and For Hire Vehicle (FHV) Relief Stands ([vqu8-xef9](https://data.cityofnewyork.us/d/vqu8-xef9)).

## 4. Relación con el notebook U5.1

El notebook lee **enero de 2025** de Yellow Taxi desde la página de la TLC
([TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)), que publica
archivos Parquet mensuales. Ese solo mes declara **3,475,226 viajes** y 20 columnas. Si un mes tiene
~3.5 millones de viajes, un año completo ronda las decenas de millones, lo que coincide con los
38 millones de filas del dataset 2023 de NYC Open Data y los 112 millones de 2018.

## 5. Explicación sencilla para comentar en la revisión

> "NYC Open Data es el portal donde la ciudad de Nueva York publica sus datos públicos. Al consultarlo
> el 13 de noviembre de 2026 tenía 3,028 recursos, de los cuales 2,410 son datasets, de temas muy
> distintos: gobierno, educación, transporte, vivienda, salud, seguridad. Solo en transporte hay 280.
> Lo que más impresiona es el volumen: el dataset de viajes de taxi amarillo de 2018 tiene más de
> 112 millones de filas y el de 2023 más de 38 millones. El de choques de vehículos tiene 2.3 millones.
> Con ese tamaño ya no conviene abrir los datos en Excel ni cargarlos completos en la memoria de una
> laptop; por eso usamos herramientas como Spark, que procesan datos por partes y en paralelo.
> Esa es justo la motivación de la unidad: volumen (millones de registros), variedad (muchos temas y
> formatos: tablas, mapas, CSV, Parquet) y velocidad (hay datasets que se actualizan a diario)."

## Cómo repetir las cifras

En el navegador (sin descargar nada):

- Total del catálogo: https://api.us.socrata.com/api/catalog/v1?domains=data.cityofnewyork.us&only=datasets&limit=1 → campo `resultSetSize`.
- Filas de un dataset: https://data.cityofnewyork.us/resource/4b4i-vvec.json?$select=count(*)

Las cifras cambian con el tiempo porque el portal se actualiza continuamente; por eso se indica la fecha de consulta.
