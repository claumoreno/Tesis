"""Genera interlocking_db_seremis.xlsx desde resultados_parciales.csv usando la plantilla de ministros como molde."""
import sys, json, re, datetime as dt, unicodedata
from copy import copy
import pandas as pd
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
from openpyxl.utils import get_column_letter

PLANTILLA, ORIGINAL, W, OUT = sys.argv[1:5]
per = pd.read_csv(f'{W}/personas.csv', keep_default_na=False)
res = pd.read_csv(f'{W}/resultados_parciales.csv', keep_default_na=False, dtype=str)
tr = pd.read_csv(f'{W}/tramos.csv', keep_default_na=False)
bd = pd.read_csv(f'{W}/board_enriquecido.csv', keep_default_na=False, dtype={'director_iden': str})
GRUPOS = json.load(open(f'{W}/grupos_ministerio.json'))
per = per.merge(res[['ID_persona', 'Consulta_usada', 'Fecha_busqueda', 'Estado_busqueda', 'Notas', 'Cargos_json']], on='ID_persona')

def fecha(s):
    return dt.datetime.strptime(s, '%d-%m-%Y') if s else None

# ---------- cargos y estados (mismas reglas que las fórmulas de la plantilla)
cargos = []
for p in per.itertuples():
    if not p.Cargos_json:
        continue
    for c in json.loads(p.Cargos_json):
        fu = [f for f in c.get('fuentes', []) if f and f[0]][:3]
        n = len(fu)
        ofi = any(f[1] == 'Oficial' for f in fu)
        estado = 'Verificado' if (n >= 3 and ofi) else ('Parcial' if n >= 1 else 'Pendiente')
        ini, ter = fecha(c.get('inicio', '')), fecha(c.get('termino', ''))
        alt = estado
        if ini and ini < dt.datetime(1990, 3, 11) and (ter is None or ter > dt.datetime(1980, 1, 1)):
            if n >= 3 and ofi: alt = 'Verificado'
            elif n == 2 and ofi: alt = 'Verificado (2 fuentes, 1 oficial)'
            elif n == 1 and ofi: alt = 'Verificado (solo 1 oficial)'
            elif n == 0: alt = 'Pendiente'
        cargos.append(dict(c, ID_persona=p.ID_persona, RUT=p.RUT, fuentes=fu, n=n, ofi=ofi, estado=estado, alt=alt,
                           ini=ini, ter=ter, grupo=GRUPOS.get(c.get('ministerio', ''), '')))

con = {}
for pid in {c['ID_persona'] for c in cargos}:
    cs = [c for c in cargos if c['ID_persona'] == pid]
    sop = [c for c in cs if c['estado'] == 'Verificado' or c['alt'].startswith('Verificado')]
    directa = int(bool(sop))
    ampliada = int(directa or any(c['n'] >= 2 for c in cs))
    inis = [c['ini'] for c in cs if c['ini']]
    vig = any(c['ter'] is None for c in cs)
    ters = [c['ter'] for c in cs if c['ter']]
    ofi = [f[0] for c in cs for f in c['fuentes'] if f[1] == 'Oficial']
    todas = [f[0] for c in cs for f in c['fuentes']]
    con[pid] = dict(directa=directa, ampliada=ampliada,
                    nivel='N2' if ampliada else '',
                    cargo=' | '.join(f"{c['cargo']} ({c['institucion']})" for c in cs),
                    a_ini=min(inis).year if inis else '',
                    a_ter='' if vig or not ters else max(ters).year,
                    sop_inis=[c['ini'] for c in sop],
                    fuente=(ofi or todas or [''])[0])

# ---------- libro
wb = openpyxl.load_workbook(PLANTILLA)
HDR = wb['Cargos']['A1']

