"""Paso 4: preparación de datos (sin búsquedas web). Trabaja sobre copias."""
import re, sys
import pandas as pd

SRC, OUT = sys.argv[1], sys.argv[2]
df = pd.read_excel(SRC, sheet_name='board')
df['anio'] = df.fiscal_year.str[2:].astype(int)
df['director_iden'] = df.director_iden.astype(str).str.strip()

RUT = re.compile(r'^[\d.]+-[\dkK]$')
PART = {'de', 'del', 'la', 'las', 'los', 'y', 'van', 'von', 'da', 'di', 'der', 'dos', 'e', 'mac', 'mc'}

def titulo(s):
    out = []
    for i, w in enumerate(s.lower().split()):
        out.append(w if (w in PART and w not in ('mac', 'mc') and i > 0) else '-'.join(p[:1].upper() + p[1:] for p in w.split('-')))
    return ' '.join(out)

COMPUESTOS = ['Garcia Huidobro', 'García Huidobro', 'Ruiz Tagle', 'Perez Cotapos', 'Santa Maria', 'Santa María', 'San Martin',
              'Santa Cruz', 'Marquez de la Plata', 'Perez de Arce', 'Garcia de la Huerta', 'Ruiz de Gamboa', 'Lopez de Maturana', 'Perez de Castro', 'Diaz de Valdes', 'Martinez de Urquidi']

def partir(nombre):
    """Devuelve (nombres, paterno, materno) suponiendo que los dos últimos bloques son apellidos."""
    for c in COMPUESTOS:
        nombre = re.sub(r'\b%s\b' % c, c.replace(' ', '_'), nombre)
    t = nombre.split()
    bloques = []
    for w in reversed(t):
        if w.lower() in PART and bloques:
            bloques[0] = w + ' ' + bloques[0]   # la partícula va con el apellido que sigue
        else:
            bloques.insert(0, w)
    bloques = [b.replace('_', ' ') for b in bloques]
    if len(bloques) >= 3:
        return ' '.join(bloques[:-2]), bloques[-2], bloques[-1]
    if len(bloques) == 2:
        return bloques[0], bloques[1], ''
    return bloques[0] if bloques else '', '', ''

def categoria(cod):
    return {'D1/CHAIRMAN': 'Presidente(a) del directorio', 'CEO': 'CEO'}.get(cod, 'Director(a)')

df['categoria'] = df.director.map(categoria)

# ---- personas
rows = []
for iden, g in df.groupby('director_iden'):
    graf = sorted(g.name_director.str.strip().unique(), key=lambda s: (-len(s.split()), -len(s), s))
    con_rut = bool(RUT.match(iden))
    nb = titulo(graf[0])
    n, p, m = partir(nb)
    var_b = ' '.join(x for x in [n.split()[0] if n else '', p, m] if x)
    variantes = [nb] + ([var_b] if var_b and var_b != nb else [])
    sim = g.groupby('anio').firm_iden.nunique()
    rows.append(dict(director_iden=iden, RUT='' if not con_rut else iden, Sin_RUT=not con_rut,
                     Nombre_busqueda=nb, Nombres=n, Apellido_paterno=p, Apellido_materno=m,
                     Variantes_busqueda=' ; '.join(variantes),
                     Grafias_en_base='; '.join(graf),
                     N_empresas_distintas=g.firm_iden.nunique(),
                     Max_directorios_simultaneos=int(sim.max()),
                     Anios_empresa=len(g[['firm_iden', 'anio']].drop_duplicates()),
                     Tramo='B' if not con_rut else 'A'))
per = pd.DataFrame(rows).sort_values(['Tramo', 'Max_directorios_simultaneos', 'Anios_empresa', 'Nombre_busqueda'],
                                     ascending=[True, False, False, True]).reset_index(drop=True)
per['Orden'] = range(1, len(per) + 1)
per['ID_persona'] = ['P%04d' % i for i in per.Orden]
per.to_csv(f'{OUT}/personas.csv', index=False)
idmap = dict(zip(per.director_iden, per.ID_persona))
df['ID_persona'] = df.director_iden.map(idmap)

# notas: nombres casi idénticos con identificadores distintos (mismo nombre normalizado)
dup = per.groupby('Nombre_busqueda').ID_persona.apply(list)
dup = dup[dup.str.len() > 1]
print('nombres iguales con distinto identificador:', len(dup))
pd.DataFrame({'Nombre_busqueda': dup.index, 'IDs': dup.str.join('; ')}).to_csv(f'{OUT}/nombres_duplicados.csv', index=False)

# ---- N_directorios_ese_año
nd = df.groupby(['ID_persona', 'anio']).firm_iden.nunique().rename('N_directorios_ese_año')
df = df.join(nd, on=['ID_persona', 'anio'])

# ---- tramos (persona, empresa, categoría, años consecutivos)
tr = []
for (pid, firm, cat), g in df.groupby(['ID_persona', 'firm_iden', 'categoria']):
    anios = sorted(g.anio.unique())
    seg = [[anios[0]]]
    for a in anios[1:]:
        (seg[-1].append(a) if a == seg[-1][-1] + 1 else seg.append([a]))
    for s in seg:
        sub = g[g.anio.isin(s)]
        cods = sorted(sub.director.unique(), key=lambda c: (len(c), c))
        tr.append(dict(ID_persona=pid, firm_iden=firm, Categoria=cat, Anio_inicio=s[0], Anio_termino=s[-1],
                       N_anios=len(s), Puesto='; '.join(cods), Empresa=sub.company_name.iloc[0]))
tr = pd.DataFrame(tr)
tr['Inicio_censurado'] = (tr.Anio_inicio == 2010).astype(int)
tr['Vigente_FY2024'] = (tr.Anio_termino == 2024).astype(int)
tr.to_csv(f'{OUT}/tramos.csv', index=False)
print('tramos:', len(tr))

# año -> tramo
key = {}
for r in tr.itertuples():
    for a in range(r.Anio_inicio, r.Anio_termino + 1):
        key[(r.ID_persona, r.firm_iden, r.Categoria, a)] = (r.Anio_inicio, r.Anio_termino)
df['Anio_inicio_puesto'] = [key[(p, f, c, a)][0] for p, f, c, a in zip(df.ID_persona, df.firm_iden, df.categoria, df.anio)]
df['Anio_termino_puesto'] = [key[(p, f, c, a)][1] for p, f, c, a in zip(df.ID_persona, df.firm_iden, df.categoria, df.anio)]
df.to_csv(f'{OUT}/board_enriquecido.csv', index=False)
print(per.Tramo.value_counts().to_dict(), 'multi grafía:', (per.Grafias_en_base.str.contains(';')).sum())
