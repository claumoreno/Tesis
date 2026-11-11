# -*- coding: utf-8 -*-
"""
ETAPA 1. Limpieza de la base board, cruce con directores políticos y diagnóstico.

Entradas (carpeta raíz del proyecto):
  - new_interlocking2.xlsx, hoja "board"
  - Cruce_politicos_interlocking.xlsx, hoja "Cruce"

Salidas:
  - output/intermedios/board_limpio.csv   (director-empresa-año, sin CEO, con atributos)
  - output/diagnostico.csv                 (tabla por año)
  - output/diagnostico_cruce.csv           (verificación del cruce de políticos)
  - output/problemas_base.csv              (casos de la base que conviene revisar)

Reglas de limpieza (decisiones ya tomadas por la autora, no se cambian):
  1. Se excluyen todas las filas con director = "CEO".
  2. D#/CHAIRMAN es un director normal.
  3. ID del director = RUT normalizado; si no es RUT, nombre normalizado (sin_rut = 1).
     Los sin RUT nunca son políticos.
  4. Empresas con "^" se mantienen (panel no balanceado).
  5. Se eliminan duplicados director-empresa-año.
"""

from pathlib import Path

import numpy as np
import pandas as pd

import red_funciones as rf

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
INT = OUT / "intermedios"
INT.mkdir(parents=True, exist_ok=True)

NIVELES = ["N1.1", "N1.2", "N2.1", "N2.2"]
COL_POL = "Pasado político antes del año (N1.1–N2.2)"

# ---------------------------------------------------------------------------
# 1. Lectura
# ---------------------------------------------------------------------------
board = pd.read_excel(BASE / "new_interlocking2.xlsx", sheet_name="board", dtype=str)
cruce = pd.read_excel(BASE / "Cruce_politicos_interlocking.xlsx", sheet_name="Cruce",
                      dtype={"director_iden": str})
print(f"board: {len(board)} filas; cruce: {len(cruce)} filas")

cols = ["firm_iden", "fiscal_year", "company_name", "director", "name_director",
        "director_iden", "gender"]
board = board[cols].copy()
for c in cols:
    board[c] = board[c].str.strip()          # quita espacios sobrantes (p. ej. en company_name)
board["anio"] = board["fiscal_year"].str.replace("FY", "", regex=False).astype(int)

problemas = []

# ---------------------------------------------------------------------------
# 2. Verificación del cruce contra la base completa (antes de sacar CEO)
# ---------------------------------------------------------------------------
llave = ["firm_iden", "fiscal_year", "director_iden"]
cruce["director_iden"] = cruce["director_iden"].str.strip()
ver = cruce.merge(board[llave + ["director"]], on=llave, how="left", indicator=True)
n_calzan = int((ver["_merge"] == "both").sum())
n_no_calzan = int((ver["_merge"] == "left_only").sum())
dup_cruce = cruce[cruce.duplicated(llave, keep=False)]
ceo_cruce = ver[ver["director"] == "CEO"]
for _, f in dup_cruce.iterrows():
    problemas.append({"tipo": "Fila duplicada en el cruce (mismo RUT con dos ID_persona)",
                      "firm_iden": f["firm_iden"], "fiscal_year": f["fiscal_year"],
                      "detalle": f"{f['name_director']} ({f['director_iden']}) aparece como "
                                 f"{f['ID_persona']} '{f['Político (nombre en la base)']}'. "
                                 "Se unifican niveles con el máximo (mismo RUT = misma persona)."})
for _, f in ceo_cruce.iterrows():
    problemas.append({"tipo": "Persona del cruce que es CEO (se pierde al excluir CEO)",
                      "firm_iden": f["firm_iden"], "fiscal_year": f["fiscal_year"],
                      "detalle": f"{f['name_director']} ({f['director_iden']}), pasado político = {f[COL_POL]}"})

verif = pd.DataFrame([
    ("Filas en hoja Cruce", len(cruce)),
    ("Filas del cruce que calzan con board (firm_iden + fiscal_year + director_iden)", n_calzan),
    ("Filas del cruce que NO calzan con board", n_no_calzan),
    ("Filas del cruce involucradas en duplicados (misma llave)", len(dup_cruce)),
    ("Filas únicas director-empresa-año del cruce", len(cruce.drop_duplicates(llave))),
    ("Personas distintas en el cruce (ID_persona)", cruce["ID_persona"].nunique()),
    ("RUT distintos en el cruce", cruce["director_iden"].nunique()),
    ("Filas del cruce con pasado político = 1", int((cruce[COL_POL] == 1).sum())),
    ("Filas del cruce con rol CEO (se pierden al sacar CEO)", len(ceo_cruce)),
    ("  de ellas con pasado político = 1", int((ceo_cruce[COL_POL] == 1).sum())),
    ("Filas únicas del cruce que quedan sin CEO", int(ver[ver["director"] != "CEO"].drop_duplicates(llave).shape[0])),
    ("  de ellas con pasado político = 1",
     int(ver[(ver["director"] != "CEO")].groupby(llave)[COL_POL].max().sum())),
], columns=["concepto", "valor"])

