# -*- coding: utf-8 -*-
"""Genera el documento de entrega sobre el modelo de proyeccion de esperanza
de vida que publica Our World in Data. Formato de reporte escolar:
portada, desarrollo y referencias. Solo usa matplotlib."""
import os
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.backends.backend_pdf import PdfPages

NEGRO = "#111111"
GRIS = "#555555"
AZUL = "#1F3864"

ANCHO, ALTO = 8.27, 11.69
MARGEN_X, MARGEN_SUP, MARGEN_INF = 1.0, 1.0, 0.95
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


def encabezado(contenido, tam=12):
    _hueco(0.7)
    espacio(0.16)
    texto(contenido, MARGEN_X, cursor[0], fontsize=tam, color=AZUL, weight="bold", va="top")
    cursor[0] -= 0.33


def parrafo(contenido, tam=10.5, color=NEGRO, ancho=92, interlinea=0.205, sangria=0.0):
    lineas = []
    for bloque in contenido.strip().split("\n"):
        lineas.extend(textwrap.wrap(bloque.strip(), ancho) or [""])
    for i, linea in enumerate(lineas):
        _hueco(0.24)
        x = MARGEN_X + (sangria if i == 0 else 0.0)
        texto(linea, x, cursor[0], fontsize=tam, color=color, va="top")
        cursor[0] -= interlinea
    cursor[0] -= 0.10


def lista(contenido, tam=10.5, marca="•", ancho=88):
    lineas = textwrap.wrap(contenido.strip(), ancho)
    for i, linea in enumerate(lineas):
        _hueco(0.24)
        if i == 0:
            texto(marca, MARGEN_X + 0.12, cursor[0], fontsize=tam, color=NEGRO, va="top")
        texto(linea, MARGEN_X + 0.36, cursor[0], fontsize=tam, color=NEGRO, va="top")
        cursor[0] -= 0.205
    cursor[0] -= 0.06


def referencia(contenido, tam=10, ancho=92):
    lineas = textwrap.wrap(contenido.strip(), ancho)
    for i, linea in enumerate(lineas):
        _hueco(0.24)
        x = MARGEN_X + (0.0 if i == 0 else 0.30)
        texto(linea, x, cursor[0], fontsize=tam, color=NEGRO, va="top")
        cursor[0] -= 0.195
    cursor[0] -= 0.08


def figura_esquema(alto=2.3):
    _hueco(alto + 0.15)
    pagina.append(("esquema", None, MARGEN_X, cursor[0], {"alto": alto}))
    cursor[0] -= alto + 0.15


# =============================================================== PORTADA
texto("Instituto · Ingeniería en Sistemas Computacionales", ANCHO / 2, ALTO - 2.2,
      fontsize=11, color=GRIS, ha="center", va="top")
texto("Tópicos de Big Data", ANCHO / 2, ALTO - 2.5, fontsize=12, color=GRIS, ha="center", va="top")

pagina.append(("linea", None, MARGEN_X + 1.2, ALTO - 3.35, {"ancho": ANCHO_UTIL - 2.4}))

for i, linea in enumerate(["El modelo que utiliza Our World in Data",
                           "para proyectar la esperanza de vida", "hasta el año 2100"]):
    texto(linea, ANCHO / 2, ALTO - 3.8 - i * 0.42, fontsize=19, color=AZUL,
          weight="bold", ha="center", va="top")

texto("Investigación documental", ANCHO / 2, ALTO - 5.35, fontsize=11.5, color=GRIS,
      ha="center", va="top")
pagina.append(("linea", None, MARGEN_X + 1.2, ALTO - 5.75, {"ancho": ANCHO_UTIL - 2.4}))

texto("Alumno: Diego Gael Tierra", ANCHO / 2, ALTO - 6.6, fontsize=12, color=NEGRO,
      ha="center", va="top")
texto("Unidad 3 · Modelos de regresión y proyecciones demográficas", ANCHO / 2, ALTO - 6.95,
      fontsize=11, color=GRIS, ha="center", va="top")
texto("Octubre de 2026", ANCHO / 2, ALTO - 7.3, fontsize=11, color=GRIS, ha="center", va="top")

nueva_pagina()

