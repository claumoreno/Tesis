# -*- coding: utf-8 -*-
"""
ETAPA 6 (parte 2). Validación de los resultados sobre la base real.

- Valores imposibles (densidad fuera de [0, 1], grados negativos, proporciones fuera de rango).
- Empresa-año repetidos en el panel.
- N° de empresa-año del panel = n° de empresa-año de la base sin CEO.
- Identidades internas (grado medio = densidad * (n-1), grado medio = media del grado del panel).

Salida: output/validacion_panel.csv. El script falla si alguna verificación no se cumple.
"""

from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"

b = pd.read_csv(OUT / "intermedios" / "board_limpio.csv", encoding="utf-8-sig", dtype={"id_director": str})
pe = pd.read_csv(OUT / "panel_red_empresa_anio.csv", encoding="utf-8-sig")
pdr = pd.read_csv(OUT / "panel_red_director_anio.csv", encoding="utf-8-sig", dtype={"id_director": str})
coh = pd.read_csv(OUT / "cohesion_por_anio.csv", encoding="utf-8-sig")

res = []


def chequeo(nombre, condicion, detalle=""):
    res.append({"verificacion": nombre, "ok": bool(condicion), "detalle": detalle})
    print(f"[{'OK' if condicion else 'FALLA'}] {nombre} {detalle}")


def entre(s, lo, hi):
    s = s.dropna()
    return bool(((s >= lo - 1e-9) & (s <= hi + 1e-9)).all())


# 1. Valores imposibles en cohesión
chequeo("Densidad entre 0 y 1", entre(coh["densidad"], 0, 1))
for v in ["conectividad", "compacidad", "coef_agrupamiento_global", "centralizacion_grado",
          "ratio_componentes"]:
    chequeo(f"{v} entre 0 y 1", entre(coh[v], 0, 1))
for v in ["pct_comp_principal", "pct_aislados", "pct_puntos_corte", "pct_relaciones_multiples"]:
    chequeo(f"{v} entre 0 y 100", entre(coh[v], 0, 100))
chequeo("Grado medio = densidad * (n - 1)",
        np.allclose(coh["grado_medio"], coh["densidad"] * (coh["n_nodos"] - 1)))
gm_panel = pe.groupby("anio")["grado"].mean().reindex(coh["anio"]).values
chequeo("Grado medio = media del grado de las empresas del panel", np.allclose(coh["grado_medio"], gm_panel))
chequeo("Suma de grados del panel = 2L", np.array_equal(pe.groupby("anio")["grado"].sum().reindex(coh["anio"]).values,
                                                        2 * coh["n_enlaces"].values))
chequeo("Distancia media del comp. principal >= 1", entre(coh["distancia_media_comp_principal"], 1, np.inf))

# 2. Valores imposibles en el panel de empresas
for v in ["grado", "grado_ponderado", "intermediacion", "cercania_armonica", "n_directores",
          "n_politicos", "n_vecinos_con_politico"]:
    chequeo(f"{v} no negativo", (pe[v] >= 0).all())
for v in ["grado_norm", "intermediacion_norm", "cercania_armonica_norm", "eigenvector_comp_principal"]:
    chequeo(f"{v} entre 0 y 1", entre(pe[v], 0, 1))
for v in ["pct_politicos", "pct_mujeres", "pct_vecinos_con_politico"]:
    chequeo(f"{v} entre 0 y 100", entre(pe[v], 0, 100))
chequeo("Grado ponderado >= grado", (pe["grado_ponderado"] >= pe["grado"]).all())
chequeo("Eigenvector vacío solo fuera del componente principal",
        (pe["eigenvector_comp_principal"].isna() == (pe["en_comp_principal"] == 0)).all())
chequeo("Aislados con grado 0 e intermediación 0",
        ((pe.loc[pe["aislado"] == 1, ["grado", "intermediacion"]] == 0).all().all()))
chequeo("Distancia mínima a empresa con político >= 1", entre(pe["dist_min_empresa_con_politico"], 1, np.inf))
chequeo("Puente político implica tener director político",
        (pe.loc[pe["puente_politico"] == 1, "tiene_politico"] == 1).all())
chequeo("n_vecinos_via_politico <= grado", (pe["n_vecinos_via_politico"] <= pe["grado"]).all())

# 3. Unicidad y cobertura
dup = pe.duplicated(["firm_iden", "anio"]).sum()
chequeo("Sin empresa-año repetidos en el panel de empresas", dup == 0, f"(duplicados: {dup})")
dupd = pdr.duplicated(["id_director", "anio"]).sum()
chequeo("Sin director-año repetidos en el panel de directores", dupd == 0, f"(duplicados: {dupd})")
fy_base = b[["firm_iden", "anio"]].drop_duplicates()
chequeo("N° empresa-año del panel = n° empresa-año de la base sin CEO", len(pe) == len(fy_base),
        f"(panel {len(pe)}, base {len(fy_base)})")
m = fy_base.merge(pe[["firm_iden", "anio"]], how="outer", indicator=True)
chequeo("Las empresa-año del panel y de la base son las mismas", (m["_merge"] == "both").all())
chequeo("N° director-año del panel = n° director-año de la base sin CEO",
        len(pdr) == b[["id_director", "anio"]].drop_duplicates().shape[0])
chequeo("n_directorios del panel de directores = filas del director en la base",
        np.array_equal(pdr.sort_values(["id_director", "anio"])["n_directorios"].values,
                       b.groupby(["id_director", "anio"]).size().sort_index().values))
chequeo("Directores sin RUT nunca son políticos", (pdr.loc[pdr["sin_rut"] == 1, "politico"] == 0).all())
uno = pdr[pdr["n_directorios"] == 1].merge(
    pe[["firm_iden", "anio", "n_directores"]], left_on=["empresas", "anio"], right_on=["firm_iden", "anio"])
chequeo("Director en un solo directorio: grado en red de directores = n° de directores de esa empresa - 1",
        (uno["grado_red_directores"] == uno["n_directores"] - 1).all(), f"({len(uno)} casos)")

tabla = pd.DataFrame(res)
tabla.to_csv(OUT / "validacion_panel.csv", index=False, encoding="utf-8-sig")
fallas = (~tabla["ok"]).sum()
print(f"\n{len(tabla)} verificaciones, {fallas} fallas")
if fallas:
    raise SystemExit("Hay verificaciones que fallan.")