# ---------------------------------------------------------------------------
# 3. Limpieza de la base board
# ---------------------------------------------------------------------------
n_total = len(board)
fy_total = board[["firm_iden", "anio"]].drop_duplicates().shape[0]
n_ceo = int((board["director"] == "CEO").sum())
b = board[board["director"] != "CEO"].copy()                       # regla 1

# regla 3: identificador
ids = [rf.identificador_director(d, n) for d, n in zip(b["director_iden"], b["name_director"])]
b["id_director"] = [i for i, _ in ids]
b["sin_rut"] = [s for _, s in ids]
b["es_chairman"] = b["director"].str.contains("CHAIRMAN").astype(int)  # regla 2 (solo informativo)
b["empresa_deslistada"] = b["firm_iden"].str.contains(r"\^", regex=True).astype(int)  # regla 4

# casos raros de identificador
raros = b[(b["sin_rut"] == 1) & b["director_iden"].str.contains(r"\d", regex=True)]
for _, f in raros.drop_duplicates("director_iden").iterrows():
    problemas.append({"tipo": "director_iden no es RUT válido ni nombre",
                      "firm_iden": f["firm_iden"], "fiscal_year": f["fiscal_year"],
                      "detalle": f"{f['name_director']} con director_iden '{f['director_iden']}'. "
                                 "Se trata como sin RUT y se usa el nombre como ID."})
cortos = b[(b["sin_rut"] == 0) & (b["id_director"].str.len() < 8)]
for _, f in cortos.iterrows():
    problemas.append({"tipo": "RUT válido pero inusualmente bajo (6 dígitos); posible error de digitación",
                      "firm_iden": f["firm_iden"], "fiscal_year": f["fiscal_year"],
                      "detalle": f"{f['name_director']} con RUT '{f['director_iden']}'. Se mantiene tal cual."})
# nombres de empresas con espacios sobrantes
nombres = board.groupby("firm_iden")["company_name"].nunique()
# directores sin RUT con nombres parecidos (posible misma persona, no se fusionan)
import difflib
nr = sorted(b.loc[b["sin_rut"] == 1, "id_director"].unique())
for i, x in enumerate(nr):
    for y in nr[i + 1:]:
        if x.split()[-1] == y.split()[-1] and difflib.SequenceMatcher(None, x, y).ratio() >= 0.85 \
                and x[0] == y[0]:
            problemas.append({"tipo": "Directores sin RUT con nombres parecidos (no se fusionan)",
                              "firm_iden": "", "fiscal_year": "", "detalle": f"'{x}' y '{y}'"})

# regla 5: duplicados director-empresa-año
n_antes = len(b)
b = b.drop_duplicates(["firm_iden", "anio", "id_director"])
n_dup = n_antes - len(b)

# ---------------------------------------------------------------------------
# 4. Atributo político (nivel director-año)
# ---------------------------------------------------------------------------
cr = cruce.copy()
cr["id_director"] = cr["director_iden"].map(rf.normalizar_rut)
cr["anio"] = cr["Año"].astype(int)
cols_niv = {COL_POL: "politico"}
cols_niv.update({f"{n} antes del año": f"politico_{n.replace('.', '')}" for n in NIVELES})
cr = cr.rename(columns=cols_niv)
pol_vars = list(cols_niv.values())
# por empresa-año-director (unifica la fila duplicada de Mladinic con el máximo)
cr_fy = cr.groupby(["firm_iden", "anio", "id_director"], as_index=False)[pol_vars].max()
b = b.merge(cr_fy, on=["firm_iden", "anio", "id_director"], how="left")
# director-año: el pasado político es atributo de la persona en el año
pol_da = b.groupby(["id_director", "anio"])[pol_vars].max().reset_index()
b = b.drop(columns=pol_vars).merge(pol_da, on=["id_director", "anio"], how="left")
for v in pol_vars:
    b[v] = b[v].fillna(0).astype(int)
    b.loc[b["sin_rut"] == 1, v] = 0          # los sin RUT nunca son políticos
b["en_cruce"] = b.set_index(["firm_iden", "anio", "id_director"]).index.isin(
    cr_fy.set_index(["firm_iden", "anio", "id_director"]).index).astype(int)

# n° de directorios del director en el año
b["n_directorios"] = b.groupby(["id_director", "anio"])["firm_iden"].transform("nunique")