# =============================================================== CONTENIDO
encabezado("1. Introducción", tam=13)
parrafo(
    "En la práctica de la unidad trabajamos con el conjunto de datos de nacimientos y defunciones de Our "
    "World in Data y construimos tres modelos de regresión para proyectar valores hasta el año 2100. Al "
    "comparar nuestras proyecciones con la línea que publica el propio sitio aparecieron diferencias "
    "grandes, y de ahí surgió la pregunta de esta investigación: qué modelo usa Our World in Data para "
    "proyectar la esperanza de vida hasta 2100.")
parrafo(
    "Para responderla revisé la ficha técnica de los indicadores publicados por el sitio, la documentación "
    "de la fuente original y los artículos académicos en los que se basa esa metodología. El resultado "
    "principal es que el sitio no realiza ninguna predicción propia, de modo que la pregunta se termina "
    "respondiendo con la metodología de las Naciones Unidas.")

encabezado("2. De dónde provienen los datos publicados")
parrafo(
    "Our World in Data funciona como un repositorio y un visualizador de datos: reúne información de otras "
    "instituciones, la procesa para que sea comparable entre países y la publica en gráficos interactivos. "
    "En la ficha del indicador de esperanza de vida se indica que, para los años anteriores a 1950, se "
    "utilizan la Human Mortality Database, los datos de Zijdeman y los de Riley; de 1950 en adelante se "
    "utiliza el World Population Prospects de las Naciones Unidas, en su revisión de 2024.")
parrafo(
    "El tramo futuro se publica en un gráfico aparte, titulado «Life expectancy at birth – UN WPP – with "
    "medium scenario projections», que abarca de 2024 a 2100. En la descripción de ese indicador se aclara "
    "que las proyecciones corresponden al escenario medio de las Naciones Unidas y que los valores futuros "
    "son la media de miles de trayectorias simuladas por ese organismo.")
parrafo(
    "También se menciona un detalle metodológico relevante: al ajustar el modelo de proyección, las "
    "Naciones Unidas excluyeron las esperanzas de vida observadas entre 2020 y 2023, con el fin de que el "
    "efecto temporal de la pandemia de COVID-19 no modificara la tendencia de largo plazo.")

encabezado("3. El modelo utilizado por las Naciones Unidas")
parrafo(
    "Desde 2015 la División de Población de las Naciones Unidas proyecta la fecundidad, la mortalidad y la "
    "migración con métodos probabilísticos bayesianos, desarrollados en colaboración con investigadores de "
    "la Universidad de Washington. No se trata de una regresión ajustada al año ni de un algoritmo de "
    "aprendizaje automático, sino de un modelo estadístico construido sobre teoría demográfica. El "
    "procedimiento para la esperanza de vida puede resumirse en cuatro etapas.")

figura_esquema(2.2)

encabezado("3.1 Proyección de la esperanza de vida femenina")
parrafo(
    "La primera etapa no modela la esperanza de vida directamente, sino sus ganancias de un quinquenio a "
    "otro. Esas ganancias se describen como un paseo aleatorio con deriva, donde la deriva es una función "
    "doble logística del nivel de esperanza de vida alcanzado hasta ese momento. Esta forma matemática "
    "recoge un comportamiento observado en los datos históricos: la esperanza de vida mejora lentamente en "
    "los países que parten de niveles muy bajos, mejora rápido en los niveles intermedios y vuelve a "
    "frenarse en los países que ya alcanzaron valores altos.")
parrafo(
    "El modelo es jerárquico porque los parámetros de cada país se estiman con su propia historia, pero al "
    "mismo tiempo se acercan a una media mundial. Gracias a eso, un país con pocos registros aprovecha el "
    "patrón observado en los demás. La estimación se realiza con cadenas de Markov Monte Carlo, un "
    "procedimiento de simulación que no entrega un solo resultado, sino miles de trayectorias posibles "
    "para cada país.")

encabezado("3.2 Proyección de la esperanza de vida masculina")
parrafo(
    "La esperanza de vida de los hombres no se proyecta de forma independiente. Primero se proyecta la "
    "femenina y después se modela la diferencia entre ambos sexos, de manera conjunta, para evitar que las "
    "dos series se crucen de forma poco realista. El estudio en el que se basa este paso encontró que esa "
    "brecha tiende a crecer mientras la esperanza de vida femenina se mantiene por debajo de los 75 años y "
    "a reducirse cuando supera ese nivel.")

