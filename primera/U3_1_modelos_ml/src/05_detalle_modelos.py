# -*- coding: utf-8 -*-
"""Extrae el detalle interno de cada modelo: coeficientes, cortes del arbol y hojas."""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.ensemble import RandomForestRegressor

CSV = "data/raw/births-and-deaths-projected-to-2100.csv"
df = pd.read_csv(CSV).rename(columns={
    "entity": "Entity", "year": "Year",
    "births__sex_all__age_all__variant_estimates": "births_estimates",
    "births__sex_all__age_all__variant_medium__projected": "births_projected",
})
df["births"] = df["births_estimates"].fillna(df["births_projected"])
mex = df[df["Entity"] == "Mexico"].sort_values("Year")
hist = mex[mex["Year"] <= 2023]
X, y = hist[["Year"]], hist["births"]

# ---------------------------------------------------------------- lineal
lin = LinearRegression().fit(X, y)
print("LINEAL")
print("  pendiente b1 = %.4f" % lin.coef_[0])
print("  intercepto b0 = %.4f" % lin.intercept_)
print("  y(2050) = %.0f" % lin.predict(pd.DataFrame({"Year": [2050]}))[0])

# ------------------------------------------------------------ polinomial
poly = PolynomialFeatures(degree=2, include_bias=False)
Xp = poly.fit_transform(X)
pol = LinearRegression().fit(Xp, y)
b1, b2 = pol.coef_
b0 = pol.intercept_
print("POLINOMIAL  y = b0 + b1*x + b2*x^2")
print("  b0 = %.4f" % b0)
print("  b1 = %.4f" % b1)
print("  b2 = %.6f" % b2)
print("  vertice x = %.1f" % (-b1 / (2 * b2)))
for a in (2023, 2100):
    print("  %d^2 = %d  ->  y = %.0f" % (a, a * a, b0 + b1 * a + b2 * a * a))

# --------------------------------------------------------- random forest
rf = RandomForestRegressor(n_estimators=100, random_state=42).fit(X, y)
arbol = rf.estimators_[0].tree_
print("RANDOM FOREST")
print("  n_estimators = %d | criterio = %s" % (rf.n_estimators, rf.criterion))
print("  arbol 0: nodos = %d, hojas = %d, profundidad = %d"
      % (arbol.node_count, (arbol.children_left == -1).sum(), rf.estimators_[0].get_depth()))
print("  corte raiz: Year <= %.1f" % arbol.threshold[0])
izq, der = arbol.children_left[0], arbol.children_right[0]
print("  corte izquierdo: Year <= %.1f | corte derecho: Year <= %.1f"
      % (arbol.threshold[izq], arbol.threshold[der]))

# hoja que atiende a los anios futuros
hoja = rf.estimators_[0].apply(pd.DataFrame({"Year": [2100]}).to_numpy())[0]
muestras = arbol.n_node_samples[hoja]
print("  hoja para 2100 (arbol 0): valor %.0f con %d muestras" % (arbol.value[hoja].ravel()[0], muestras))
print("  prediccion del bosque para 2024 y 2100: %.0f / %.0f"
      % (rf.predict(pd.DataFrame({"Year": [2024]}))[0], rf.predict(pd.DataFrame({"Year": [2100]}))[0]))

# ultimos anios del entrenamiento, que alimentan esa hoja
ultimos = hist.tail(4)[["Year", "births"]]
print("  ultimos anios de entrenamiento:")
for _, r in ultimos.iterrows():
    print("    %d: %d" % (r["Year"], r["births"]))
print("  promedio de los ultimos 3: %.0f" % hist.tail(3)["births"].mean())
