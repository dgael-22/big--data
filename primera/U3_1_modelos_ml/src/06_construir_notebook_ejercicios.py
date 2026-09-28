# -*- coding: utf-8 -*-
"""Construye el notebook de ejercicios (China y Mexico desde 2000) copiando la
estructura del notebook original U3_1_modelos_regresion_demografia."""
import io
import json

celdas = []


def md(texto):
    celdas.append({"cell_type": "markdown", "metadata": {}, "source": texto.strip("\n").splitlines(keepends=True)})


def code(texto):
    celdas.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": texto.strip("\n").splitlines(keepends=True),
    })


# ----------------------------------------------------------------- portada
md("""
# Ejercicios de modelos de regresión — China y México

**Materia:** Tópicos de Big Data
**Tema:** Aprendizaje supervisado con modelos de regresión
**Herramientas:** Python · Jupyter Notebook · Pandas · NumPy · Matplotlib · Scikit-learn

---

Este notebook reutiliza el trabajo del notebook `U3_1_modelos_regresion_demografia`.
Se conserva el mismo dataset, la misma preparación de datos, los mismos modelos y el
mismo estilo de gráficas. Solo se cambió lo necesario para resolver dos ejercicios:

1. **Ejercicio 1 — China:** aplicar los tres modelos a los nacimientos de China.
2. **Ejercicio 2 — México desde el año 2000:** aplicar los tres modelos a los
   nacimientos y a las defunciones de México, usando solamente los datos de 2000 en adelante.
""")

# --------------------------------------------------------------- librerias
md("""
# PARTE 1. Importar las bibliotecas

Se utilizan exactamente las mismas bibliotecas del notebook original.
""")

code("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
""")

code("""
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
""")

# ----------------------------------------------------------------- dataset
md("""
# PARTE 2. Cargar y preparar el dataset

Es el mismo archivo de **Our World in Data** que se usó en el notebook original:
*Births and deaths projected to 2100*.
""")

code("""
url = "https://ourworldindata.org/grapher/births-and-deaths-projected-to-2100.csv?v=1&csvType=full&useColumnShortNames=true"

try:
    df = pd.read_csv(
        url,
        storage_options={
            "User-Agent": "Our World In Data data fetch/1.0"
        }
    )
except Exception as error:
    print("No fue posible descargar el archivo desde internet:", error)
    print("Se utilizará el archivo local guardado en data/raw/")
    df = pd.read_csv("../data/raw/births-and-deaths-projected-to-2100.csv")

df.head()
""")

code("""
print("Dimensiones (filas, columnas):", df.shape)
print()
print("Columnas:")
for columna in df.columns:
    print("  -", columna)
""")

md("""
## Renombrar las columnas

Igual que en el notebook original: nombres más cortos y dos columnas unificadas
(`births` y `deaths`) que toman el dato histórico y, cuando no existe, la proyección de OWID.
""")

code("""
df = df.rename(columns={
    "entity": "Entity",
    "code": "Code",
    "year": "Year",
    "births__sex_all__age_all__variant_estimates": "births_estimates",
    "births__sex_all__age_all__variant_medium__projected": "births_projected",
    "deaths__sex_all__age_all__variant_estimates": "deaths_estimates",
    "deaths__sex_all__age_all__variant_medium__projected": "deaths_projected",
})

df.head()
""")

code("""
# Columna unificada: dato histórico si existe; si no, la proyección de OWID
df["births"] = df["births_estimates"].fillna(df["births_projected"])
df["deaths"] = df["deaths_estimates"].fillna(df["deaths_projected"])
df.head()
""")

md("""
## Modelos utilizados

Son los tres modelos del notebook original, con los mismos parámetros:

1. **Regresión lineal** — `LinearRegression()`
2. **Regresión polinomial** — `PolynomialFeatures(degree=2, include_bias=False)` + `LinearRegression()`
3. **Random Forest Regressor** — `RandomForestRegressor(n_estimators=100, random_state=42)`

En los dos ejercicios la variable predictora (**X**) es el año y la variable objetivo (**y**)
es el número de nacimientos o de defunciones.
""")

# ============================================================== EJERCICIO 1
md("""
---

# EJERCICIO 1 — CHINA

## 1. Extraer únicamente China

Se filtra igual que en el notebook original, solo cambia el país.
""")

code("""
pais = "China"

df_china = df[df["Entity"] == pais]

df_china.head()
""")

md("""
## 2. Mostrar los datos obtenidos
""")

code("""
print("Rango de años:", df_china["Year"].min(), "-", df_china["Year"].max())
print("Número de filas:", df_china.shape[0])

df_china[["Entity", "Year", "births", "deaths"]].head(10)
""")

code("""
plt.figure(figsize=(12, 5))

plt.plot(
    df_china["Year"],
    df_china["births"]
)

plt.title("Nacimientos en China")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.grid()
plt.show()
""")

md("""
## 3. Separar datos históricos y proyectados

Se usa el mismo punto de corte del notebook original: el año **2023**.
""")

code("""
df_historico = df_china[
    df_china["Year"] <= 2023
]

df_proyectado = df_china[
    df_china["Year"] > 2023
]

print("Histórico  ->", df_historico.shape, "| años:", df_historico["Year"].min(), "a", df_historico["Year"].max())
print("Proyectado ->", df_proyectado.shape, "| años:", df_proyectado["Year"].min(), "a", df_proyectado["Year"].max())
""")

code("""
df_historico[["Year", "births", "deaths"]].isna().sum()
""")

md("""
## 4. Preparar las variables

* **X:** el año
* **y:** los nacimientos
""")

code("""
X = df_historico[["Year"]]
y_nacimientos = df_historico["births"]

print("X.shape:", X.shape)
print("y.shape:", y_nacimientos.shape)
X.head()
""")

code("""
anios_futuros = np.arange(2024, 2101).reshape(-1, 1)

X_futuro = pd.DataFrame(anios_futuros, columns=["Year"])

X_futuro.head()
""")

md("""
## 5. China — Regresión lineal
""")

code("""
modelo_lineal = LinearRegression()

modelo_lineal.fit(X, y_nacimientos)

print("Pendiente (a):", modelo_lineal.coef_[0])
print("Intercepto (b):", modelo_lineal.intercept_)
""")

code("""
predicciones_lineal = modelo_lineal.predict(X)

predicciones_lineal_futuras = modelo_lineal.predict(X_futuro)

print(predicciones_lineal_futuras[:10])
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico["Year"],
    df_historico["births"],
    label="Datos históricos",
    alpha=0.6
)

