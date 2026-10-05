# -*- coding: utf-8 -*-
"""Genera el PDF con la investigacion sobre el modelo que usa OWID para
proyectar la esperanza de vida hasta 2100. Solo usa matplotlib.

Cada pagina es un eje sin marco con coordenadas en pulgadas, para controlar
la maquetacion sin dependencias extra.
"""
import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

AZUL = "#0B2545"
AZUL_MEDIO = "#1D7AE0"
GRIS = "#53607A"
ACENTO = "#C2410C"

ANCHO, ALTO = 8.27, 11.69
MARGEN_X, MARGEN_SUP, MARGEN_INF = 0.85, 0.80, 0.80
ANCHO_UTIL = ANCHO - 2 * MARGEN_X

paginas = []
pagina = []
cursor = [ALTO - MARGEN_SUP]


def nueva_pagina():
    global pagina
    if pagina:
        paginas.append(pagina)
    pagina = []
    cursor[0] = ALTO - MARGEN_SUP


def espacio(p):
    cursor[0] -= p


def _hueco(alto):
    if cursor[0] - alto < MARGEN_INF:
        nueva_pagina()


def texto(contenido, x, y, **kw):
    pagina.append(("texto", contenido, x, y, kw))


def titulo(lineas, tam=18):
    _hueco(0.45 * len(lineas))
    for linea in lineas:
        texto(linea, MARGEN_X, cursor[0], fontsize=tam, color=AZUL, weight="bold", va="top")
        cursor[0] -= 0.34
    cursor[0] -= 0.05


def subtitulo(contenido, tam=12.5):
    _hueco(0.6)
    espacio(0.14)
    texto(contenido, MARGEN_X, cursor[0], fontsize=tam, color=AZUL_MEDIO, weight="bold", va="top")
    cursor[0] -= 0.30


def parrafo(contenido, tam=9.6, color="#17202A", ancho=100, interlinea=0.172):
    lineas = []
    for bloque in contenido.strip().split("\n"):
        lineas.extend(textwrap.wrap(bloque.strip(), ancho) or [""])
    for linea in lineas:
        _hueco(0.2)
        texto(linea, MARGEN_X, cursor[0], fontsize=tam, color=color, va="top")
        cursor[0] -= interlinea
    cursor[0] -= 0.07


def vinieta(contenido, tam=9.6, marca="•", ancho=95):
    lineas = textwrap.wrap(contenido.strip(), ancho)
    for i, linea in enumerate(lineas):
        _hueco(0.2)
        if i == 0:
            texto(marca, MARGEN_X + 0.05, cursor[0], fontsize=tam, color=AZUL_MEDIO, va="top")
        texto(linea, MARGEN_X + 0.26, cursor[0], fontsize=tam, color="#17202A", va="top")
        cursor[0] -= 0.172
    cursor[0] -= 0.05


def caja(contenido, tam=9.6, fondo="#EEF4FC", borde=AZUL_MEDIO, color_texto=AZUL, ancho=92):
    lineas = []
    for bloque in contenido.strip().split("\n"):
        lineas.extend(textwrap.wrap(bloque.strip(), ancho) if bloque.strip() else [""])
    alto = 0.172 * len(lineas) + 0.30
    _hueco(alto + 0.12)
    arriba = cursor[0]
    pagina.append(("caja", None, MARGEN_X, arriba, {"alto": alto, "fondo": fondo, "borde": borde}))
    cursor[0] -= 0.19
    for linea in lineas:
        texto(linea, MARGEN_X + 0.20, cursor[0], fontsize=tam, color=color_texto, va="top")
        cursor[0] -= 0.172
    cursor[0] -= 0.22


def diagrama(alto=2.55):
    _hueco(alto + 0.12)
    pagina.append(("diagrama", None, MARGEN_X, cursor[0], {"alto": alto}))
    cursor[0] -= alto + 0.10


# ------------------------------------------------------------------ contenido
titulo(["¿Qué modelo usa Our World in Data",
        "para proyectar la esperanza de vida hasta 2100?"])
texto("Investigación para la clase de Tópicos de Big Data · Diego Gael Tierra",
      MARGEN_X, cursor[0], fontsize=9.5, color=GRIS, va="top")
cursor[0] -= 0.22
pagina.append(("linea", None, MARGEN_X, cursor[0], {"ancho": ANCHO_UTIL}))
espacio(0.22)

caja("Respuesta corta: Our World in Data (OWID) no construye ningún modelo propio de predicción. Toma "
     "las proyecciones ya calculadas por la ONU en el World Population Prospects 2024, escenario medio. "
     "La ONU no usa regresión lineal ni machine learning: usa un modelo jerárquico bayesiano "
     "probabilístico, estimado por simulación MCMC, y convierte la esperanza de vida proyectada en tasas "
     "de mortalidad por edad con una versión modificada del método Lee-Carter.")

