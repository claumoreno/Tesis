# -*- coding: utf-8 -*-
"""
ETAPA 7. Entregables.

- output/resultados_red.xlsx (todas las tablas en hojas separadas + diccionario)
- output/gephi/red_empresas_FY####.gexf (un archivo por año)
- output/graficos/red_2010.png, red_2024.png, evolucion_cohesion.png, evolucion_politicos.png
- output/README.md (plantilla + diccionario de variables)
"""

import pickle
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

from diccionario import D

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
INT = OUT / "intermedios"
GEXF = OUT / "gephi"
FIG = OUT / "graficos"
GEXF.mkdir(exist_ok=True)
FIG.mkdir(exist_ok=True)

# Paleta (validada para daltonismo en la guía de visualización usada)
AZUL = "#2a78d6"      # empresa sin director político
NARANJO = "#eb6834"   # empresa con director político
GRIS_ENLACE = "#b9b8b3"
TEXTO = "#0b0b0b"
TEXTO_2 = "#52514e"

pe = pd.read_csv(OUT / "panel_red_empresa_anio.csv", encoding="utf-8-sig")
pdr = pd.read_csv(OUT / "panel_red_director_anio.csv", encoding="utf-8-sig", dtype={"id_director": str})
coh = pd.read_csv(OUT / "cohesion_por_anio.csv", encoding="utf-8-sig")
comp = pd.read_csv(OUT / "comparacion_politicos_vs_no_politicos.csv", encoding="utf-8-sig")
diag = pd.read_csv(OUT / "diagnostico.csv", encoding="utf-8-sig")
diag_c = pd.read_csv(OUT / "diagnostico_cruce.csv", encoding="utf-8-sig")
prob = pd.read_csv(OUT / "problemas_base.csv", encoding="utf-8-sig")
val_f = pd.read_csv(OUT / "validacion_funciones.csv", encoding="utf-8-sig")
val_p = pd.read_csv(OUT / "validacion_panel.csv", encoding="utf-8-sig")
cargas = pd.read_csv(INT / "indice_cohesion_cargas.csv", encoding="utf-8-sig")
dic = pd.DataFrame(D)
with open(INT / "grafos_por_anio.pkl", "rb") as f:
    grafos = pickle.load(f)

# ---------------------------------------------------------------------------
# 1. Excel
# ---------------------------------------------------------------------------
hojas = [
    ("Indice", pd.DataFrame([
        ("Diagnostico", "Etapa 1. Conteos por año (empresas, directores, interlocks, políticos)"),
        ("Diagnostico_cruce", "Etapa 1. Limpieza y verificación del cruce de políticos"),
        ("Problemas_base", "Casos de la base que conviene revisar"),
        ("Cohesion_por_anio", "Etapa 3. Cohesión global de la red de empresas, una fila por año"),
        ("Indice_cohesion_cargas", "Cargas del índice de cohesión por componentes principales"),
        ("Panel_empresa_anio", "Etapas 2, 4 y 5. Panel empresa-año (para unir con datos financieros)"),
        ("Panel_director_anio", "Etapas 2 y 4. Panel director-año"),
        ("Comparacion_politicos", "Etapa 5. Centralidad de políticos vs no políticos"),
        ("Validacion_funciones", "Etapa 6. Ejemplos del material de Cárdenas"),
        ("Validacion_panel", "Etapa 6. Verificaciones sobre la base real"),
        ("Diccionario", "Definición, fórmula, lectura y sección del material de cada variable"),
    ], columns=["hoja", "contenido"])),
    ("Diagnostico", diag), ("Diagnostico_cruce", diag_c), ("Problemas_base", prob),
    ("Cohesion_por_anio", coh), ("Indice_cohesion_cargas", cargas),
    ("Panel_empresa_anio", pe), ("Panel_director_anio", pdr),
    ("Comparacion_politicos", comp), ("Validacion_funciones", val_f),
    ("Validacion_panel", val_p), ("Diccionario", dic),
]
with pd.ExcelWriter(OUT / "resultados_red.xlsx", engine="openpyxl") as xw:
    for nombre, df in hojas:
        df.to_excel(xw, sheet_name=nombre, index=False)
        ws = xw.sheets[nombre]
        for c in ws[1]:
            c.font = Font(bold=True, color="FFFFFF")
            c.fill = PatternFill("solid", fgColor="2A78D6")
            c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.freeze_panes = "A2"
        ws.auto_filter.ref = ws.dimensions
        for i, col in enumerate(df.columns, start=1):
            largo = max([len(str(col))] + [len(str(x)) for x in df[col].head(200)])
            ws.column_dimensions[get_column_letter(i)].width = min(max(10, largo + 2), 60)
print("Excel listo")

# ---------------------------------------------------------------------------
# 2. Gephi (.gexf): nodos = empresas, color según director político, tamaño según grado
# ---------------------------------------------------------------------------
def hex_rgb(h):
    h = h.lstrip("#")
    return {"r": int(h[0:2], 16), "g": int(h[2:4], 16), "b": int(h[4:6], 16), "a": 1.0}