plt.plot(
    df_historico["Year"],
    predicciones_lineal,
    color="tab:orange",
    label="Regresión lineal (ajuste histórico)"
)

plt.plot(
    anios_futuros.flatten(),
    predicciones_lineal_futuras,
    color="tab:orange",
    linestyle="--",
    label="Regresión lineal (proyección)"
)

plt.title("China — Regresión Lineal (nacimientos)")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
## 6. China — Regresión polinomial

Polinomio de grado 2, igual que en el notebook original.
""")

code("""
poly = PolynomialFeatures(
    degree=2,
    include_bias=False
)

X_poly = poly.fit_transform(X)

X_poly[:5]
""")

code("""
modelo_polinomial = LinearRegression()

modelo_polinomial.fit(
    X_poly,
    y_nacimientos
)
""")

code("""
predicciones_polinomiales = modelo_polinomial.predict(X_poly)

anios_futuros_poly = poly.transform(X_futuro)

predicciones_polinomiales_futuras = modelo_polinomial.predict(anios_futuros_poly)

print(predicciones_polinomiales_futuras[:10])
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico["Year"],
    df_historico["births"],
    label="Datos históricos",
    alpha=0.6
)

plt.plot(
    df_historico["Year"],
    predicciones_polinomiales,
    color="tab:green",
    label="Regresión polinomial (ajuste histórico)"
)

plt.plot(
    anios_futuros.flatten(),
    predicciones_polinomiales_futuras,
    color="tab:green",
    linestyle="--",
    label="Regresión polinomial (proyección)"
)

plt.title("China — Regresión Polinomial (nacimientos)")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
## 7. China — Random Forest Regressor
""")

code("""
modelo_rf = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

modelo_rf.fit(
    X,
    y_nacimientos
)
""")

code("""
predicciones_rf = modelo_rf.predict(X)

predicciones_rf_futuras = modelo_rf.predict(X_futuro)

