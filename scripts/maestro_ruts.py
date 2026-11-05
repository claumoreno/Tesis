"""
Construye un maestro de directores (1 fila por RUT) a partir de interlocking_db.xlsx
y genera diagnósticos de calidad:
  - validación del dígito verificador (módulo 11)
  - RUTs con más de una variante de nombre (y tipo de diferencia)
  - RUTs distintos con nombres casi idénticos (posible RUT mal digitado o familiares)
  - mismo RUT dos veces en la misma empresa-año (posible confusión de personas)
Uso: python scripts/maestro_ruts.py ruta/interlocking_db.xlsx datos/
"""
import re, sys
from collections import Counter
from pathlib import Path
import pandas as pd
from rapidfuzz import fuzz
from unidecode import unidecode

src, outdir = Path(sys.argv[1]), Path(sys.argv[2])
df = pd.read_excel(src, dtype=str).fillna("")

def dv(body: int) -> str:
    s, m = 0, 2
    for d in reversed(str(body)):
        s += int(d) * m
        m = 2 if m == 7 else m + 1
    r = 11 - s % 11
    return "0" if r == 11 else "K" if r == 10 else str(r)

def parse_rut(x):
    t = re.sub(r"[.\s]", "", x.upper())
    m = re.fullmatch(r"(\d{1,9})-?([\dK])", t)
    if not m:
        return None
    return int(m.group(1)), m.group(2)

def norm(n):  # para comparar nombres
    return re.sub(r"\s+", " ", unidecode(n).upper().replace(".", " ")).strip()

df["_p"] = df.director_iden.map(parse_rut)
df["es_rut"] = df._p.notna()
ch = df[df.es_rut].copy()
ch["rut_num"] = ch._p.map(lambda p: p[0])
ch["dv"] = ch._p.map(lambda p: p[1])
ch["rut"] = ch.rut_num.map(lambda b: f"{b:,}".replace(",", ".")) + "-" + ch.dv
ch["dv_valido"] = ch.apply(lambda r: dv(r.rut_num) == r.dv, axis=1)
ch["name_norm"] = ch.name_director.map(norm)

def classify(variants):
    """'unico' | 'solo_completitud' (un nombre contiene al otro) | 'diferencia_ortografica' | 'nombres_distintos'"""
    if len(variants) == 1:
        return "unico"
    toks = [set(v.split()) for v in variants]
    base = max(toks, key=len)
    if all(t <= base for t in toks):
        return "solo_completitud"
    worst = min(fuzz.token_set_ratio(a, b) for a in variants for b in variants)
    return "diferencia_ortografica" if worst >= 80 else "nombres_distintos"

rows = []
for rut, g in ch.groupby("rut"):
    cnt = Counter(g.name_norm)
    variants = list(cnt)
    tipo = classify(variants)
    # candidato: el más completo (más palabras); empate -> el más frecuente
    cand = max(variants, key=lambda v: (len(v.split()), cnt[v]))
    years = sorted(g.fiscal_year.str[2:].astype(int))
    rows.append(dict(
        rut=rut, rut_num=g.rut_num.iat[0], dv=g.dv.iat[0], dv_valido=bool(g.dv_valido.iat[0]),
        nombre_candidato=cand, n_variantes=len(variants), tipo_diferencia=tipo,
        variantes=" | ".join(f"{v} ({c})" for v, c in cnt.most_common()),
        n_obs=len(g), anio_min=years[0], anio_max=years[-1],
        empresas=" | ".join(sorted(g.company_name.unique())),
    ))
m = pd.DataFrame(rows)

# mismo RUT dos veces en la misma empresa-año
dup = ch.groupby(["rut", "firm_iden", "fiscal_year"]).size()
dup_ruts = set(dup[dup > 1].index.get_level_values(0))
m["repetido_misma_empresa_anio"] = m.rut.isin(dup_ruts)