subtitulo("1. De dónde salen los datos que vemos en OWID")
parrafo(
    "En la ficha del indicador de esperanza de vida, OWID declara que combina varias fuentes según el "
    "periodo: antes de 1950 usa la Human Mortality Database (2025), Zijdeman et al. (2015) y Riley (2005); "
    "de 1950 en adelante usa el United Nations World Population Prospects (2024).")
parrafo(
    "Para el tramo futuro, OWID publica el gráfico «Life expectancy at birth – UN WPP – with medium "
    "scenario projections», con datos de 2024 a 2100. En la descripción del indicador dice que las "
    "proyecciones futuras se basan en el escenario medio de la ONU y que los valores futuros son la media "
    "de miles de trayectorias simuladas por la ONU.")
parrafo(
    "Hay un detalle que OWID señala y que conviene llevar a la clase: al ajustar su modelo de proyección, "
    "la ONU excluyó las esperanzas de vida observadas de 2020 a 2023 para que el efecto temporal del "
    "COVID-19 no distorsionara la tendencia de largo plazo.")

subtitulo("2. El modelo de la ONU, paso a paso")
parrafo(
    "Desde 2015 la División de Población de la ONU proyecta fecundidad, mortalidad y migración con métodos "
    "probabilísticos bayesianos desarrollados junto con el grupo de la Universidad de Washington. Para la "
    "esperanza de vida el procedimiento tiene cuatro etapas:")
diagrama(2.45)

nueva_pagina()

subtitulo("2.1 Esperanza de vida femenina: modelo jerárquico bayesiano")
parrafo(
    "Lo que se modela no es la esperanza de vida en sí, sino sus ganancias quinquenales. La serie se "
    "describe como un paseo aleatorio con deriva (random walk with drift), donde la deriva es una función "
    "doble logística del nivel actual de esperanza de vida.")
vinieta("La forma doble logística refleja un hecho observado: la esperanza de vida mejora más despacio en "
        "los países que están muy abajo y en los que ya están muy arriba, y más rápido en los intermedios.")
vinieta("El modelo es jerárquico: los parámetros de cada país se estiman con su propia historia, pero se "
        "encogen hacia una media mundial, de modo que un país con pocos datos se apoya en el patrón de los demás.")
vinieta("Se estima con MCMC (cadenas de Markov Monte Carlo), que produce miles de trayectorias posibles en "
        "lugar de una sola predicción.")
parrafo("Referencia: Raftery, Chunn, Gerland y Ševčíková, «Bayesian Probabilistic Projections of Life "
        "Expectancy for All Countries», Demography (2013).", tam=8.8, color=GRIS)

subtitulo("2.2 Esperanza de vida masculina: modelo de la brecha entre sexos")
parrafo(
    "La esperanza de vida masculina no se proyecta por separado. Primero se proyecta la femenina y después "
    "se modela la brecha entre mujeres y hombres, de forma conjunta para que las dos series no se crucen de "
    "manera irreal. El estudio base encontró que esa brecha crece mientras la esperanza de vida femenina "
    "está por debajo de 75 años y se reduce por encima de ese nivel.")
parrafo("Referencia: Raftery, Lalic y Gerland, «Joint probabilistic projection of female and male life "
        "expectancy», Demographic Research 30(27), 2014.", tam=8.8, color=GRIS)

subtitulo("2.3 De la esperanza de vida a las tasas de mortalidad por edad")
parrafo(
    "Una esperanza de vida no basta para proyectar una población: hace falta la mortalidad por edad y sexo. "
    "La ONU usa una versión modificada del método Lee-Carter (1992), cuyo modelo base es:")
caja("log m_x(t)  =  a_x  +  b_x · k(t)  +  ε_x(t)\n"
     "m_x(t): tasa de mortalidad a la edad x en el año t   ·   a_x: patrón de mortalidad por edad\n"
     "b_x: velocidad de cambio de cada edad   ·   k(t): índice temporal de mortalidad",
     fondo="#FFF4EC", borde=ACENTO, color_texto="#7C2D12")
parrafo(
    "La diferencia con el Lee-Carter clásico es que el índice k(t) no se proyecta con un paseo aleatorio "
    "propio, sino que se ajusta para reproducir las trayectorias de esperanza de vida del paso anterior. "
    "Además se aplican dos variantes: la coherente, que obliga a hombres y mujeres a compartir parámetros "
    "para que sus curvas no diverjan, y la rotada, que reconoce que cuando la mortalidad ya es baja las "
    "mejoras se concentran en las edades avanzadas.")
parrafo("Referencia: Ševčíková, Li, Kantorová, Gerland y Raftery, «Age-Specific Mortality and Fertility "
        "Rates for Probabilistic Population Projections» (2016).", tam=8.8, color=GRIS)