encabezado("3.3 Conversión en tasas de mortalidad por edad")
parrafo(
    "Para proyectar una población no basta con la esperanza de vida: se necesitan las tasas de mortalidad "
    "de cada grupo de edad y sexo. Para obtenerlas se emplea una versión modificada del método Lee-Carter, "
    "propuesto originalmente en 1992, cuya expresión básica es log m(x,t) = a(x) + b(x) k(t) + e(x,t), "
    "donde m(x,t) es la tasa de mortalidad a la edad x en el año t, a(x) describe el patrón de mortalidad "
    "por edad, b(x) la velocidad con que cambia cada edad y k(t) un índice que resume el nivel de "
    "mortalidad en el tiempo.")
parrafo(
    "La diferencia con el método original está en que el índice k(t) no se proyecta por su cuenta, sino "
    "que se ajusta para reproducir las trayectorias de esperanza de vida obtenidas en la etapa anterior. "
    "Además se aplican dos variantes: una coherente, que obliga a que los parámetros de hombres y mujeres "
    "no se separen indefinidamente, y una rotada, que reconoce que cuando la mortalidad ya es baja las "
    "mejoras se concentran en las edades avanzadas.")

encabezado("3.4 El escenario medio y la incertidumbre")
parrafo(
    "Las Naciones Unidas definen el escenario medio como la media de la fecundidad y la mortalidad —y la "
    "mediana de la migración neta— de varios miles de trayectorias distintas generadas por el modelo "
    "probabilístico. Los intervalos de predicción del 80 % y del 95 % que acompañan a la publicación "
    "representan la dispersión de esas trayectorias, es decir, la incertidumbre de la proyección.")
parrafo(
    "Por esa razón, la línea que aparece en el gráfico de Our World in Data no debe leerse como un "
    "pronóstico exacto, sino como el centro de un conjunto amplio de escenarios posibles. El mismo "
    "organismo publica además variantes alta, baja, de fecundidad constante, de mortalidad constante y de "
    "migración cero, que sirven para comparar supuestos y no para anticipar lo que ocurrirá.")

encabezado("4. Comparación con los modelos de la práctica", tam=13)
parrafo(
    "En la práctica de la unidad entrenamos tres modelos usando únicamente el año como variable "
    "predictora: una regresión lineal, una regresión polinomial de grado 2 y un Random Forest. Comparar "
    "esos modelos con el procedimiento de las Naciones Unidas ayuda a entender por qué los resultados "
    "fueron tan distintos.")
lista("Nuestros modelos aprenden una forma matemática a partir de pares de año y valor. El modelo "
      "demográfico incorpora información adicional: tablas de vida, estructura por edad y sexo, y el "
      "comportamiento histórico de todos los países al mismo tiempo.")
lista("Nuestros modelos entregan un único número por año, mientras que el procedimiento de las Naciones "
      "Unidas entrega una distribución completa de trayectorias, de la cual se resumen después la línea "
      "central y los intervalos de confianza.")
lista("Nuestros modelos no distinguen entre un resultado posible y uno imposible. La regresión polinomial "
      "llegaba a predecir un número negativo de nacimientos para el año 2100, algo que no tiene sentido "
      "demográfico.")
lista("El Random Forest no extrapola: a partir del último año de entrenamiento repite siempre el mismo "
      "valor. El modelo demográfico sí extrapola, pero lo hace apoyándose en la experiencia de países que "
      "ya atravesaron niveles similares de esperanza de vida.")

encabezado("5. Conclusiones")
parrafo(
    "Our World in Data no construye un modelo de predicción propio para la esperanza de vida: publica las "
    "proyecciones del World Population Prospects 2024 de las Naciones Unidas, en su escenario medio. La "
    "metodología detrás de esas cifras combina un modelo jerárquico bayesiano para la esperanza de vida "
    "femenina, un modelo de la brecha entre sexos para la masculina y una versión modificada del método "
    "Lee-Carter para obtener las tasas de mortalidad por edad.")
parrafo(
    "De esta investigación me quedan tres ideas para la discusión en clase. La primera es que conviene "
    "presentar siempre la proyección junto con su intervalo de incertidumbre, porque el escenario medio "
    "suele interpretarse como un pronóstico seguro. La segunda es que la decisión de excluir los años de "
    "la pandemia al ajustar el modelo es discutible: evita que un episodio excepcional marque una "
    "tendencia de ochenta años, pero da por hecho que sus efectos son temporales. La tercera es que la "
    "idea de estimar cada país apoyándose en el resto equivale, en términos de aprendizaje automático, a "
    "la regularización o a la transferencia de aprendizaje, lo que muestra que ambos campos resuelven el "
    "mismo problema con nombres distintos.")