# Instrucciones
ws = wb['Instrucciones']
ws['B2'] = 'Base de Seremis – Chile 1980–2026'
ws['C18'] = ('Presidente de la República, ministros y subsecretarios; autoridades económicas N3 (Banco Central, SBIF, SVS, CMF, '
             'SII, Dipres, CORFO, BancoEstado); diputados, senadores y miembros de la Junta de Gobierno; intendentes, delegados '
             'y gobernadores regionales (niveles N1 a N5: no se buscan en esta etapa). Además: servicios sectoriales, alcaldes, '
             'concejales, embajadores, asesores, convencionales, empresas del Estado, cargos en otros países. No se registran.')
for cell, v in {'C24': 'Juan Andrés', 'C25': 'Pérez', 'C26': 'Gómez', 'C27': 'J. A. Pérez G.; Juan Pérez Gómez', 'C28': 'N2.3',
                'C29': 'Seremi de Salud, Región de Valparaíso',
                'C30': 'Secretaría Regional Ministerial de Salud, Región de Valparaíso',
                'C31': '11-03-2010', 'C32': '11-03-2014', 'C33': 'Decreto en Diario Oficial (Oficial)'}.items():
    ws[cell] = v

# Catalogo_cargos: N2.3 después de N2.2
ws = wb['Catalogo_cargos']
ws.insert_rows(5)
for col in range(1, 8):
    ws.cell(5, col)._style = copy(ws.cell(4, col)._style)
for col, v in enumerate(['N2.3', 'Secretario(a) Regional Ministerial (Seremi)', 'Secretarías Regionales Ministeriales', '1980–2026',
                         'Principal', 'Titular; no subrogantes ni suplentes',
                         'Exclusiva confianza presidencial: nombrado por el Presidente a partir de una terna del delegado '
                         'presidencial regional, oyendo al ministro de la cartera'], 1):
    ws.cell(5, col, v)
if ws.row_dimensions[4].height:
    ws.row_dimensions[5].height = ws.row_dimensions[4].height

# Resumen: fila nueva N2.3 después de N2.2 (fila 7) y fórmulas reescritas
ws = wb['Resumen']
ws.insert_rows(8)
for col in range(2, 9):
    ws.cell(8, col)._style = copy(ws.cell(7, col)._style)
ws['B8'], ws['C8'] = 'N2.3', 'Secretario(a) Regional Ministerial (Seremi)'
R = 'Cargos!$I$2:$I$3001'; Y = 'Cargos!$Y$2:$Y$3001'
for r in range(5, 20):
    ws[f'D{r}'] = f'=COUNTIF({R},B{r})'
    ws[f'E{r}'] = f'=COUNTIFS({R},B{r},{Y},"Verificado")'
    ws[f'F{r}'] = f'=COUNTIFS({R},B{r},{Y},"Parcial")'
    ws[f'G{r}'] = f'=COUNTIFS({R},B{r},{Y},"Pendiente")'
    ws[f'H{r}'] = f'=IF(D{r}=0,0,E{r}/D{r})'
assert ws['B20'].value == 'Total'
for c in 'DEFG':
    ws[f'{c}20'] = f'=SUM({c}5:{c}19)'
ws['H20'] = '=IF(D20=0,0,E20/D20)'
assert ws['B22'].value == 'Personas distintas registradas'
ws['D22'] = '=SUMPRODUCT((Cargos!$B$2:$B$3001<>"")/COUNTIF(Cargos!$B$2:$B$3001,Cargos!$B$2:$B$3001&""))'

# Cargos: validación de Nivel con N2.3, borrar datos (azules + AB, AC) y escribir los Seremis
ws = wb['Cargos']
for dv in ws.data_validations.dataValidation:
    if 'N2.2' in (dv.formula1 or ''):
        dv.formula1 = '"N1,N2.1,N2.2,N2.3,N3.1,N3.2,N3.3,N3.4,N3.5,N3.6,N3.7,N3.8,N4.1,N4.2,N5"'
AZUL = ['A', 'B', 'C', 'D', 'E', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'Q', 'R', 'S', 'T', 'U', 'V', 'Z', 'AB', 'AC']
for r in range(2, ws.max_row + 1):
    for c in AZUL:
        ws[f'{c}{r}'].value = None
