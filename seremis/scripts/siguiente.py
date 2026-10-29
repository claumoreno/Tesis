import pandas as pd, sys
W, n = sys.argv[1], int(sys.argv[2])
r = pd.read_csv(f'{W}/resultados_parciales.csv', keep_default_na=False)
p = r[r.Estado_busqueda == 'No buscado'].sort_values('Orden').head(n)
for x in p.itertuples(): print(x.ID_persona, x.Consulta_usada, sep='\t')
print('pendientes:', (r.Estado_busqueda == 'No buscado').sum())
