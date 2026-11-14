# U5.1 — Preparación de PySpark y exploración de NYC Taxi

Práctica independiente con su propio `requirements.txt` y `.venv` (el `.venv` no se sube a GitHub).

```
U5_1_pyspark_nyc_taxi/
├── notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb   # notebook del curso, ejecutado completo
├── docs/nyc_open_data_exploracion.md                    # Actividad 1
├── docs/ENTREGA_U5_1.md                                 # estado de requisitos y evidencias
├── requirements.txt
└── .venv/                                               # local, ignorado por Git
```

## Entorno comprobado (13/11/2026, Windows 11)

| Componente | Versión |
|---|---|
| Python (`.venv`, creado con `uv`) | 3.12.13 |
| PySpark | 4.3.0 |
| PyArrow | 26.0.1 |
| Java (Liberica JDK, `JAVA_HOME` ya configurado) | 21.0.12.1 LTS |

PySpark 4.x requiere Java 17 o 21. No hace falta instalar Spark aparte: viene dentro del paquete `pyspark`.

## Cómo recrear el entorno (solo si no existe `.venv`)

Desde una terminal en esta carpeta:

```bash
uv venv --python 3.12 .venv
```

```bash
uv pip install --python .venv/Scripts/python.exe -r requirements.txt
```

## Cómo abrir y ejecutar en VS Code

1. Abrir `notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb`.
2. Arriba a la derecha, **Select Kernel → Python Environments →** `.venv\Scripts\python.exe` de esta carpeta
   (también aparece como *Python 3.12 (U5_1 PySpark)*).
3. **Restart** del kernel y luego **Run All**. Tarda ~3–4 min (la celda 4–5 lee rangos del Parquet por internet).

## Cómo ejecutarlo desde la terminal (kernel limpio, guarda las salidas)

```bash
.venv/Scripts/jupyter-nbconvert.exe --to notebook --execute --inplace --ExecutePreprocessor.kernel_name=u5_1_pyspark --ExecutePreprocessor.timeout=900 notebooks/U5_1_preparation_pyspark_NYC_taxi.ipynb
```

## Cambio aplicado al notebook y motivo

Único cambio de código, en la celda de la SparkSession:

```python
os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable
```

**Motivo:** al ejecutar el notebook original en Windows, la celda 3 (`df.show()`) falló con
`SparkException: Python worker failed to connect back`. Spark arranca sus procesos *worker* con el
comando `python3`; en Windows ese comando es el acceso directo de Microsoft Store, no el Python del
`.venv`. Con el cambio, Spark usa el mismo intérprete del kernel. No se eliminó ningún ejercicio ni se
ocultó ninguna excepción; en macOS/Linux el cambio no tiene efecto.

## Avisos normales en Windows (no son errores)

- `WARN Shell: Did not find winutils.exe ... HADOOP_HOME and hadoop.home.dir are unset`: solo importa
  si se escriben archivos con Spark; este notebook no escribe nada.
- `El sistema no puede encontrar la ruta especificada` / `Missing Python executable ... defaulting to ... for SPARK_HOME`:
  lo provoca el espacio en la ruta `D:\big data`; PySpark detecta `SPARK_HOME` correctamente y continúa.