b = b.sort_values(["anio", "firm_iden", "director"]).reset_index(drop=True)
b.to_csv(INT / "board_limpio.csv", index=False, encoding="utf-8-sig")

# ---------------------------------------------------------------------------
# 5. Diagnóstico por año
# ---------------------------------------------------------------------------
da = b.drop_duplicates(["id_director", "anio"])
filas = []
for anio in sorted(b["anio"].unique()):
    x = b[b["anio"] == anio]
    d = da[da["anio"] == anio]
    emp_pol = x.groupby("firm_iden")["politico"].max()
    filas.append({
        "fiscal_year": f"FY{anio}",
        "anio": anio,
        "n_filas_sin_ceo": len(x),
        "n_empresas": x["firm_iden"].nunique(),
        "n_empresas_deslistadas_^": x.loc[x["empresa_deslistada"] == 1, "firm_iden"].nunique(),
        "n_directores": len(d),
        "n_directores_2mas_directorios": int((d["n_directorios"] >= 2).sum()),
        "n_directores_sin_rut": int((d["sin_rut"] == 1).sum()),
        "n_directores_sin_rut_2mas_directorios": int(((d["sin_rut"] == 1) & (d["n_directorios"] >= 2)).sum()),
        "n_directores_politicos": int(d["politico"].sum()),
        "n_politicos_2mas_directorios": int(((d["politico"] == 1) & (d["n_directorios"] >= 2)).sum()),
        "n_empresas_con_director_politico": int(emp_pol.sum()),
        "pct_empresas_con_director_politico": 100 * emp_pol.mean(),
        "n_directores_mujeres": int((d["gender"] == "F").sum()),
    })
diag = pd.DataFrame(filas)
tot = {"fiscal_year": "Total filas / personas distintas", "anio": np.nan,
       "n_filas_sin_ceo": len(b), "n_empresas": b["firm_iden"].nunique(),
       "n_empresas_deslistadas_^": b.loc[b["empresa_deslistada"] == 1, "firm_iden"].nunique(),
       "n_directores": b["id_director"].nunique(),
       "n_directores_2mas_directorios": da.loc[da["n_directorios"] >= 2, "id_director"].nunique(),
       "n_directores_sin_rut": b.loc[b["sin_rut"] == 1, "id_director"].nunique(),
       "n_directores_sin_rut_2mas_directorios": da.loc[(da["sin_rut"] == 1) & (da["n_directorios"] >= 2), "id_director"].nunique(),
       "n_directores_politicos": da.loc[da["politico"] == 1, "id_director"].nunique(),
       "n_politicos_2mas_directorios": da.loc[(da["politico"] == 1) & (da["n_directorios"] >= 2), "id_director"].nunique(),
       "n_empresas_con_director_politico": b.loc[b["politico"] == 1, "firm_iden"].nunique(),
       "pct_empresas_con_director_politico": np.nan,
       "n_directores_mujeres": b.loc[b["gender"] == "F", "id_director"].nunique()}
diag = pd.concat([diag, pd.DataFrame([tot])], ignore_index=True)
diag.to_csv(OUT / "diagnostico.csv", index=False, encoding="utf-8-sig")

# resumen de la limpieza (se agrega a la verificación del cruce)
limpieza = pd.DataFrame([
    ("Filas en board", n_total),
    ("Empresa-año en board", fy_total),
    ("Filas CEO excluidas", n_ceo),
    ("Filas sin CEO", n_total - n_ceo),
    ("Duplicados director-empresa-año eliminados", n_dup),
    ("Filas finales director-empresa-año", len(b)),
    ("Empresa-año en la base sin CEO", b[["firm_iden", "anio"]].drop_duplicates().shape[0]),
    ("Empresas distintas", b["firm_iden"].nunique()),
    ("Empresas con '^' (dejaron de transarse)", b.loc[b["empresa_deslistada"] == 1, "firm_iden"].nunique()),
    ("Directores distintos (sin CEO)", b["id_director"].nunique()),
    ("Directores distintos sin RUT", b.loc[b["sin_rut"] == 1, "id_director"].nunique()),
    ("Filas con director sin RUT", int(b["sin_rut"].sum())),
    ("Filas con género faltante (sin CEO)", int(b["gender"].isna().sum())),
], columns=["concepto", "valor"])
verif = pd.concat([limpieza.assign(seccion="Limpieza"), verif.assign(seccion="Cruce de políticos")])
verif = verif[["seccion", "concepto", "valor"]]
verif.to_csv(OUT / "diagnostico_cruce.csv", index=False, encoding="utf-8-sig")

prob = pd.DataFrame(problemas)
prob.to_csv(OUT / "problemas_base.csv", index=False, encoding="utf-8-sig")

print(verif.to_string(index=False))
print(diag.to_string(index=False))
print(f"\nCasos a revisar: {len(prob)}")
