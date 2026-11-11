# -*- coding: utf-8 -*-
"""
ETAPAS 2 a 5. Construcción de la red por año e indicadores.

ETAPA 2. Para cada año FY2010-FY2024:
  - matriz de 2 modos director x empresa;
  - proyección empresa x empresa (valor = n° de directores compartidos);
  - proyección director x director (comparten al menos un directorio);
  - atributos de empresas y directores.
ETAPA 3. Cohesión global de la red de empresas (una fila por año).
ETAPA 4. Centralidad por empresa-año y por director-año.
ETAPA 5. Variables políticas de red y comparación políticos vs no políticos.

Entrada: output/intermedios/board_limpio.csv (generado por 01_limpieza_diagnostico.py)
Salidas: ver la lista al final del script.
"""

import pickle
from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

import red_funciones as rf

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
INT = OUT / "intermedios"
RED = OUT / "redes_por_anio"
RED.mkdir(parents=True, exist_ok=True)

NIV = ["N11", "N12", "N21", "N22"]

b = pd.read_csv(INT / "board_limpio.csv", encoding="utf-8-sig", dtype={"id_director": str})
anios = sorted(b["anio"].unique())

cohesion, panel_emp, panel_dir, grafos = [], [], [], {}

for anio in anios:
    x = b[b["anio"] == anio].copy()
    fy = f"FY{anio}"

    # ------------------------------------------------------------------
    # ETAPA 2. Matriz de 2 modos y proyecciones
    # ------------------------------------------------------------------
    m2 = rf.matriz_dos_modos(x)                      # directores x empresas
    emp_val, dir_val = rf.proyectar(m2)              # con diagonal (se documenta)
    g_emp = rf.grafo_desde_matriz(emp_val)           # diagonal ignorada, peso = intensidad
    g_dir = rf.grafo_desde_matriz(dir_val)

    # directores políticos del año y proyección SOLO con ellos (puentes políticos)
    attr_dir = x.drop_duplicates("id_director").set_index("id_director")
    pol = attr_dir.loc[m2.index, "politico"].values
    a = m2.values
    a_pol = a[pol == 1]
    w_pol = a_pol.T @ a_pol
    np.fill_diagonal(w_pol, 0)
    empresas = list(m2.columns)
    idx = {e: i for i, e in enumerate(empresas)}

    # guardar matrices y listas de enlaces del año
    m2.to_csv(RED / f"matriz_2modos_director_empresa_{fy}.csv", encoding="utf-8-sig")
    emp_val.to_csv(RED / f"matriz_empresa_empresa_valorada_{fy}.csv", encoding="utf-8-sig")
    enl = pd.DataFrame([(u, v, d["weight"], int(w_pol[idx[u], idx[v]]))
                        for u, v, d in g_emp.edges(data=True)],
                       columns=["empresa_1", "empresa_2", "directores_compartidos",
                                "directores_politicos_compartidos"])
    enl.to_csv(RED / f"enlaces_empresa_empresa_{fy}.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame([(u, v, d["weight"]) for u, v, d in g_dir.edges(data=True)],
                 columns=["director_1", "director_2", "directorios_compartidos"]
                 ).to_csv(RED / f"enlaces_director_director_{fy}.csv", index=False, encoding="utf-8-sig")

    # ------------------------------------------------------------------
    # Atributos de empresa
    # ------------------------------------------------------------------
    ae = x.groupby("firm_iden").agg(
        company_name=("company_name", "first"),
        empresa_deslistada=("empresa_deslistada", "first"),
        n_directores=("id_director", "nunique"),
        n_directores_sin_rut=("sin_rut", "sum"),
        n_directores_interlock=("n_directorios", lambda s: int((s >= 2).sum())),
        n_politicos=("politico", "sum"),
        **{f"n_politicos_{n}": (f"politico_{n}", "sum") for n in NIV},
        n_mujeres=("gender", lambda s: int((s == "F").sum())),
        n_genero_informado=("gender", lambda s: int(s.notna().sum())),
    )
    ae["pct_politicos"] = 100 * ae["n_politicos"] / ae["n_directores"]
    ae["tiene_politico"] = (ae["n_politicos"] > 0).astype(int)
    for n in NIV:
        ae[f"tiene_politico_{n}"] = (ae[f"n_politicos_{n}"] > 0).astype(int)
    ae["pct_mujeres"] = 100 * ae["n_mujeres"] / ae["n_genero_informado"]
    nx.set_node_attributes(g_emp, ae["tiene_politico"].to_dict(), "tiene_politico")

    # ------------------------------------------------------------------
    # ETAPA 3. Cohesión global
    # ------------------------------------------------------------------
    coh = {"fiscal_year": fy, "anio": anio}
    coh.update(rf.cohesion_global(g_emp))
    # resumen de la red director x director (contexto)
    gdb = rf.binaria(g_dir)
    coh.update({
        "red_dir_n_nodos": gdb.number_of_nodes(),
        "red_dir_n_enlaces": gdb.number_of_edges(),
        "red_dir_densidad": rf.densidad(gdb.number_of_nodes(), gdb.number_of_edges()),
        "red_dir_grado_medio": rf.grado_medio(gdb.number_of_nodes(), gdb.number_of_edges()),
        "red_dir_pct_comp_principal": 100 * len(rf.componente_principal(gdb)) / gdb.number_of_nodes(),
    })
    # contexto político del año
    coh["n_empresas_con_politico"] = int(ae["tiene_politico"].sum())
    coh["pct_empresas_con_politico"] = 100 * ae["tiene_politico"].mean()
    coh["n_enlaces_via_politico"] = int((np.triu(w_pol, 1) > 0).sum())
    coh["pct_enlaces_via_politico"] = (100 * coh["n_enlaces_via_politico"] / coh["n_enlaces"]
                                       if coh["n_enlaces"] else np.nan)
    cohesion.append(coh)

    # ------------------------------------------------------------------
    # ETAPA 4. Centralidad por empresa-año
    # ------------------------------------------------------------------
    cen = rf.centralidad_nodos(g_emp).set_index("nodo")
    cen.index.name = "firm_iden"

    # ------------------------------------------------------------------
    # ETAPA 5. Variables políticas de red por empresa-año
    # ------------------------------------------------------------------
    gb = rf.binaria(g_emp)
    dist = rf.distancias_todas(gb)
    pol_emp = set(ae.index[ae["tiene_politico"] == 1])
    filas = []
    for e in empresas:
        vec = list(gb.neighbors(e))
        n_vec_pol = sum(1 for v in vec if v in pol_emp)
        d_otros = [d for v, d in dist[e].items() if v in pol_emp and v != e]
        i = idx[e]
        vec_via_pol = [v for v in vec if w_pol[i, idx[v]] > 0]
        vec_solo_pol = [v for v in vec_via_pol if w_pol[i, idx[v]] == g_emp[e][v]["weight"]]
        filas.append({
            "firm_iden": e,
            "n_vecinos_con_politico": n_vec_pol,
            "pct_vecinos_con_politico": 100 * n_vec_pol / len(vec) if vec else np.nan,
            "dist_min_empresa_con_politico": min(d_otros) if d_otros else np.nan,
            "puente_politico": int(len(vec_via_pol) > 0),
            "n_vecinos_via_politico": len(vec_via_pol),
            "n_vecinos_solo_via_politico": len(vec_solo_pol),
        })
    vp = pd.DataFrame(filas).set_index("firm_iden")

    pe = ae.join(cen).join(vp).reset_index()
    pe.insert(1, "fiscal_year", fy)
    pe.insert(2, "anio", anio)
    pe["n_empresas_red_anio"] = gb.number_of_nodes()
    panel_emp.append(pe)

    # ------------------------------------------------------------------
    # ETAPA 4. Centralidad por director-año
    # ------------------------------------------------------------------
    cd = rf.centralidad_directores(g_dir).set_index("nodo")
    cd.index.name = "id_director"
    emp_de = x.groupby("id_director")["firm_iden"].apply(lambda s: "; ".join(sorted(s)))
    ch = x.groupby("id_director")["es_chairman"].max()
    ad = attr_dir[["name_director", "sin_rut", "gender", "politico"] +
                  [f"politico_{n}" for n in NIV] + ["n_directorios"]].copy()
    ad["empresas"] = emp_de
    ad["preside_algun_directorio"] = ch
    pdir = ad.join(cd).reset_index()
    pdir.insert(1, "fiscal_year", fy)
    pdir.insert(2, "anio", anio)
    panel_dir.append(pdir)

    grafos[anio] = {"empresas": g_emp, "atributos_empresas": pe}
    print(f"{fy}: {coh['n_nodos']} empresas, {coh['n_enlaces']} enlaces, "
          f"densidad {coh['densidad']:.4f}, {coh['pct_comp_principal']:.1f}% en comp. principal")

