# -*- coding: utf-8 -*-
"""Analisis real del dataset OWID para la presentacion: metricas y figuras."""
import io, json, os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

AZUL_OSCURO = "#0B2545"
AZUL = "#1D7AE0"
AZUL_CLARO = "#8EC5FF"
GRIS = "#8A94A6"
ACENTO = "#FF8A3D"
VERDE = "#12A594"
ROJO = "#E5484D"

plt.rcParams.update({
    "figure.dpi": 160,
    "savefig.dpi": 160,
    "font.size": 12,
    "axes.titlesize": 15,
    "axes.titleweight": "bold",
    "axes.labelcolor": AZUL_OSCURO,
    "axes.edgecolor": GRIS,
    "axes.titlecolor": AZUL_OSCURO,
    "text.color": AZUL_OSCURO,
    "xtick.color": AZUL_OSCURO,
    "ytick.color": AZUL_OSCURO,
    "axes.grid": True,
    "grid.color": "#DDE3EC",
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

SALIDA = "reports/figuras"
os.makedirs(SALIDA, exist_ok=True)

miles = FuncFormatter(lambda v, _: format(int(v), ",").replace(",", " "))


def guardar(fig, nombre):
    fig.tight_layout()
    ruta = os.path.join(SALIDA, nombre)
    fig.savefig(ruta, bbox_inches="tight")
    plt.close(fig)
    print("figura:", ruta)


# ---------------------------------------------------------------- datos
CSV = "data/raw/births-and-deaths-projected-to-2100.csv"
df = pd.read_csv(CSV).rename(columns={
    "entity": "Entity", "code": "Code", "year": "Year",
    "births__sex_all__age_all__variant_estimates": "births_estimates",
    "births__sex_all__age_all__variant_medium__projected": "births_projected",
    "deaths__sex_all__age_all__variant_estimates": "deaths_estimates",
    "deaths__sex_all__age_all__variant_medium__projected": "deaths_projected",
})
df["births"] = df["births_estimates"].fillna(df["births_projected"])
df["deaths"] = df["deaths_estimates"].fillna(df["deaths_projected"])

info = {}
info["filas_totales"] = int(df.shape[0])
info["entidades"] = int(df["Entity"].nunique())
info["anio_min"] = int(df["Year"].min())
info["anio_max"] = int(df["Year"].max())
info["nulos_por_columna"] = {c: int(df[c].isna().sum()) for c in df.columns}

mex = df[df["Entity"] == "Mexico"].sort_values("Year")
hist = mex[mex["Year"] <= 2023]
proy = mex[mex["Year"] > 2023]
info["mexico_filas"] = int(mex.shape[0])
info["mexico_hist"] = [int(hist["Year"].min()), int(hist["Year"].max()), int(hist.shape[0])]
info["mexico_proy"] = [int(proy["Year"].min()), int(proy["Year"].max()), int(proy.shape[0])]
info["nulos_mexico_hist"] = {c: int(hist[c].isna().sum()) for c in ["Year", "births", "deaths"]}

X = hist[["Year"]]
anios_fut = np.arange(2024, 2101)
X_fut = pd.DataFrame(anios_fut, columns=["Year"])

# --------------------------------------------- particion temporal train/test
corte = 2010
tr = hist[hist["Year"] <= corte]
te = hist[hist["Year"] > corte]
info["train"] = [int(tr["Year"].min()), int(tr["Year"].max()), int(tr.shape[0])]
info["test"] = [int(te["Year"].min()), int(te["Year"].max()), int(te.shape[0])]

poly_tr = PolynomialFeatures(degree=2, include_bias=False)
Xtr_p = poly_tr.fit_transform(tr[["Year"]])
Xte_p = poly_tr.transform(te[["Year"]])

metricas = {}
predichos_test = {}
for var in ("births", "deaths"):
    ytr, yte = tr[var], te[var]
    modelos = {
        "Regresion lineal": (LinearRegression().fit(tr[["Year"]], ytr), te[["Year"]]),
        "Regresion polinomial": (LinearRegression().fit(Xtr_p, ytr), Xte_p),
        "Random Forest": (RandomForestRegressor(n_estimators=100, random_state=42).fit(tr[["Year"]], ytr), te[["Year"]]),
    }
    metricas[var] = {}
    predichos_test[var] = {}
    for nombre, (m, Xe) in modelos.items():
        pred = m.predict(Xe)
        predichos_test[var][nombre] = pred
        metricas[var][nombre] = {
            "MAE": float(mean_absolute_error(yte, pred)),
            "RMSE": float(np.sqrt(mean_squared_error(yte, pred))),
            "R2": float(r2_score(yte, pred)),
        }

# ------------------------------------ modelos entrenados con todo el historico
poly = PolynomialFeatures(degree=2, include_bias=False)
Xp = poly.fit_transform(X)
Xfp = poly.transform(X_fut)

proyecciones = {}
ajustes = {}
coef = {}
for var in ("births", "deaths"):
    y = hist[var]
    lin = LinearRegression().fit(X, y)
    pol = LinearRegression().fit(Xp, y)
    rf = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)
    ajustes[var] = {"lineal": lin.predict(X), "poly": pol.predict(Xp), "rf": rf.predict(X)}
    proyecciones[var] = {"lineal": lin.predict(X_fut), "poly": pol.predict(Xfp), "rf": rf.predict(X_fut)}
    coef[var] = {"pendiente": float(lin.coef_[0]), "intercepto": float(lin.intercept_)}

owid = {v: proy.set_index("Year")[v].reindex(anios_fut).to_numpy() for v in ("births", "deaths")}

resumen = {}
for var in ("births", "deaths"):
    resumen[var] = {
        "2100": {k: float(v[-1]) for k, v in proyecciones[var].items()},
        "2100_owid": float(owid[var][-1]),
        "2050": {k: float(v[anios_fut.tolist().index(2050)]) for k, v in proyecciones[var].items()},
        "2050_owid": float(owid[var][anios_fut.tolist().index(2050)]),
        "mae_vs_owid": {k: float(np.abs(v - owid[var]).mean()) for k, v in proyecciones[var].items()},
        "rf_valores_distintos": int(len(np.unique(proyecciones[var]["rf"]))),
        "max_hist": [int(hist.loc[hist[var].idxmax(), "Year"]), float(hist[var].max())],
        "valor_2023": float(hist[hist["Year"] == 2023][var].iloc[0]),
        "valor_1950": float(hist[hist["Year"] == 1950][var].iloc[0]),
    }
neg = [int(a) for a, v in zip(anios_fut, proyecciones["births"]["poly"]) if v < 0]
resumen["poly_primer_anio_negativo"] = neg[0] if neg else None

# ------------------------------------------------------------------ figuras
# 1. Serie historica
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(hist["Year"], hist["births"], color=AZUL, lw=2.5, label="Nacimientos")
ax.plot(hist["Year"], hist["deaths"], color=ACENTO, lw=2.5, label="Defunciones")
ax.set_title("México 1950-2023: nacimientos y defunciones")
ax.set_xlabel("Año"); ax.set_ylabel("Personas por año")
ax.yaxis.set_major_formatter(miles); ax.legend(frameon=False)
guardar(fig, "01_serie_historica.png")

# 2-4. Cada modelo
for nombre, clave, color, arch in [
    ("Regresión lineal", "lineal", ACENTO, "02_lineal.png"),
    ("Regresión polinomial (grado 2)", "poly", VERDE, "03_polinomial.png"),
    ("Random Forest", "rf", ROJO, "04_random_forest.png"),
]:
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(hist["Year"], hist["births"], s=18, color=AZUL_CLARO, label="Datos históricos", zorder=2)
    ax.plot(hist["Year"], ajustes["births"][clave], color=color, lw=2.5, label="Ajuste histórico")
    ax.plot(anios_fut, proyecciones["births"][clave], color=color, lw=2.5, ls="--", label="Proyección 2024-2100")
    ax.axhline(0, color=GRIS, lw=1)
    ax.set_title("Nacimientos en México — " + nombre)
    ax.set_xlabel("Año"); ax.set_ylabel("Nacimientos")
    ax.yaxis.set_major_formatter(miles); ax.legend(frameon=False)
    guardar(fig, arch)

# 5. Comparacion nacimientos vs OWID
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(hist["Year"], hist["births"], s=14, color=AZUL_CLARO, label="Histórico 1950-2023")
ax.plot(anios_fut, owid["births"], color=AZUL_OSCURO, lw=3, label="Proyección OWID (ONU)")
ax.plot(anios_fut, proyecciones["births"]["lineal"], color=ACENTO, lw=2, label="Regresión lineal")
ax.plot(anios_fut, proyecciones["births"]["poly"], color=VERDE, lw=2, label="Regresión polinomial")
ax.plot(anios_fut, proyecciones["births"]["rf"], color=ROJO, lw=2, label="Random Forest")
ax.axhline(0, color=GRIS, lw=1)
ax.set_title("Nacimientos: los tres modelos frente a OWID")
ax.set_xlabel("Año"); ax.set_ylabel("Nacimientos")
ax.yaxis.set_major_formatter(miles); ax.legend(frameon=False, fontsize=10)
guardar(fig, "05_comparacion_nacimientos.png")

# 6. Comparacion defunciones vs OWID
fig, ax = plt.subplots(figsize=(9, 5))
ax.scatter(hist["Year"], hist["deaths"], s=14, color=AZUL_CLARO, label="Histórico 1950-2023")
ax.plot(anios_fut, owid["deaths"], color=AZUL_OSCURO, lw=3, label="Proyección OWID (ONU)")
ax.plot(anios_fut, proyecciones["deaths"]["lineal"], color=ACENTO, lw=2, label="Regresión lineal")
ax.plot(anios_fut, proyecciones["deaths"]["poly"], color=VERDE, lw=2, label="Regresión polinomial")
ax.plot(anios_fut, proyecciones["deaths"]["rf"], color=ROJO, lw=2, label="Random Forest")
ax.set_title("Defunciones: los tres modelos frente a OWID")
ax.set_xlabel("Año"); ax.set_ylabel("Defunciones")
ax.yaxis.set_major_formatter(miles); ax.legend(frameon=False, fontsize=10)
guardar(fig, "06_comparacion_defunciones.png")

# 7. Real vs predicho en la prueba (2011-2023), nacimientos
fig, ax = plt.subplots(figsize=(9, 5))
ax.plot(te["Year"], te["births"], color=AZUL_OSCURO, lw=3, marker="o", ms=5, label="Valor real")
for nombre, color in [("Regresion lineal", ACENTO), ("Regresion polinomial", VERDE), ("Random Forest", ROJO)]:
    ax.plot(te["Year"], predichos_test["births"][nombre], color=color, lw=2, ls="--", marker="o", ms=4, label=nombre.replace("Regresion", "Regresión"))
ax.set_title("Prueba 2011-2023: valor real frente a valor predicho (nacimientos)")
ax.set_xlabel("Año"); ax.set_ylabel("Nacimientos")
ax.yaxis.set_major_formatter(miles); ax.legend(frameon=False, fontsize=10)
guardar(fig, "07_real_vs_predicho.png")

# 8. Barras de error MAE en prueba
fig, ax = plt.subplots(figsize=(9, 5))
nombres = ["Regresion lineal", "Regresion polinomial", "Random Forest"]
x = np.arange(len(nombres)); ancho = 0.35
ax.bar(x - ancho / 2, [metricas["births"][n]["MAE"] for n in nombres], ancho, color=AZUL, label="Nacimientos")
ax.bar(x + ancho / 2, [metricas["deaths"][n]["MAE"] for n in nombres], ancho, color=ACENTO, label="Defunciones")
ax.set_xticks(x); ax.set_xticklabels([n.replace("Regresion", "Regresión") for n in nombres])
ax.set_title("Error promedio (MAE) en la prueba 2011-2023")
ax.set_ylabel("Error en personas por año")
ax.yaxis.set_major_formatter(miles); ax.legend(frameon=False)
for i, n in enumerate(nombres):
    ax.text(i - ancho / 2, metricas["births"][n]["MAE"], format(int(metricas["births"][n]["MAE"]), ","),
            ha="center", va="bottom", fontsize=9)
    ax.text(i + ancho / 2, metricas["deaths"][n]["MAE"], format(int(metricas["deaths"][n]["MAE"]), ","),
            ha="center", va="bottom", fontsize=9)
guardar(fig, "08_error_mae.png")

salida = {"dataset": info, "coeficientes": coef, "metricas_prueba": metricas, "resumen_proyecciones": resumen}
io.open("reports/resultados.json", "w", encoding="utf-8").write(json.dumps(salida, indent=2, ensure_ascii=False))
print(json.dumps(salida, indent=2, ensure_ascii=False))