cols_gexf = ["company_name", "n_directores", "n_politicos", "pct_politicos", "tiene_politico",
             "pct_mujeres", "grado", "grado_ponderado", "intermediacion_norm",
             "cercania_armonica_norm", "eigenvector_comp_principal", "punto_corte",
             "en_comp_principal", "n_vecinos_con_politico", "puente_politico", "empresa_deslistada"]
for anio, d in grafos.items():
    g = d["empresas"].copy()
    attrs = d["atributos_empresas"].set_index("firm_iden")
    pos = nx.spring_layout(g, seed=42, k=0.35, iterations=200)
    for nodo in g.nodes():
        a = attrs.loc[nodo]
        g.nodes[nodo].clear()
        g.nodes[nodo]["label"] = a["company_name"]
        for c in cols_gexf[1:]:
            val = a[c]
            if pd.notna(val):            # los vacíos se omiten (no se rellenan)
                g.nodes[nodo][c] = float(val) if isinstance(val, (float, np.floating)) else int(val)
        g.nodes[nodo]["viz"] = {
            "color": hex_rgb(NARANJO if a["tiene_politico"] == 1 else AZUL),
            "size": float(4 + 2 * a["grado"]),
            "position": {"x": float(pos[nodo][0] * 1000), "y": float(pos[nodo][1] * 1000), "z": 0.0},
        }
    for u, v_, e in g.edges(data=True):
        e["weight"] = float(e["weight"])
    nx.write_gexf(g, GEXF / f"red_empresas_FY{anio}.gexf")
print("GEXF listos")

# ---------------------------------------------------------------------------
# 3. Gráficos
# ---------------------------------------------------------------------------
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.edgecolor": "#d0cfca",
                     "axes.labelcolor": TEXTO_2, "xtick.color": TEXTO_2, "ytick.color": TEXTO_2,
                     "axes.spines.top": False, "axes.spines.right": False})