# ---------------------------------------------------------------------------
# Ensamblar tablas
# ---------------------------------------------------------------------------
coh = pd.DataFrame(cohesion)

# Índice de cohesión por componentes principales (Cárdenas 2020, sección 6.3).
# Se estandarizan los indicadores de su artículo, se extrae el primer componente
# y se orienta para que un valor más alto signifique más cohesión.
ind = ["conectividad", "densidad", "grado_medio", "ratio_componentes",
       "pct_comp_principal", "pct_aislados", "compacidad"]
z = (coh[ind] - coh[ind].mean()) / coh[ind].std(ddof=1)
u, s, vt = np.linalg.svd(z.values, full_matrices=False)
carga = vt[0]
if carga[ind.index("densidad")] < 0:
    carga = -carga
lam = s[0] ** 2 / (len(coh) - 1)
coh["indice_cohesion_acp"] = z.values @ carga / np.sqrt(lam)
var_exp = lam / len(ind)
pd.DataFrame({"indicador": ind, "carga_componente_1": carga}).assign(
    varianza_explicada_componente_1=var_exp).to_csv(
    INT / "indice_cohesion_cargas.csv", index=False, encoding="utf-8-sig")

pe = pd.concat(panel_emp, ignore_index=True)
orden_emp = (["firm_iden", "company_name", "fiscal_year", "anio", "empresa_deslistada",
              "n_empresas_red_anio",
              "n_directores", "n_directores_sin_rut", "n_directores_interlock",
              "n_politicos", "pct_politicos", "tiene_politico"]
             + [f"tiene_politico_{n}" for n in NIV] + [f"n_politicos_{n}" for n in NIV]
             + ["n_mujeres", "pct_mujeres",
                "grado", "grado_norm", "grado_ponderado", "intermediacion", "intermediacion_norm",
                "cercania_armonica", "cercania_armonica_norm", "eigenvector_comp_principal",
                "punto_corte", "en_comp_principal", "aislado", "tam_componente",
                "n_vecinos_con_politico", "pct_vecinos_con_politico",
                "dist_min_empresa_con_politico", "puente_politico",
                "n_vecinos_via_politico", "n_vecinos_solo_via_politico"])