print(predicciones_rf_futuras[:10])
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico["Year"],
    df_historico["births"],
    label="Datos históricos",
    alpha=0.6
)

plt.plot(
    df_historico["Year"],
    predicciones_rf,
    color="tab:red",
    label="Random Forest (ajuste histórico)"
)

plt.plot(
    anios_futuros.flatten(),
    predicciones_rf_futuras,
    color="tab:red",
    linestyle="--",
    label="Random Forest (proyección)"
)

plt.title("China — Random Forest (nacimientos)")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
## 8. China — Comparación de los tres modelos

Primero los valores reales contra el ajuste de cada modelo (años históricos) y después
las tres proyecciones juntas.
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico["Year"],
    df_historico["births"],
    label="Valores reales",
    alpha=0.5
)

plt.plot(df_historico["Year"], predicciones_lineal, color="tab:orange", label="Regresión lineal")
plt.plot(df_historico["Year"], predicciones_polinomiales, color="tab:green", label="Regresión polinomial")
plt.plot(df_historico["Year"], predicciones_rf, color="tab:red", label="Random Forest")

plt.title("China — Valores reales contra predicciones (1950-2023)")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

code("""
plt.figure(figsize=(14, 7))

plt.scatter(
    df_historico["Year"],
    df_historico["births"],
    label="Datos históricos",
    alpha=0.5
)

plt.plot(
    df_proyectado["Year"],
    df_proyectado["births"],
    color="black",
    linewidth=2.5,
    label="Proyección OWID"
)

plt.plot(anios_futuros.flatten(), predicciones_lineal_futuras, color="tab:orange", label="Regresión lineal")
plt.plot(anios_futuros.flatten(), predicciones_polinomiales_futuras, color="tab:green", label="Regresión polinomial")
plt.plot(anios_futuros.flatten(), predicciones_rf_futuras, color="tab:red", label="Random Forest")

plt.title("China — Comparación de los tres modelos (nacimientos)")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

code("""
anios_tabla = [2030, 2050, 2075, 2100]
indice = anios_futuros.flatten()


def construir_tabla(owid, lineal, polinomial, rf):
    tabla = pd.DataFrame(
        {
            "OWID": owid.set_index("Year").reindex(indice).to_numpy().ravel(),
            "Regresión lineal": lineal,
            "Regresión polinomial": polinomial,
            "Random Forest": rf,
        },
        index=indice
    )
    tabla.index.name = "Año"
    return tabla.loc[anios_tabla]


print("CHINA - NACIMIENTOS")
tabla_china = construir_tabla(
    df_proyectado[["Year", "births"]],
    predicciones_lineal_futuras,
    predicciones_polinomiales_futuras,
    predicciones_rf_futuras
)
display(tabla_china.style.format("{:,.0f}"))
""")

# ============================================================== EJERCICIO 2
md("""
---

# EJERCICIO 2 — MÉXICO DESDE EL AÑO 2000

## 1. Extraer México
""")

code("""
pais = "Mexico"

df_mexico = df[df["Entity"] == pais]

print("Rango de años:", df_mexico["Year"].min(), "-", df_mexico["Year"].max())
df_mexico.head()
""")

md("""
## 2. Filtrar los datos desde el año 2000

A diferencia del notebook original, aquí el entrenamiento solo usa los años **2000 a 2023**.
""")

code("""
df_mexico_2000 = df_mexico[
    df_mexico["Year"] >= 2000
]

print("Filas desde el año 2000:", df_mexico_2000.shape[0])
print("Rango de años:", df_mexico_2000["Year"].min(), "-", df_mexico_2000["Year"].max())
""")

md("""
## 3. Mostrar los datos resultantes: nacimientos y defunciones
""")

code("""
df_mexico_2000[["Entity", "Year", "births", "deaths"]].head(15)
""")

code("""
df_historico_mx = df_mexico_2000[
    df_mexico_2000["Year"] <= 2023
]

df_proyectado_mx = df_mexico_2000[
    df_mexico_2000["Year"] > 2023
]

print("Histórico  ->", df_historico_mx.shape, "| años:", df_historico_mx["Year"].min(), "a", df_historico_mx["Year"].max())
print("Proyectado ->", df_proyectado_mx.shape, "| años:", df_proyectado_mx["Year"].min(), "a", df_proyectado_mx["Year"].max())

df_historico_mx[["Year", "births", "deaths"]].isna().sum()
""")

code("""
plt.figure(figsize=(12, 5))

plt.plot(df_historico_mx["Year"], df_historico_mx["births"], label="Nacimientos")
plt.plot(df_historico_mx["Year"], df_historico_mx["deaths"], label="Defunciones")

plt.title("México desde el año 2000 — nacimientos y defunciones")
plt.xlabel("Año")
plt.ylabel("Personas por año")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
## 4. Preparar las variables

`X` vuelve a ser el año; ahora se trabajan dos variables objetivo: nacimientos y defunciones.
""")

code("""
X_mx = df_historico_mx[["Year"]]

y_nacimientos_mx = df_historico_mx["births"]
y_defunciones_mx = df_historico_mx["deaths"]

print("X_mx.shape:", X_mx.shape)
print("y_nacimientos_mx.shape:", y_nacimientos_mx.shape)
print("y_defunciones_mx.shape:", y_defunciones_mx.shape)
""")

code("""
X_futuro_mx = pd.DataFrame(anios_futuros, columns=["Year"])

X_futuro_mx.head()
""")

# ------------------------------------------------------ mexico nacimientos
md("""
---

## 5. México — NACIMIENTOS

### 5.1 Regresión lineal
""")

code("""
modelo_lineal_nac = LinearRegression()

modelo_lineal_nac.fit(X_mx, y_nacimientos_mx)

print("Pendiente (a):", modelo_lineal_nac.coef_[0])
print("Intercepto (b):", modelo_lineal_nac.intercept_)

predicciones_lineal_nac = modelo_lineal_nac.predict(X_mx)
predicciones_lineal_nac_futuras = modelo_lineal_nac.predict(X_futuro_mx)
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico_mx["Year"],
    df_historico_mx["births"],
    label="Datos históricos",
    alpha=0.6
)