def dibujar_red(anio, archivo):
    d = grafos[anio]
    g = d["empresas"]
    a = d["atributos_empresas"].set_index("firm_iden")
    aislados = sorted(n for n in g.nodes() if g.degree(n) == 0)
    comps = sorted((c for c in nx.connected_components(g) if len(c) > 1), key=len, reverse=True)
    principal, otros = comps[0], comps[1:]
    conectados = g.subgraph([n for n in g.nodes() if g.degree(n) > 0])
    # componente principal al centro (spring layout, semilla fija)
    pos = nx.spring_layout(g.subgraph(principal), seed=7, k=0.12, iterations=500)
    xs = np.array([p[0] for p in pos.values()])
    ys = np.array([p[1] for p in pos.values()])
    x0, x1 = xs.min(), xs.max()
    # componentes pequeños en una fila bajo el componente principal
    y_comp = ys.min() - 0.18
    paso = (x1 - x0) / max(len(otros), 1)
    for i, c in enumerate(otros):
        sub = nx.spring_layout(g.subgraph(c), seed=1, scale=0.035 * np.sqrt(len(c)))
        cx = x0 + paso * (i + 0.5)
        for n, p in sub.items():
            pos[n] = np.array([cx + p[0], y_comp + p[1]])
    # aislados en dos filas al fondo
    y0 = y_comp - 0.17
    ancho = np.linspace(x0, x1, max((len(aislados) + 1) // 2, 2))
    for i, n in enumerate(aislados):
        pos[n] = np.array([ancho[i // 2] + (0.5 * (ancho[1] - ancho[0]) if i % 2 else 0), y0 - 0.05 * (i % 2)])
    fig, ax = plt.subplots(figsize=(13, 11), dpi=150)
    pesos = [conectados[u][v]["weight"] for u, v in conectados.edges()]
    nx.draw_networkx_edges(conectados, pos, ax=ax, edge_color=GRIS_ENLACE,
                           width=[0.5 + 0.7 * (w - 1) for w in pesos], alpha=0.8)
    for valor, color, etiqueta in [(0, AZUL, "Sin director político"), (1, NARANJO, "Con director político")]:
        ns = [n for n in g.nodes() if a.loc[n, "tiene_politico"] == valor]
        nx.draw_networkx_nodes(g, pos, nodelist=ns, ax=ax, node_color=color,
                               node_size=[25 + 22 * a.loc[n, "grado"] for n in ns],
                               edgecolors="white", linewidths=1.0, label=etiqueta)
    top = a.sort_values("intermediacion_norm", ascending=False).head(12).index
    etiquetas = {n: n.split(".")[0] for n in top}
    nx.draw_networkx_labels(g, pos, labels=etiquetas, ax=ax, font_size=8, font_color=TEXTO,
                            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.75))
    ax.text(x0, y_comp + 0.08, f"Otros componentes ({len(otros)})", fontsize=9, color=TEXTO_2)
    ax.text(x0, y0 + 0.05, f"Empresas aisladas ({len(aislados)})", fontsize=9, color=TEXTO_2)
    fila = coh[coh["anio"] == anio].iloc[0]
    ax.set_title(f"Red de empresas por directores compartidos, FY{anio}\n"
                 f"n = {int(fila.n_nodos)} empresas, L = {int(fila.n_enlaces)} enlaces, "
                 f"densidad = {fila.densidad:.3f}, grado medio = {fila.grado_medio:.2f}, "
                 f"{fila.pct_comp_principal:.1f}% en el componente principal",
                 fontsize=12, color=TEXTO, loc="left")
    ax.legend(loc="upper left", frameon=False, fontsize=10, markerscale=0.6)
    ax.text(0.99, 0.01, "Tamaño = grado. Grosor del enlace = n° de directores compartidos.\n"
            "Etiquetas: 12 empresas con mayor intermediación.", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=8, color=TEXTO_2)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(FIG / archivo, dpi=150, facecolor="white")
    plt.close(fig)


dibujar_red(2010, "red_2010.png")
dibujar_red(2024, "red_2024.png")

# evolución de la cohesión: múltiplos pequeños, un eje por indicador
paneles = [("n_nodos", "N° de empresas (n)"), ("n_enlaces", "N° de enlaces (L)"),
           ("densidad", "Densidad"), ("grado_medio", "Grado medio (2L/n)"),
           ("pct_comp_principal", "% en componente principal"), ("pct_aislados", "% de aislados"),
           ("conectividad", "Conectividad"), ("compacidad", "Compacidad"),
           ("distancia_media_comp_principal", "Distancia media (comp. principal)"),
           ("centralizacion_grado", "Centralización de grado"),
           ("pct_puntos_corte", "% de puntos de corte"), ("indice_cohesion_acp", "Índice de cohesión (ACP)")]
fig, axs = plt.subplots(4, 3, figsize=(13, 13), dpi=150, sharex=True)
for ax, (col, titulo) in zip(axs.flat, paneles):
    ax.plot(coh["anio"], coh[col], color=AZUL, lw=2, marker="o", ms=4)
    ax.set_title(titulo, fontsize=10, color=TEXTO, loc="left")
    ax.grid(axis="y", color="#ecebe7", lw=0.8)
    ax.tick_params(labelsize=8)
    for i in [0, len(coh) - 1]:
        v = coh[col].iloc[i]
        ax.annotate(f"{v:.3g}", (coh["anio"].iloc[i], v), textcoords="offset points",
                    xytext=(0, 7), ha="center", fontsize=8, color=TEXTO_2)
    ax.margins(y=0.2)
for ax in axs[-1]:
    ax.set_xticks(range(2010, 2025, 2))
fig.suptitle("Evolución de la cohesión de la red de empresas, FY2010–FY2024 (red dicotomizada)",
             fontsize=13, color=TEXTO, x=0.01, ha="left")
fig.tight_layout(rect=(0, 0, 1, 0.97))
fig.savefig(FIG / "evolucion_cohesion.png", dpi=150, facecolor="white")
plt.close(fig)

# evolución de la presencia política en la red
fig, axs = plt.subplots(1, 2, figsize=(12, 4.2), dpi=150)
for ax, (col, titulo) in zip(axs, [("pct_empresas_con_politico", "% de empresas con director político"),
                                   ("pct_enlaces_via_politico", "% de enlaces que pasan por un director político")]):
    ax.plot(coh["anio"], coh[col], color=NARANJO, lw=2, marker="o", ms=4)
    ax.set_title(titulo, fontsize=10, color=TEXTO, loc="left")
    ax.grid(axis="y", color="#ecebe7", lw=0.8)
    ax.set_ylim(0, max(40, coh[col].max() * 1.2))
    ax.set_xticks(range(2010, 2025, 2))
fig.tight_layout()
fig.savefig(FIG / "evolucion_politicos.png", dpi=150, facecolor="white")
plt.close(fig)
print("Gráficos listos")

# ---------------------------------------------------------------------------
# 4. README (plantilla + diccionario)
# ---------------------------------------------------------------------------
partes = []
for tabla, sub in dic.groupby("tabla", sort=False):
    partes.append(f"\n### `{tabla}.csv`\n")
    partes.append("| Variable | Definición | Fórmula | Cómo se lee | Material |")
    partes.append("|---|---|---|---|---|")
    for _, r in sub.iterrows():
        celdas = [f"`{r.variable}`", r.definicion, r.formula, r.como_se_lee, r.seccion_material]
        partes.append("| " + " | ".join(str(c).replace("|", "\\|") for c in celdas) + " |")
plantilla = (Path(__file__).parent / "plantilla_readme.md").read_text(encoding="utf-8")
carga_txt = ", ".join(f"{r.indicador} {r.carga_componente_1:+.2f}" for r in cargas.itertuples())
readme = (plantilla.replace("{{DICCIONARIO}}", "\n".join(partes))
          .replace("{{VAR_ACP}}", f"{cargas['varianza_explicada_componente_1'].iloc[0]:.1%}")
          .replace("{{CARGAS_ACP}}", carga_txt))
(OUT / "README.md").write_text(readme, encoding="utf-8")
print("README listo")