# RUTs distintos con nombres muy parecidos
sim = []
names = m[["rut", "rut_num", "nombre_candidato"]].values.tolist()
for i in range(len(names)):
    for j in range(i + 1, len(names)):
        a, b = names[i], names[j]
        s = fuzz.token_sort_ratio(a[2], b[2])
        if s >= 88:
            da = sum(x != y for x, y in zip(str(a[1]).zfill(9), str(b[1]).zfill(9)))
            sim.append(dict(rut_a=a[0], nombre_a=a[2], rut_b=b[0], nombre_b=b[2], similitud=round(s, 1),
                            digitos_distintos=da,
                            sospecha=("RUTs consecutivos: probablemente hermanos" if abs(a[1] - b[1]) <= 2
                                      else "posible RUT mal digitado" if da <= 2
                                      else "posibles familiares / homónimos")))
sim = pd.DataFrame(sim)
sim_ruts = set(sim.rut_a) | set(sim.rut_b) if len(sim) else set()
m["nombre_parecido_a_otro_rut"] = m.rut.isin(sim_ruts)

def prioridad(r):
    if not r.dv_valido or r.rut_num < 1_000_000 or r.tipo_diferencia == "nombres_distintos" or r.repetido_misma_empresa_anio:
        return "1-alta"
    if r.tipo_diferencia == "diferencia_ortografica" or r.nombre_parecido_a_otro_rut or len(r.nombre_candidato.split()) < 3:
        return "2-media"
    return "3-baja"
m["prioridad_verificacion"] = m.apply(prioridad, axis=1)
m["nombre_verificado"] = ""      # a completar con CMF / rutificador
m["fuente_verificacion"] = ""    # CMF, nombrerutyfirma, memoria, prensa...
m["notas"] = ""
m = m.sort_values(["prioridad_verificacion", "rut_num"])

extranjeros = (df[~df.es_rut].groupby("director_iden")
               .agg(n_obs=("id", "size"), empresas=("company_name", lambda s: " | ".join(sorted(set(s)))))
               .reset_index().rename(columns={"director_iden": "identificador_texto"}))

resumen = pd.DataFrame([
    ("Filas totales en la base", len(df)),
    ("Filas con RUT numérico", int(df.es_rut.sum())),
    ("Filas sin RUT (extranjeros, excluidos)", int((~df.es_rut).sum())),
    ("RUTs únicos", len(m)),
    ("RUTs con dígito verificador INVÁLIDO", int((~m.dv_valido).sum())),
    ("RUTs sospechosamente cortos (< 1.000.000)", int((m.rut_num < 1_000_000).sum())),
    ("RUTs con 1 sola forma de nombre", int((m.n_variantes == 1).sum())),
    ("RUTs con variantes: solo nombre más/menos completo", int((m.tipo_diferencia == "solo_completitud").sum())),
    ("RUTs con variantes: errores de ortografía", int((m.tipo_diferencia == "diferencia_ortografica").sum())),
    ("RUTs con nombres DISTINTOS (posible 2 personas)", int((m.tipo_diferencia == "nombres_distintos").sum())),
    ("RUTs repetidos en la misma empresa-año", int(m.repetido_misma_empresa_anio.sum())),
    ("Pares de RUTs distintos con nombre muy parecido", len(sim)),
    ("Nombres con menos de 3 palabras", int((m.nombre_candidato.str.split().str.len() < 3).sum())),
    ("Prioridad 1 (alta)", int((m.prioridad_verificacion == "1-alta").sum())),
    ("Prioridad 2 (media)", int((m.prioridad_verificacion == "2-media").sum())),
    ("Prioridad 3 (baja)", int((m.prioridad_verificacion == "3-baja").sum())),
], columns=["indicador", "valor"])

out = outdir / "maestro_directores_rut.xlsx"
with pd.ExcelWriter(out) as w:
    resumen.to_excel(w, sheet_name="resumen", index=False)
    m.to_excel(w, sheet_name="maestro_rut", index=False)
    m[~m.dv_valido].to_excel(w, sheet_name="dv_invalido", index=False)
    m[m.n_variantes > 1].to_excel(w, sheet_name="variantes_nombre", index=False)
    sim.to_excel(w, sheet_name="nombres_parecidos", index=False)
    extranjeros.to_excel(w, sheet_name="sin_rut_excluidos", index=False)
print(resumen.to_string(index=False))
print("->", out)
