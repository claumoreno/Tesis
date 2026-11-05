"""
Integra la verificación web de los RUTs con variantes de nombre
(datos/verificacion_web_217.tsv) al maestro de directores y genera:
  datos/maestro_directores_rut_verificado.xlsx  (1 fila por RUT, nombre final + estado + fuentes)
  datos/interlocking_db_nombres_corregidos.xlsx (base original + nombre_final por fila)

Uso: python scripts/integrar_verificacion.py interlocking_db.xlsx
"""
import re, sys
from collections import Counter
import pandas as pd
from unidecode import unidecode

base_p = sys.argv[1]
maestro = pd.read_excel("datos/maestro_directores_rut.xlsx", sheet_name="maestro_rut", dtype=str).fillna("")
verif = pd.read_csv("datos/verificacion_web_217.tsv", sep="\t", dtype=str).fillna("")
base = pd.read_excel(base_p, dtype=str).fillna("")

# Diccionario de palabras para restaurar la Ñ (la base usa MAYÚSCULAS, con Ñ y sin tildes)
tok = Counter(t for n in base.name_director for t in n.upper().split())
enie = {}
for t, c in tok.items():
    k = unidecode(t)
    if "Ñ" in t and c > tok.get(k, 0) / 3:
        enie[k] = t
enie.update({"PENA": "PEÑA", "INAKI": "IÑAKI", "MUNOZ": "MUÑOZ", "VICUNA": "VICUÑA",
             "CANAS": "CAÑAS", "BASCUNAN": "BASCUÑAN", "IBANEZ": "IBAÑEZ", "ZANARTU": "ZAÑARTU"})

def con_enie(n):
    return " ".join(enie.get(t, t) for t in n.split())

ESTADOS = {
    "verificado_2+_fuentes": "1. Verificado: 2 o más fuentes web",
    "verificado_1_fuente": "2. Verificado: 1 fuente web que calza con la empresa",
    "verificado_indirecto": "3. Verificado indirecto (apellido confirmado en familiar)",
    "completitud_sin_fuente_web": "4. Sin fuente web: se tomó la forma más completa de la base",
    "corregido_sin_fuente_web": "5. Sin fuente web: corregido error tipográfico evidente",
    "no_confirmado": "6. NO CONFIRMADO: revisar a mano",
}
verif["estado_verificacion"] = verif.estado.map(ESTADOS)
verif["nombre_verificado"] = verif.nombre_verificado.map(con_enie)

m = maestro.drop(columns=["nombre_verificado", "fuente_verificacion", "notas"]).merge(
    verif[["rut", "nombre_verificado", "estado_verificacion", "fuentes", "nota"]], on="rut", how="left").fillna("")
unico = m.estado_verificacion == ""
m.loc[unico, "estado_verificacion"] = "0. Un solo nombre en la base (no buscado en web)"
m["nombre_final"] = m.nombre_verificado.where(m.nombre_verificado != "", m.nombre_candidato)

# casos de RUT sospechoso (prioridad alta sin variantes)
notas_extra = {
    "235-6": "RUT SOSPECHOSO: 3 dígitos, no plausible (probablemente truncado en la memoria). Apellido correcto: VALDÉS. "
             "EX DIPUTADO y EX ALCALDE (https://en.wikipedia.org/wiki/Gustavo_Alessandri_Vald%C3%A9s). Buscar RUT real en memoria/CMF",
    "401.301-8": "RUT SOSPECHOSO: 6 dígitos, probablemente truncado. Sin resultados web para Copec. Buscar RUT real en memoria/CMF",
}
for r, t in notas_extra.items():
    i = m.rut == r
    m.loc[i, "nota"] = t
    m.loc[i, "estado_verificacion"] = "6. NO CONFIRMADO: revisar a mano"
m.loc[m.rut == "235-6", "nombre_final"] = "GUSTAVO ALESSANDRI VALDES"

POL = re.compile(r"(POSIBLE EX MINISTR\w* DE \w+|EX MINISTR\w*|MINISTRO DE RR\.EE\.|EX DIPUTAD\w*|EX SENADOR\w*|EX ALCALDE|"
                 r"EX INTENDENTE[^.;]*|EX CONVENCIONAL CONSTITUYENTE|EX PRESIDENTE CÁMARA DE DIPUTADOS|EX EMBAJADOR[^.;]*|"
                 r"presidente de CODELCO|presidente CODELCO|director de Codelco|Banco Central|empresa estatal|"
                 r"régimen militar|nieta de A\. Pinochet|yerno de A\. Pinochet|Radomiro Tomic Romero)")
m["pista_politica_detectada"] = m.nota.map(lambda s: " | ".join(dict.fromkeys(x.strip() for x in POL.findall(s))))

m["revisar_a_mano"] = m.estado_verificacion.str[0].isin(["4", "5", "6"]) | m.nota.str.contains("VERIFICAR|OJO|confirmar", case=False)
cols = ["rut", "nombre_final", "estado_verificacion", "revisar_a_mano", "pista_politica_detectada", "fuentes", "nota",
        "variantes", "tipo_diferencia", "n_obs", "anio_min", "anio_max", "empresas", "nombre_parecido_a_otro_rut",
        "rut_num", "dv", "dv_valido"]
m = m[cols].rename(columns={"nota": "notas"})
m["_o"] = m.estado_verificacion.str[0].astype(int)
m = m.sort_values(["_o", "rut_num"], key=lambda s: s.astype(int) if s.name == "rut_num" else s, ascending=[False, True]).drop(columns="_o")

resumen = (m.estado_verificacion.value_counts().sort_index().rename_axis("estado").reset_index(name="n_ruts"))
otras = pd.read_excel("datos/maestro_directores_rut.xlsx", sheet_name=None)

with pd.ExcelWriter("datos/maestro_directores_rut_verificado.xlsx") as w:
    resumen.to_excel(w, sheet_name="resumen", index=False)
    m.to_excel(w, sheet_name="maestro_rut", index=False)
    m[m.revisar_a_mano].to_excel(w, sheet_name="revisar_a_mano", index=False)
    m[m.pista_politica_detectada != ""].to_excel(w, sheet_name="pistas_politicas", index=False)
    otras["nombres_parecidos"].to_excel(w, sheet_name="nombres_parecidos", index=False)
    otras["sin_rut_excluidos"].to_excel(w, sheet_name="sin_rut_excluidos", index=False)

# base completa con nombre final
def norm_rut(x):
    t = re.sub(r"[.\s]", "", x.upper())
    g = re.fullmatch(r"(\d{1,9})-?([\dK])", t)
    return f"{int(g.group(1)):,}".replace(",", ".") + "-" + g.group(2) if g else ""

base["rut_normalizado"] = base.director_iden.map(norm_rut)
base = base.merge(m[["rut", "nombre_final", "estado_verificacion"]], how="left", left_on="rut_normalizado", right_on="rut").drop(columns="rut")
sin = base.rut_normalizado == ""
base.loc[sin, "nombre_final"] = base.loc[sin, "name_director"]
base.loc[sin, "estado_verificacion"] = "Sin RUT (extranjero): no verificado"
base["nombre_cambio"] = base.nombre_final != base.name_director.str.strip()
base.to_excel("datos/interlocking_db_nombres_corregidos.xlsx", index=False)

print(resumen.to_string(index=False))
print("revisar a mano:", int(m.revisar_a_mano.sum()), "| pistas políticas:", int((m.pista_politica_detectada != "").sum()))
print("filas de la base con nombre cambiado:", int(base.nombre_cambio.sum()), "de", len(base))