plt.plot(
    df_historico_mx["Year"],
    predicciones_lineal_nac,
    color="tab:orange",
    label="Regresión lineal (ajuste histórico)"
)

plt.plot(
    anios_futuros.flatten(),
    predicciones_lineal_nac_futuras,
    color="tab:orange",
    linestyle="--",
    label="Regresión lineal (proyección)"
)

plt.title("México — Nacimientos — Regresión Lineal")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
### 5.2 Regresión polinomial
""")

code("""
poly_mx = PolynomialFeatures(
    degree=2,
    include_bias=False
)

X_poly_mx = poly_mx.fit_transform(X_mx)
anios_futuros_poly_mx = poly_mx.transform(X_futuro_mx)

modelo_polinomial_nac = LinearRegression()

modelo_polinomial_nac.fit(X_poly_mx, y_nacimientos_mx)

predicciones_polinomiales_nac = modelo_polinomial_nac.predict(X_poly_mx)
predicciones_polinomiales_nac_futuras = modelo_polinomial_nac.predict(anios_futuros_poly_mx)
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico_mx["Year"],
    df_historico_mx["births"],
    label="Datos históricos",
    alpha=0.6
)

plt.plot(
    df_historico_mx["Year"],
    predicciones_polinomiales_nac,
    color="tab:green",
    label="Regresión polinomial (ajuste histórico)"
)

plt.plot(
    anios_futuros.flatten(),
    predicciones_polinomiales_nac_futuras,
    color="tab:green",
    linestyle="--",
    label="Regresión polinomial (proyección)"
)

plt.title("México — Nacimientos — Regresión Polinomial")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
### 5.3 Random Forest Regressor
""")

code("""
modelo_rf_nac = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

modelo_rf_nac.fit(X_mx, y_nacimientos_mx)

predicciones_rf_nac = modelo_rf_nac.predict(X_mx)
predicciones_rf_nac_futuras = modelo_rf_nac.predict(X_futuro_mx)
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico_mx["Year"],
    df_historico_mx["births"],
    label="Datos históricos",
    alpha=0.6
)

plt.plot(
    df_historico_mx["Year"],
    predicciones_rf_nac,
    color="tab:red",
    label="Random Forest (ajuste histórico)"
)

