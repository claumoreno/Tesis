"""
Agrega el pasado político (datos/pasado_politico.tsv) al maestro verificado y a la base completa.
Columnas nuevas: pasado_politico, tipo_cargo, cargos_politicos, fuentes_cargo_politico, confianza_cargo.
Uso: python scripts/integrar_pasado_politico.py
"""
import re
import pandas as pd

pp = pd.read_csv("datos/pasado_politico.tsv", sep="\t", dtype=str).fillna("")

TIPOS = [
    ("Ministro/a", r"Ministr[oa] (?!Presidente de la Comisi)|Biministro|Ministra"),
    ("Subsecretario/a", r"Subsecretari"),
    ("Parlamentario/a", r"Diputad|Senador|Riksdag"),
    ("Convencional / proceso constituyente", r"Convencional|Comisión Experta"),
    ("Alcalde / Intendente", r"Alcald|Intendente"),
    ("Banco Central / organismo autónomo", r"Banco Central|Contralor|Servel|Consejo Fiscal|Superintendent|Consejo Nacional de Televisión|CNTV|Comisión Nacional de Productividad"),
    ("Jefe de servicio público", r"Director de Presupuestos|Director del SII|Servicio de Impuestos|Odeplan|SECOM|Secretaría de Comunicaciones|Fonasa|Comisión Nacional de Energía|Comité de Inversiones"),
    ("Directivo de empresa estatal", r"Codelco|BancoEstado|Corfo|ENAP|Metro|TVN|ENACAR|EFE|SEP|empresa estatal"),
    ("Cargo político en el extranjero", r"\(España\)|Suecia|BCE|FMI|BID|Banco Mundial"),
    ("Embajador/a", r"Embajad"),
]
def tipos(t):
    return " | ".join(n for n, rx in TIPOS if re.search(rx, t)) or "Otro cargo público"
pp["tipo_cargo"] = pp.cargos_politicos.map(tipos)
pp = pp.rename(columns={"fuentes": "fuentes_cargo_politico", "confianza": "confianza_cargo"})
cols = ["tipo_cargo", "cargos_politicos", "fuentes_cargo_politico", "confianza_cargo"]

xl = pd.read_excel("datos/maestro_directores_rut_verificado.xlsx", sheet_name=None)
m = xl["maestro_rut"].merge(pp[["nombre_final"] + cols], on="nombre_final", how="left")
m["pasado_politico"] = m.cargos_politicos.notna().map({True: "SÍ", False: "No identificado"})
m[cols] = m[cols].fillna("")
orden = ["rut", "nombre_final", "pasado_politico", "tipo_cargo", "cargos_politicos", "fuentes_cargo_politico", "confianza_cargo"]
m = m[orden + [c for c in m.columns if c not in orden]]
xl["maestro_rut"] = m
xl["pasado_politico"] = m[m.pasado_politico == "SÍ"][orden + ["empresas", "anio_min", "anio_max"]].sort_values("nombre_final")
xl["pistas_politicas"] = None  # reemplazada por la hoja pasado_politico
del xl["pistas_politicas"]
res = xl["resumen"]
extra = pd.DataFrame({"estado": ["Directores con pasado político identificado", "Sin pasado político identificado (no implica que no tengan)"],
                      "n_ruts": [int((m.pasado_politico == "SÍ").sum()), int((m.pasado_politico != "SÍ").sum())]})
xl["resumen"] = pd.concat([res, pd.DataFrame({"estado": [""], "n_ruts": [None]}), extra], ignore_index=True)
with pd.ExcelWriter("datos/maestro_directores_rut_verificado.xlsx") as w:
    for k in ["resumen", "maestro_rut", "pasado_politico", "revisar_a_mano", "nombres_parecidos", "sin_rut_excluidos"]:
        xl[k].to_excel(w, sheet_name=k, index=False)

b = pd.read_excel("datos/interlocking_db_nombres_corregidos.xlsx", dtype=str)
for c in ["pasado_politico"] + cols:
    if c in b.columns: b = b.drop(columns=c)
b = b.merge(m[["rut", "pasado_politico"] + cols], how="left", left_on="rut_normalizado", right_on="rut").drop(columns="rut")
b["pasado_politico"] = b.pasado_politico.fillna("No evaluado (sin RUT)")
b.to_excel("datos/interlocking_db_nombres_corregidos.xlsx", index=False)
print(extra.to_string(index=False))
print(xl["pasado_politico"].tipo_cargo.str.split(" \\| ").explode().value_counts().to_string())
print("filas base con pasado político:", int((b.pasado_politico == "SÍ").sum()))