assert len(cargos) <= 3000
for i, c in enumerate(cargos, 2):
    vals = {'A': 'R%05d' % (i - 1), 'B': c['ID_persona'], 'C': c.get('nombres'), 'D': c.get('paterno'), 'E': c.get('materno') or None,
            'G': c.get('variantes'), 'H': c['RUT'] or None, 'I': 'N2.3', 'J': c['cargo'], 'K': c['institucion'],
            'L': c['ini'], 'M': c['ter'], 'Z': c.get('notas'), 'AB': c['grupo'] or None, 'AC': c['alt']}
    for k, (u, t) in zip(['Q', 'S', 'U'], c['fuentes']):
        vals[k] = u
        vals[chr(ord(k) + 1)] = t
    for k, v in vals.items():
        ws[f'{k}{i}'] = v

# ---------- hojas nuevas
def hoja(nombre, df, anchos=None):
    ws = wb.create_sheet(nombre)
    ws.append(list(df.columns))
    for row in df.itertuples(index=False):
        ws.append(['' if (isinstance(v, float) and pd.isna(v)) else v for v in row])
    for j in range(1, len(df.columns) + 1):
        h = ws.cell(1, j)
        h._style = copy(HDR._style)
        ws.column_dimensions[get_column_letter(j)].width = (anchos or {}).get(j, max(12, min(45, len(str(h.value)) + 4)))
    ws.freeze_panes = 'A2'
    ws.auto_filter.ref = ws.dimensions
    ws.row_dimensions[1].height = 31.5
    return ws

def norm(s):
    s = unicodedata.normalize('NFKD', s.lower())
    return ''.join(ch for ch in s if not unicodedata.combining(ch))

# notas de nombres casi idénticos (no se fusionan)
claves = {}
for p in per.itertuples():
    t = norm(p.Nombre_busqueda).split()
    if len(t) >= 2:
        claves.setdefault((t[0], norm(p.Apellido_paterno)), []).append(p.ID_persona)
casi = {}
for ids in claves.values():
    if len(ids) > 1:
        for i in ids:
            casi[i] = [j for j in ids if j != i]
def nota(p):
    n = [p.Notas] if p.Notas else []
    if p.ID_persona in casi:
        n.append('Nombre casi idéntico a ' + ', '.join(casi[p.ID_persona][:5]) + ' (identificador distinto; no se fusionó).')
    return ' '.join(n)

dirs = pd.DataFrame({'ID_persona': per.ID_persona, 'director_iden': per.director_iden,
                     'RUT o "Sin RUT"': [r if r else 'Sin RUT' for r in per.RUT], 'Nombre_busqueda': per.Nombre_busqueda,
                     'Grafias_en_base': per.Grafias_en_base, 'N_empresas_distintas': per.N_empresas_distintas,
                     'Max_directorios_simultaneos': per.Max_directorios_simultaneos, 'Tramo': per.Tramo,
                     'Consulta_usada': per.Consulta_usada, 'Fecha_busqueda': per.Fecha_busqueda,
                     'Estado_busqueda': per.Estado_busqueda, 'Notas': [nota(p) for p in per.itertuples()]})
hoja('Directores', dirs, {4: 32, 5: 45, 9: 60, 11: 20, 12: 60})

nom = dict(zip(per.ID_persona, per.Nombre_busqueda)); rut = dict(zip(per.ID_persona, per.RUT))
tr = tr.sort_values(['ID_persona', 'firm_iden', 'Anio_inicio', 'Categoria'])
dto = pd.DataFrame({'ID_persona': tr.ID_persona, 'Nombre del director': tr.ID_persona.map(nom), 'RUT': tr.ID_persona.map(rut),
                    'Empresa': tr.Empresa, 'firm_iden': tr.firm_iden, 'Puesto': tr.Puesto, 'Categoría de puesto': tr.Categoria,
                    'Año_inicio': tr.Anio_inicio, 'Año_termino': tr.Anio_termino, 'N_años': tr.N_anios,
                    'Inicio_censurado': tr.Inicio_censurado, 'Vigente_FY2024': tr.Vigente_FY2024})