plt.plot(
    anios_futuros.flatten(),
    predicciones_rf_nac_futuras,
    color="tab:red",
    linestyle="--",
    label="Random Forest (proyección)"
)

plt.title("México — Nacimientos — Random Forest")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
### 5.4 Nacimientos: valores reales contra predicciones
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico_mx["Year"],
    df_historico_mx["births"],
    label="Valores reales",
    alpha=0.5
)

plt.plot(df_historico_mx["Year"], predicciones_lineal_nac, color="tab:orange", label="Regresión lineal")
plt.plot(df_historico_mx["Year"], predicciones_polinomiales_nac, color="tab:green", label="Regresión polinomial")
plt.plot(df_historico_mx["Year"], predicciones_rf_nac, color="tab:red", label="Random Forest")

plt.title("México — Nacimientos — Valores reales contra predicciones (2000-2023)")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

# ------------------------------------------------------ mexico defunciones
md("""
---

## 6. México — DEFUNCIONES

Se repite exactamente el mismo proceso, cambiando la variable objetivo.

### 6.1 Regresión lineal
""")

code("""
modelo_lineal_def = LinearRegression()

modelo_lineal_def.fit(X_mx, y_defunciones_mx)

print("Pendiente (a):", modelo_lineal_def.coef_[0])
print("Intercepto (b):", modelo_lineal_def.intercept_)

predicciones_lineal_def = modelo_lineal_def.predict(X_mx)
predicciones_lineal_def_futuras = modelo_lineal_def.predict(X_futuro_mx)
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico_mx["Year"],
    df_historico_mx["deaths"],
    label="Datos históricos",
    alpha=0.6
)

plt.plot(
    df_historico_mx["Year"],
    predicciones_lineal_def,
    color="tab:orange",
    label="Regresión lineal (ajuste histórico)"
)

plt.plot(
    anios_futuros.flatten(),
    predicciones_lineal_def_futuras,
    color="tab:orange",
    linestyle="--",
    label="Regresión lineal (proyección)"
)

plt.title("México — Defunciones — Regresión Lineal")
plt.xlabel("Año")
plt.ylabel("Defunciones")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
### 6.2 Regresión polinomial
""")

code("""
modelo_polinomial_def = LinearRegression()

modelo_polinomial_def.fit(X_poly_mx, y_defunciones_mx)

predicciones_polinomiales_def = modelo_polinomial_def.predict(X_poly_mx)
predicciones_polinomiales_def_futuras = modelo_polinomial_def.predict(anios_futuros_poly_mx)
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico_mx["Year"],
    df_historico_mx["deaths"],
    label="Datos históricos",
    alpha=0.6
)

plt.plot(
    df_historico_mx["Year"],
    predicciones_polinomiales_def,
    color="tab:green",
    label="Regresión polinomial (ajuste histórico)"
)

plt.plot(
    anios_futuros.flatten(),
    predicciones_polinomiales_def_futuras,
    color="tab:green",
    linestyle="--",
    label="Regresión polinomial (proyección)"
)

plt.title("México — Defunciones — Regresión Polinomial")
plt.xlabel("Año")
plt.ylabel("Defunciones")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
### 6.3 Random Forest Regressor
""")

code("""
modelo_rf_def = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

modelo_rf_def.fit(X_mx, y_defunciones_mx)

predicciones_rf_def = modelo_rf_def.predict(X_mx)
predicciones_rf_def_futuras = modelo_rf_def.predict(X_futuro_mx)
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico_mx["Year"],
    df_historico_mx["deaths"],
    label="Datos históricos",
    alpha=0.6
)

plt.plot(
    df_historico_mx["Year"],
    predicciones_rf_def,
    color="tab:red",
    label="Random Forest (ajuste histórico)"
)

plt.plot(
    anios_futuros.flatten(),
    predicciones_rf_def_futuras,
    color="tab:red",
    linestyle="--",
    label="Random Forest (proyección)"
)

plt.title("México — Defunciones — Random Forest")
plt.xlabel("Año")
plt.ylabel("Defunciones")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
### 6.4 Defunciones: valores reales contra predicciones
""")