subtitulo("2.4 Qué es exactamente el «escenario medio»")
parrafo(
    "La ONU define el escenario medio como la media de la fecundidad y la mortalidad —y la mediana de la "
    "migración neta— de varios miles de trayectorias distintas obtenidas con el modelo probabilístico. Los "
    "intervalos de predicción del 80 % y del 95 % reflejan la dispersión de esas trayectorias, es decir, la "
    "incertidumbre de la proyección.")
parrafo(
    "Por eso la línea que vemos en OWID no es «la predicción», sino el centro de una nube de escenarios. La "
    "ONU publica además variantes alta, baja, de fecundidad constante, de mortalidad constante y de "
    "migración cero, pensadas para comparar supuestos, no para predecir.")

nueva_pagina()

subtitulo("3. Qué NO es este modelo, y cómo se relaciona con nuestra práctica")
parrafo(
    "En la práctica U3_1 ajustamos tres modelos de aprendizaje supervisado sobre los datos de México usando "
    "solo el año como variable predictora: regresión lineal, regresión polinomial de grado 2 y Random "
    "Forest. El contraste con lo que hace la ONU es directo:")
vinieta("Nuestros modelos aprenden una forma matemática (recta, parábola, escalones) a partir del par "
        "año → valor. El modelo de la ONU incorpora conocimiento demográfico: tablas de vida, estructura por "
        "edad y sexo, y el patrón histórico de todos los países a la vez.")
vinieta("Nuestros modelos devuelven un único número por año. El de la ONU devuelve una distribución completa "
        "de trayectorias, de la que después se resumen la línea central y los intervalos.")
vinieta("Nuestros modelos no saben que un resultado puede ser imposible: la parábola llegaba a predecir "
        "nacimientos negativos. El modelo de la ONU está construido sobre cantidades demográficas acotadas y "
        "con una forma funcional elegida para no dispararse.")
vinieta("El Random Forest no extrapola: después del último año de entrenamiento repite un valor constante. "
        "La proyección de la ONU sí extrapola, pero apoyándose en la experiencia de los países que ya pasaron "
        "por ese nivel de esperanza de vida.")

subtitulo("4. Comentarios para llevar a clase")
vinieta("OWID es un repositorio y un visualizador, no un laboratorio de pronóstico: la pregunta «qué modelo "
        "usa OWID» se responde en realidad leyendo la metodología de la ONU.")
vinieta("El escenario medio se suele leer como «lo que va a pasar», cuando es solo el centro de miles de "
        "simulaciones. Un buen hábito al presentar estas cifras es acompañarlas del intervalo del 95 %.")
vinieta("Excluir 2020-2023 del ajuste es una decisión metodológica discutible: evita que la pandemia marque "
        "la tendencia de 80 años, pero asume que fue un episodio temporal.")
vinieta("El modelo jerárquico bayesiano es, en el fondo, la misma idea que en machine learning llamamos "
        "regularización o transferencia de aprendizaje: usar la información de muchos países para estabilizar "
        "la estimación de uno solo.")
vinieta("La proyección a 2100 acumula supuestos. Para 2050 la incertidumbre es moderada; para 2100 el "
        "intervalo es amplio, y conviene decirlo al presentar una gráfica como la de OWID.")

subtitulo("5. Fuentes consultadas")
vinieta("Our World in Data — Life expectancy (ficha del indicador y sus fuentes): "
        "ourworldindata.org/grapher/life-expectancy", marca="-")
vinieta("Our World in Data — Life expectancy at birth, UN WPP, with medium scenario projections, 2024-2100: "
        "ourworldindata.org/grapher/future-life-expectancy-projections", marca="-")
vinieta("UN DESA, Population Division — World Population Prospects 2024, definición de los escenarios de "
        "proyección: population.un.org/wpp/definition-of-projection-scenarios", marca="-")
vinieta("UN DESA — World Population Prospects 2024: Methodology report: "
        "un.org/development/desa/pd/content/world-population-prospects-2024-methodology-report", marca="-")
vinieta("Raftery, A., Chunn, J., Gerland, P. y Ševčíková, H. (2013). Bayesian Probabilistic Projections of "
        "Life Expectancy for All Countries. Demography.", marca="-")
vinieta("Raftery, A., Lalic, N. y Gerland, P. (2014). Joint probabilistic projection of female and male life "
        "expectancy. Demographic Research 30(27): demographic-research.org/volumes/vol30/27", marca="-")
vinieta("Ševčíková, H., Li, N., Kantorová, V., Gerland, P. y Raftery, A. (2016). Age-Specific Mortality and "
        "Fertility Rates for Probabilistic Population Projections: arxiv.org/abs/1503.05215", marca="-")
vinieta("Lee, R. y Carter, L. (1992). Modeling and Forecasting U.S. Mortality. Journal of the American "
        "Statistical Association.", marca="-")

