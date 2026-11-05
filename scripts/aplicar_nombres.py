"""
Lleva los nombres verificados del maestro a la base original.
Agrega a la base: rut_normalizado, nombre_final, fuente_nombre.
  nombre_final = nombre_verificado si existe; si no, nombre_candidato (marcado 'sin verificar').
Directores sin RUT numérico (extranjeros) quedan con su nombre original.
Uso: python scripts/aplicar_nombres.py base.xlsx datos/maestro_directores_rut.xlsx salida.xlsx
"""
import re, sys
import pandas as pd

base_p, maestro_p, out_p = sys.argv[1:4]
df = pd.read_excel(base_p, dtype=str).fillna("")
m = pd.read_excel(maestro_p, sheet_name="maestro_rut", dtype=str).fillna("")

def norm_rut(x):
    t = re.sub(r"[.\s]", "", x.upper())
    g = re.fullmatch(r"(\d{1,9})-?([\dK])", t)
    return f"{int(g.group(1)):,}".replace(",", ".") + "-" + g.group(2) if g else ""

df["rut_normalizado"] = df.director_iden.map(norm_rut)
m["nombre_final"] = m.nombre_verificado.where(m.nombre_verificado != "", m.nombre_candidato)
m["fuente_nombre"] = m.fuente_verificacion.where(m.nombre_verificado != "", "sin verificar (candidato automático)")
df = df.merge(m[["rut", "nombre_final", "fuente_nombre"]], how="left", left_on="rut_normalizado", right_on="rut").drop(columns="rut")
sin = df.rut_normalizado == ""
df.loc[sin, "nombre_final"] = df.loc[sin, "name_director"]
df.loc[sin, "fuente_nombre"] = "sin RUT (extranjero)"
df.to_excel(out_p, index=False)
print(df.fuente_nombre.value_counts().to_string())