pe = pe[orden_emp].sort_values(["firm_iden", "anio"]).reset_index(drop=True)

pdr = pd.concat(panel_dir, ignore_index=True).rename(
    columns={"name_director": "nombre_director", "gender": "genero"})
orden_dir = (["id_director", "nombre_director", "fiscal_year", "anio", "sin_rut", "genero",
              "politico"] + [f"politico_{n}" for n in NIV] +
             ["n_directorios", "empresas", "preside_algun_directorio",
              "grado_red_directores", "grado_norm_red_directores",
              "intermediacion_red_directores", "intermediacion_norm_red_directores"])
pdr = pdr[orden_dir].sort_values(["id_director", "anio"]).reset_index(drop=True)

# ---------------------------------------------------------------------------
# ETAPA 5. Comparación de centralidad: políticos vs no políticos
# ---------------------------------------------------------------------------
comp = []
periodos = [(f"FY{a}", [a]) for a in anios] + [("FY2010-FY2024 (pool)", anios)]
var_dir = ["n_directorios", "grado_red_directores", "intermediacion_norm_red_directores"]
var_emp = ["grado", "intermediacion_norm", "cercania_armonica_norm", "eigenvector_comp_principal"]
for etiqueta, lista in periodos:
    d = pdr[pdr["anio"].isin(lista)]
    for muestra, dd in [("todos los directores", d),
                        ("solo directores con RUT", d[d["sin_rut"] == 0])]:
        for v in var_dir:
            r = rf.comparar_grupos(dd.loc[dd["politico"] == 1, v], dd.loc[dd["politico"] == 0, v])
            comp.append({"nivel": "director", "periodo": etiqueta, "muestra": muestra,
                         "variable": v, **r})
    e = pe[pe["anio"].isin(lista)]
    for v in var_emp:
        r = rf.comparar_grupos(e.loc[e["tiene_politico"] == 1, v], e.loc[e["tiene_politico"] == 0, v])
        comp.append({"nivel": "empresa (con vs sin director político)", "periodo": etiqueta,
                     "muestra": "todas las empresas" if v != "eigenvector_comp_principal"
                     else "empresas del componente principal", "variable": v, **r})
comp = pd.DataFrame(comp)
comp["test_principal"] = "Welch t-test (varianzas distintas)"
comp["significativo_5pct_welch"] = (comp["p_welch"] < 0.05).astype("Int64")

# ---------------------------------------------------------------------------
# Guardar
# ---------------------------------------------------------------------------
pe.to_csv(OUT / "panel_red_empresa_anio.csv", index=False, encoding="utf-8-sig")
pdr.to_csv(OUT / "panel_red_director_anio.csv", index=False, encoding="utf-8-sig")
coh.to_csv(OUT / "cohesion_por_anio.csv", index=False, encoding="utf-8-sig")
comp.to_csv(OUT / "comparacion_politicos_vs_no_politicos.csv", index=False, encoding="utf-8-sig")
with open(INT / "grafos_por_anio.pkl", "wb") as f:
    pickle.dump(grafos, f)

print(f"\nPanel empresa-año: {len(pe)} filas; panel director-año: {len(pdr)} filas")
print(f"Índice de cohesión ACP: varianza explicada por el 1er componente = {var_exp:.1%}")
