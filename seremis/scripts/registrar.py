"""Uso: registrar.py W lote < lineas 'ID|Estado|Notas' ; IDs listados sin línea en stdin => usar 'ID' solo = Sin evidencia.
Cargos: línea 'ID|Con cargo registrado|Notas|<json lista de cargos>'."""
import pandas as pd, sys, datetime, json
W, lote = sys.argv[1], sys.argv[2]
r = pd.read_csv(f'{W}/resultados_parciales.csv', keep_default_na=False, dtype=str)
hoy = datetime.date.today().strftime('%d-%m-%Y')
n = ind = 0
for line in sys.stdin:
    line = line.strip()
    if not line: continue
    parts = line.split('|', 4)
    pid = parts[0].strip()
    est = parts[1].strip() if len(parts) > 1 and parts[1].strip() else 'Sin evidencia'
    nota = parts[2].strip() if len(parts) > 2 else ''
    cj = parts[3].strip() if len(parts) > 3 else ''
    cq = parts[4].strip() if len(parts) > 4 else ''
    if cj: json.loads(cj)
    m = r.ID_persona == pid
    assert m.sum() == 1, pid
    r.loc[m, ['Estado_busqueda', 'Fecha_busqueda', 'Notas', 'Cargos_json']] = [est, hoy, nota, cj]
    if cq: r.loc[m, 'Consulta_usada'] = cq
    n += 1; ind += est != 'Sin evidencia'
r.to_csv(f'{W}/resultados_parciales.csv', index=False)
print(f'Lote {lote} listo: {n} buscados, {ind} con indicio. Pendientes: {(r.Estado_busqueda=="No buscado").sum()}')
