import pandas as pd, sys
W = sys.argv[1]
per = pd.read_csv(f'{W}/personas.csv', keep_default_na=False)
def consulta(v):
    vs = [x.strip() for x in v.split(' ; ')]
    return '(' + ' OR '.join(f'"{x}"' for x in vs) + ') (seremi OR "secretario regional ministerial")'
res = pd.DataFrame({'ID_persona': per.ID_persona, 'Orden': per.Orden, 'Tramo': per.Tramo,
                    'Nombre_busqueda': per.Nombre_busqueda, 'Consulta_usada': per.Variantes_busqueda.map(consulta),
                    'Fecha_busqueda': '', 'Estado_busqueda': 'No buscado', 'Notas': '', 'Cargos_json': ''})
res.to_csv(f'{W}/resultados_parciales.csv', index=False)
print(len(res))