nueva_pagina()
if pagina:
    paginas.append(pagina)


# -------------------------------------------------------------------- dibujo
def dibujar_diagrama(ax, x, y_top, alto):
    ancho_caja = ANCHO_UTIL / 2 - 0.20
    alto_caja = 0.60
    sep_x = 0.40
    pasos = [
        ("1. Datos históricos de mortalidad\npor país (1950-2023)", "#E8F0FB", AZUL_MEDIO),
        ("2. Modelo jerárquico bayesiano (MCMC)\nganancias de e₀ femenina · doble logística", "#E8F0FB", AZUL_MEDIO),
        ("3. Brecha mujer-hombre\n→ esperanza de vida masculina", "#FFF2E8", ACENTO),
        ("4. Lee-Carter modificado\n→ tasas de mortalidad por edad y sexo", "#FFF2E8", ACENTO),
    ]
    fila1 = y_top - alto_caja
    fila2 = y_top - 2 * alto_caja - 0.45
    posiciones = [(x, fila1), (x + ancho_caja + sep_x, fila1),
                  (x, fila2), (x + ancho_caja + sep_x, fila2)]

    for (etiqueta, fondo, borde), (px, py) in zip(pasos, posiciones):
        ax.add_patch(Rectangle((px, py), ancho_caja, alto_caja, facecolor=fondo,
                               edgecolor=borde, linewidth=1.1, zorder=1))
        ax.text(px + ancho_caja / 2, py + alto_caja / 2, etiqueta, fontsize=8.4, color=AZUL,
                ha="center", va="center", zorder=2, linespacing=1.5)

    flechas = [
        ((x + ancho_caja, fila1 + alto_caja / 2), (x + ancho_caja + sep_x - 0.04, fila1 + alto_caja / 2)),
        ((x + ancho_caja + sep_x + ancho_caja / 2, fila1), (x + ancho_caja / 2, fila2 + alto_caja + 0.04)),
        ((x + ancho_caja, fila2 + alto_caja / 2), (x + ancho_caja + sep_x - 0.04, fila2 + alto_caja / 2)),
    ]
    for inicio, fin in flechas:
        ax.annotate("", xy=fin, xytext=inicio,
                    arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=1.2, shrinkA=0, shrinkB=0))

    banner_y = fila2 - 0.58
    ax.add_patch(Rectangle((x, banner_y), ANCHO_UTIL, 0.44, facecolor=AZUL, edgecolor="none", zorder=1))
    ax.text(x + ANCHO_UTIL / 2, banner_y + 0.22,
            "5. Miles de trayectorias  →  escenario medio = media de todas  +  intervalos del 80 % y 95 %",
            fontsize=8.6, color="white", ha="center", va="center", weight="bold", zorder=2)


SALIDA = sys.argv[1] if len(sys.argv) > 1 else "reports/OWID_esperanza_de_vida_metodologia.pdf"
os.makedirs(os.path.dirname(SALIDA) or ".", exist_ok=True)
VISTA_PREVIA = os.environ.get("VISTA_PREVIA")

with PdfPages(SALIDA) as pdf:
    for numero, bloques in enumerate(paginas, start=1):
        fig = plt.figure(figsize=(ANCHO, ALTO))
        fig.patch.set_facecolor("white")
        ax = fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(0, ANCHO)
        ax.set_ylim(0, ALTO)
        ax.set_axis_off()

        for tipo, contenido, x, y, extra in bloques:
            if tipo == "texto":
                ax.text(x, y, contenido, **extra)
            elif tipo == "linea":
                ax.plot([x, x + extra["ancho"]], [y, y], color=AZUL_MEDIO, lw=1.3)
            elif tipo == "caja":
                ax.add_patch(Rectangle((x, y - extra["alto"]), ANCHO_UTIL, extra["alto"],
                                       facecolor=extra["fondo"], edgecolor=extra["borde"],
                                       linewidth=1.1, zorder=0))
            elif tipo == "diagrama":
                dibujar_diagrama(ax, x, y, extra["alto"])

        ax.plot([MARGEN_X, ANCHO - MARGEN_X], [0.58, 0.58], color="#D7DEE8", lw=0.8)
        ax.text(MARGEN_X, 0.42, "Tópicos de Big Data · Metodología de las proyecciones de esperanza de vida",
                fontsize=7.5, color=GRIS, va="center")
        ax.text(ANCHO - MARGEN_X, 0.42, "Página %d de %d" % (numero, len(paginas)),
                fontsize=7.5, color=GRIS, ha="right", va="center")

        pdf.savefig(fig)
        if VISTA_PREVIA:
            fig.savefig(os.path.join(VISTA_PREVIA, "pag_%d.png" % numero), dpi=110)
        plt.close(fig)

print("PDF generado:", SALIDA, "| páginas:", len(paginas))
