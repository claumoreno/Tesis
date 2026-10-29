import pandas as pd, sys
W = sys.argv[1]
b = pd.read_csv(f'{W}/personas.csv', keep_default_na=False).set_index('ID_persona')
r = pd.read_csv(f'{W}/resultados_parciales.csv', keep_default_na=False, dtype=str)
def consulta(v):
    vs = [x.strip() for x in v.split(' ; ')]
    return '(' + ' OR '.join(f'"{x}"' for x in vs) + ') (seremi OR "secretario regional ministerial")'
m = r.Estado_busqueda == 'No buscado'
r.loc[m, 'Consulta_usada'] = b.loc[r.ID_persona[m], 'Variantes_busqueda'].map(consulta).values
r.to_csv(f'{W}/resultados_parciales.csv', index=False)