code("""
plt.figure(figsize=(12, 6))

plt.scatter(
    df_historico_mx["Year"],
    df_historico_mx["deaths"],
    label="Valores reales",
    alpha=0.5
)

plt.plot(df_historico_mx["Year"], predicciones_lineal_def, color="tab:orange", label="Regresión lineal")
plt.plot(df_historico_mx["Year"], predicciones_polinomiales_def, color="tab:green", label="Regresión polinomial")
plt.plot(df_historico_mx["Year"], predicciones_rf_def, color="tab:red", label="Random Forest")

plt.title("México — Defunciones — Valores reales contra predicciones (2000-2023)")
plt.xlabel("Año")
plt.ylabel("Defunciones")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

# ---------------------------------------------------- comparacion mexico
md("""
---

## 7. México — Comparación de resultados

Las proyecciones de los tres modelos, separando claramente **nacimientos** y **defunciones**.
""")

code("""
plt.figure(figsize=(14, 7))

plt.plot(
    df_proyectado_mx["Year"],
    df_proyectado_mx["births"],
    color="black",
    linewidth=2.5,
    label="Proyección OWID"
)

plt.plot(anios_futuros.flatten(), predicciones_lineal_nac_futuras, color="tab:orange", label="Regresión lineal")
plt.plot(anios_futuros.flatten(), predicciones_polinomiales_nac_futuras, color="tab:green", label="Regresión polinomial")
plt.plot(anios_futuros.flatten(), predicciones_rf_nac_futuras, color="tab:red", label="Random Forest")

plt.title("México — Nacimientos — Comparación de los tres modelos")
plt.xlabel("Año")
plt.ylabel("Nacimientos")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

code("""
plt.figure(figsize=(14, 7))

plt.plot(
    df_proyectado_mx["Year"],
    df_proyectado_mx["deaths"],
    color="black",
    linewidth=2.5,
    label="Proyección OWID"
)

plt.plot(anios_futuros.flatten(), predicciones_lineal_def_futuras, color="tab:orange", label="Regresión lineal")
plt.plot(anios_futuros.flatten(), predicciones_polinomiales_def_futuras, color="tab:green", label="Regresión polinomial")
plt.plot(anios_futuros.flatten(), predicciones_rf_def_futuras, color="tab:red", label="Random Forest")

plt.title("México — Defunciones — Comparación de los tres modelos")
plt.xlabel("Año")
plt.ylabel("Defunciones")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

code("""
print("MÉXICO (datos desde 2000) - NACIMIENTOS")
tabla_mx_nacimientos = construir_tabla(
    df_proyectado_mx[["Year", "births"]],
    predicciones_lineal_nac_futuras,
    predicciones_polinomiales_nac_futuras,
    predicciones_rf_nac_futuras
)
display(tabla_mx_nacimientos.style.format("{:,.0f}"))

print("MÉXICO (datos desde 2000) - DEFUNCIONES")
tabla_mx_defunciones = construir_tabla(
    df_proyectado_mx[["Year", "deaths"]],
    predicciones_lineal_def_futuras,
    predicciones_polinomiales_def_futuras,
    predicciones_rf_def_futuras
)
display(tabla_mx_defunciones.style.format("{:,.0f}"))
""")

# ================================================== datasets adicionales
md("""
---

# PARTE 3. Datasets adicionales de Our World in Data

Además del dataset de nacimientos y defunciones, se cargan dos indicadores más,
con el mismo método (`pd.read_csv` directo desde OWID):

1. **Total healthcare spending as a share of GDP (2000 a 2023)** — gasto total en salud
   como porcentaje del PIB.
2. **GDP per capita** — PIB por persona.
""")

md("""
## 1. Gasto en salud como porcentaje del PIB
""")

code("""
df_health = pd.read_csv(
    "https://ourworldindata.org/grapher/total-healthcare-expenditure-gdp.csv?v=1&csvType=full&useColumnShortNames=true",
    storage_options={"User-Agent": "Our World In Data data fetch/1.0"}
)

df_health.head()
""")

code("""
print("Dimensiones (filas, columnas):", df_health.shape)
print("Rango de años:", df_health["year"].min(), "-", df_health["year"].max())
print()
print("Columnas:")
for columna in df_health.columns:
    print("  -", columna)
""")

code("""
df_health = df_health.rename(columns={
    "entity": "Entity",
    "code": "Code",
    "year": "Year",
    "current_health_expenditure__che__as_percentage_of_gross_domestic_product__gdp__pct": "health_gdp_pct",
})

df_health.head()
""")

md("""
## 2. PIB per cápita
""")

code("""
df_gdp = pd.read_csv(
    "https://ourworldindata.org/grapher/gdp-per-capita-worldbank.csv?v=1&csvType=full&useColumnShortNames=true",
    storage_options={"User-Agent": "Our World In Data data fetch/1.0"}
)

df_gdp.head()
""")

code("""
print("Dimensiones (filas, columnas):", df_gdp.shape)
print("Rango de años:", df_gdp["year"].min(), "-", df_gdp["year"].max())
print()
print("Columnas:")
for columna in df_gdp.columns:
    print("  -", columna)
""")

code("""
df_gdp = df_gdp.rename(columns={
    "entity": "Entity",
    "code": "Code",
    "year": "Year",
    "ny_gdp_pcap_pp_kd": "gdp_per_capita",
})

df_gdp.head()
""")

md("""
## 3. Extraer China y México

Se filtran los dos países que se usaron en los ejercicios, desde el año 2000.
""")

code("""
paises = ["China", "Mexico"]

df_health_paises = df_health[
    (df_health["Entity"].isin(paises)) &
    (df_health["Year"] >= 2000)
]

df_gdp_paises = df_gdp[
    (df_gdp["Entity"].isin(paises)) &
    (df_gdp["Year"] >= 2000)
]

print("Gasto en salud ->", df_health_paises.shape)
print("PIB per cápita ->", df_gdp_paises.shape)

df_health_paises.head(10)
""")

code("""
df_gdp_paises.head(10)
""")

md("""
## 4. Gráficas de los dos indicadores

Mismo estilo de gráficas que se usó en los ejercicios anteriores.
""")

code("""
plt.figure(figsize=(12, 5))

for pais in paises:
    datos = df_health_paises[df_health_paises["Entity"] == pais]
    plt.plot(datos["Year"], datos["health_gdp_pct"], label=pais)

plt.title("Gasto total en salud como porcentaje del PIB (2000-2023)")
plt.xlabel("Año")
plt.ylabel("Porcentaje del PIB")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

code("""
plt.figure(figsize=(12, 5))

for pais in paises:
    datos = df_gdp_paises[df_gdp_paises["Entity"] == pais]
    plt.plot(datos["Year"], datos["gdp_per_capita"], label=pais)

plt.title("PIB per cápita (desde el año 2000)")
plt.xlabel("Año")
plt.ylabel("PIB per cápita")

plt.ticklabel_format(style="plain", axis="y", useOffset=False)
plt.legend()
plt.grid()
plt.show()
""")

md("""
---

# Observaciones finales

* **China:** los tres modelos parten de los mismos datos (1950-2023) y aun así dibujan
  proyecciones distintas: una recta, una curva y una línea plana.
* **México desde 2000:** al usar solo 24 años de entrenamiento, la recta y la curva quedan
  más pegadas a la tendencia reciente que cuando se usaba toda la serie desde 1950.
* En los dos ejercicios el Random Forest se queda constante después de 2023, porque los
  modelos de árboles no pueden extrapolar fuera del rango de años con el que se entrenaron.
* Igual que en el notebook original, en este trabajo solo se construyen y comparan los
  modelos; la evaluación formal con métricas corresponde a la siguiente práctica.
""")

notebook = {
    "cells": celdas,
    "metadata": {
        "kernelspec": {"display_name": "base", "language": "python", "name": "python3"},
        "language_info": {
            "codemirror_mode": {"name": "ipython", "version": 3},
            "file_extension": ".py",
            "mimetype": "text/x-python",
            "name": "python",
            "nbconvert_exporter": "python",
            "pygments_lexer": "ipython3",
            "version": "3.14.6",
        },
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

RUTA = "notebooks/U3_2_ejercicios_china_mexico.ipynb"
with io.open(RUTA, "w", encoding="utf-8", newline="\n") as f:
    json.dump(notebook, f, ensure_ascii=False, indent=1)
    f.write("\n")

print("notebook creado:", RUTA)
print("celdas:", len(celdas), "| codigo:", sum(1 for c in celdas if c["cell_type"] == "code"))