hoja('Directorios', dto, {2: 32, 4: 36})

g = lambda pid, k, d='': con.get(pid, {}).get(k, d)
bd = bd.sort_values(['firm_iden', 'anio', 'ID_persona', 'director'])
def previo(pid, anio):
    if not g(pid, 'directa', 0): return 0
    return int(any(i <= dt.datetime(anio, 12, 31) for i in g(pid, 'sop_inis', [])))
bf = pd.DataFrame({'Empresa': bd.company_name, 'firm_iden': bd.firm_iden, 'Año': bd.anio, 'Nombre del director': bd.name_director,
                   'ID_persona': bd.ID_persona, 'RUT': bd.ID_persona.map(rut), 'Puesto en el directorio': bd.director,
                   'Categoría de puesto': bd.categoria, 'Año inicio puesto': bd.Anio_inicio_puesto,
                   'Año término puesto': bd.Anio_termino_puesto, 'N_directorios_ese_año': bd['N_directorios_ese_año'],
                   'Conexion_directa': [g(p, 'directa', 0) for p in bd.ID_persona],
                   'Conexion_ampliada': [g(p, 'ampliada', 0) for p in bd.ID_persona],
                   'Nivel_mas_alto': [g(p, 'nivel') for p in bd.ID_persona],
                   'Cargo político e institución': [g(p, 'cargo') for p in bd.ID_persona],
                   'Año inicio cargo político': [g(p, 'a_ini') for p in bd.ID_persona],
                   'Año término cargo político': [g(p, 'a_ter') for p in bd.ID_persona],
                   'Seremi_previo_o_simultaneo': [previo(p, a) for p, a in zip(bd.ID_persona, bd.anio)],
                   'Fuente': [g(p, 'fuente') for p in bd.ID_persona]})
hoja('Base_final', bf, {1: 34, 4: 34, 15: 50, 19: 50})

ea = (bf.drop_duplicates(['firm_iden', 'Año', 'ID_persona'])
        .groupby(['firm_iden', 'Año'])
        .agg(company_name=('Empresa', 'first'), N_directores=('ID_persona', 'nunique'),
             N_directores_conectados=('Conexion_directa', 'sum'), N_amp=('Conexion_ampliada', 'sum')).reset_index())
ea = pd.DataFrame({'firm_iden': ea.firm_iden, 'company_name': ea.company_name, 'Año': ea['Año'], 'N_directores': ea.N_directores,
                   'N_directores_conectados': ea.N_directores_conectados,
                   'Empresa_conectada': (ea.N_directores_conectados >= 1).astype(int),
                   'Empresa_conectada_ampliada': (ea.N_amp >= 1).astype(int)})
hoja('Empresa_año', ea, {2: 36})

# board original sin cambios
src = openpyxl.load_workbook(ORIGINAL)['board']
ws = wb.create_sheet('board')
for row in src.iter_rows(values_only=True):
    ws.append(row)
for k, d in src.column_dimensions.items():
    ws.column_dimensions[k].width = d.width
for j, c in enumerate(src[1], 1):
    ws.cell(1, j)._style = copy(c._style)
ws.freeze_panes = src.freeze_panes
ws.auto_filter.ref = src.auto_filter.ref

wb.calculation.fullCalcOnLoad = True
wb.active = 0
wb.save(OUT)
json.dump({'cargos': len(cargos), 'verificados': sum(c['estado'] == 'Verificado' for c in cargos),
           'parciales': sum(c['estado'] == 'Parcial' for c in cargos),
           'estados_python': [c['estado'] for c in cargos],
           'empresas_conectadas': int(ea.groupby('firm_iden').Empresa_conectada.max().sum())}, open(f'{W}/resumen_build.json', 'w'))
print('ok', OUT, len(cargos), 'cargos')