encabezado("6. Referencias")
referencia("Lee, R. y Carter, L. (1992). Modeling and Forecasting U.S. Mortality. Journal of the American "
           "Statistical Association, 87(419), 659-671.")
referencia("Naciones Unidas, Departamento de Asuntos Económicos y Sociales, División de Población (2024). "
           "World Population Prospects 2024: Methodology report. Recuperado de "
           "https://www.un.org/development/desa/pd/content/world-population-prospects-2024-methodology-report")
referencia("Naciones Unidas, División de Población (2024). Definition of projection scenarios. World "
           "Population Prospects 2024. Recuperado de "
           "https://population.un.org/wpp/definition-of-projection-scenarios")
referencia("Our World in Data (2025). Life expectancy. Recuperado de "
           "https://ourworldindata.org/grapher/life-expectancy")
referencia("Our World in Data (2025). Life expectancy at birth, UN WPP, with medium scenario projections. "
           "Recuperado de https://ourworldindata.org/grapher/future-life-expectancy-projections")
referencia("Raftery, A., Chunn, J., Gerland, P. y Ševčíková, H. (2013). Bayesian Probabilistic Projections "
           "of Life Expectancy for All Countries. Demography, 50(3), 777-801.")
referencia("Raftery, A., Lalic, N. y Gerland, P. (2014). Joint probabilistic projection of female and male "
           "life expectancy. Demographic Research, 30(27), 795-822.")
referencia("Ševčíková, H., Li, N., Kantorová, V., Gerland, P. y Raftery, A. (2016). Age-Specific Mortality "
           "and Fertility Rates for Probabilistic Population Projections. Recuperado de "
           "https://arxiv.org/abs/1503.05215")

nueva_pagina()
if pagina:
    paginas.append(pagina)


# ---------------------------------------------------------------- esquema
def dibujar_esquema(ax, x, y_top, alto):
    pasos = [
        "1. Datos históricos de mortalidad por país",
        "2. Modelo jerárquico bayesiano: esperanza de vida femenina",
        "3. Modelo de la brecha entre sexos: esperanza de vida masculina",
        "4. Método Lee-Carter modificado: tasas de mortalidad por edad",
        "5. Miles de trayectorias; el escenario medio es su promedio",
    ]
    alto_caja = 0.36
    sep = 0.09
    for i, etiqueta in enumerate(pasos):
        py = y_top - alto_caja - i * (alto_caja + sep)
        color_fondo = "#EDF1F7" if i < 4 else AZUL
        color_texto = NEGRO if i < 4 else "white"
        ax.add_patch(Rectangle((x + 0.35, py), ANCHO_UTIL - 0.7, alto_caja, facecolor=color_fondo,
                               edgecolor="#9AA7BD" if i < 4 else AZUL, linewidth=0.9, zorder=1))
        ax.text(x + ANCHO_UTIL / 2, py + alto_caja / 2, etiqueta, fontsize=9.5, color=color_texto,
                ha="center", va="center", zorder=2)
        if i < len(pasos) - 1:
            ax.annotate("", xy=(x + ANCHO_UTIL / 2, py - sep + 0.01), xytext=(x + ANCHO_UTIL / 2, py),
                        arrowprops=dict(arrowstyle="-|>", color="#6B7A90", lw=1.0, shrinkA=0, shrinkB=0))

    ax.text(x + ANCHO_UTIL / 2, y_top - alto + 0.02,
            "Figura 1. Etapas del procedimiento de proyección de las Naciones Unidas.",
            fontsize=9, color=GRIS, ha="center", va="top", style="italic")


SALIDA = sys.argv[1] if len(sys.argv) > 1 else "reports/Investigacion_esperanza_de_vida_OWID.pdf"
os.makedirs(os.path.dirname(SALIDA) or ".", exist_ok=True)
VISTA = os.environ.get("VISTA_PREVIA")

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
                ax.plot([x, x + extra["ancho"]], [y, y], color="#9AA7BD", lw=0.9)
            elif tipo == "esquema":
                dibujar_esquema(ax, x, y, extra["alto"])

        if numero > 1:
            ax.text(ANCHO - MARGEN_X, 0.55, str(numero - 1), fontsize=10, color=GRIS,
                    ha="right", va="center")
        pdf.savefig(fig)
        if VISTA:
            fig.savefig(os.path.join(VISTA, "doc_%d.png" % numero), dpi=110)
        plt.close(fig)

print("Documento generado:", SALIDA, "| páginas:", len(paginas))
