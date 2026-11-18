# Entrega U5.1 — Estado de requisitos y evidencias

**Alumno:** Diego Gael Tierra · **Fecha de trabajo:** 13/11/2026 · **Rama:** `u5-1-pyspark-databricks`

> **Discrepancia de fechas:** la plataforma marca cierre el **15/11/2026 a las 23:59**, pero las
> instrucciones mencionan revisión el **miércoles 18**. Se tomó el **15/11** como límite; no se asume prórroga.

## Resumen

| # | Requisito | Estado |
|---|---|---|
| 1 | Explorar NYC Open Data y preparar nota | ✅ Comprobado |
| 2 | Ejecutar localmente y sin errores `U5_1_preparation_pyspark_NYC_taxi.ipynb` | ✅ Comprobado |
| 3a | Databricks conectado con el repo de GitHub | ✅ Comprobado |
| 3b | Recorrido A: local → GitHub → pull en Databricks | ✅ Comprobado |
| 3c | Recorrido B: Databricks → commit & push → pull en local | ✅ Comprobado |
| — | Fusionar la rama de prueba en `main` | ⏳ Pendiente (decisión tuya) |

## 1. NYC Open Data

Nota completa: [nyc_open_data_exploracion.md](nyc_open_data_exploracion.md). Consulta del 13/11/2026 por la
API oficial del catálogo: **3,028 recursos / 2,410 datasets**, 280 de transporte, 100 con "taxi".
Ej.: *2018 Yellow Taxi Trip Data* = **112,234,626 filas**; *2023 Yellow Taxi Trip Data* = **38,310,226 filas**.
No se descargó ningún dataset completo.

## 2. Notebook en la computadora local

- Archivo: [`notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb`](../notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb)
  (el mismo archivo recibido, más un cambio mínimo).
- Entorno: Windows 11 · Python 3.12.13 (`.venv` con `uv`) · PySpark 4.3.0 · PyArrow 26.0.1 · Java 21.0.12.1 LTS.
- **Ejecución original (sin cambios):** falló en la celda 3 con
  `SparkException: Python worker failed to connect back`.
- **Cambio:** en la celda de la SparkSession, `PYSPARK_PYTHON` y `PYSPARK_DRIVER_PYTHON = sys.executable`
  (Spark usaba `python3`, que en Windows no es el Python del `.venv`). Detalle en el [README](../README.md).
- **Ejecución final:** kernel limpio con `nbconvert --execute`, 13/11/2026 17:37 (hora local), **6/6 celdas de
  código ejecutadas en orden (1→6), 0 errores**, ~3 min 45 s, salidas guardadas en el notebook:
  - Spark 4.3.0 creada con `local[*]`; DataFrame de prueba (3 filas) con `show()` y `printSchema()`.
  - Parquet remoto de enero 2025: **4 grupos de filas, 3,475,226 filas declaradas, 20 columnas**.
  - Muestra de **1,000 registros**; distancia promedio **2.78** mi, importe promedio **24.93** USD.
- Avisos no bloqueantes: `winutils.exe` / `HADOOP_HOME` y el espacio en la ruta `D:\big data` (ver README).

## 3. Databricks + GitHub + Git local

| Elemento | Valor |
|---|---|
| Workspace | Databricks **Free Edition** (sin costo), `dbc-06a53fdc-876c.cloud.databricks.com` |
| Credencial Git | GitHub vinculado con la app oficial de Databricks (OAuth, sin tokens en texto) |
| Repositorio | https://github.com/dgael-22/big--data |
| Git folder en Databricks | `/Workspace/Users/<tu correo>/big--data` |
| Rama de prueba | `u5-1-pyspark-databricks` (`main` no se tocó) |

**Recorrido A (local → Databricks)**

| Paso | Evidencia |
|---|---|
| Commit + push local | `e19b4e2` — "Prueba A: cambio creado en local…" |
| Archivo | [`sync_test/A_desde_local.md`](sync_test/A_desde_local.md), marca `PRUEBA-A-LOCAL-202611131810` |
| Pull en Databricks | Git folder pasó de `89c3212` a `e19b4e2`; archivo visible: [captura](sync_test/evidencias/A_pull_en_databricks.jpg) |

**Recorrido B (Databricks → local)**

| Paso | Evidencia |
|---|---|
| Archivo creado en Databricks | [`sync_test/B_desde_databricks.md`](sync_test/B_desde_databricks.md), marca `PRUEBA-B-DATABRICKS-202611131813` |
| Commit & Push desde Databricks | `375e07c` (autor `dgael-22`, 2026-11-14 00:17:20 UTC): "Successfully committed and pushed…" — [captura](sync_test/evidencias/B_push_desde_databricks.jpg) |
| `git pull` local | `Fast-forward e19b4e2..375e07c`, 1 archivo creado |

**Incidencias resueltas:**
- *"Invalid authorization state"* al vincular GitHub: un segundo intento sobre un estado OAuth ya usado. Al recargar,
  la credencial aparecía guardada como **GitHub (Linked)**.
- Primer push desde Databricks rechazado (*"The link to your GitHub account does not have access"*): faltaba
  instalar la app de Databricks en el repo. Al instalarla en `big--data` (paso que hiciste tú), el push funcionó.

## Cómo repetir la demostración en la revisión

**Notebook (local):** abrir el `.ipynb` en VS Code → kernel `.venv` de `U5_1_pyspark_nyc_taxi` → *Restart* → *Run All*.

**Sincronización (≈3 min):**

1. Local: editar algo pequeño en `docs/sync_test/A_desde_local.md` y ejecutar:

   ```bash
   git commit -am "Demo revision: cambio local" && git push
   ```

2. Databricks: *Workspace → big--data →* botón de rama → **Pull** → abrir el archivo y mostrar el cambio.
3. Databricks: editar `B_desde_databricks.md` → botón de rama → mensaje → **Commit & Push**.
4. Local:

   ```bash
   git pull
   ```

   Mostrar el archivo y `git log --oneline -3`.

## Acciones que dependen de ti

1. **Decidir si fusionar** `u5-1-pyspark-databricks` en `main` (PR o merge). No se hizo para proteger `main`.
2. Antes de la revisión, abrir sesión en Databricks (login.databricks.com) en el navegador que usarás.
3. Opcional: el aviso "Verify identity" del encabezado de Databricks no bloqueó nada en esta práctica.
