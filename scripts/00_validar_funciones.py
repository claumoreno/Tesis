# -*- coding: utf-8 -*-
"""
ETAPA 6 (parte 1). Validación de las funciones con los ejemplos del material de
Cárdenas ANTES de usarlas sobre la base real.

Si algún ejemplo no da el valor esperado, el script se detiene con error.
Los resultados quedan en output/validacion_funciones.csv.
"""

from pathlib import Path

import networkx as nx
import numpy as np
import pandas as pd

import red_funciones as rf

BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "output"
OUT.mkdir(exist_ok=True)

resultados = []


def chequear(nombre, obtenido, esperado, tol=0.005, fuente=""):
    ok = bool(np.isclose(obtenido, esperado, atol=tol))
    resultados.append({"prueba": nombre, "esperado": esperado,
                       "obtenido": round(float(obtenido), 4), "ok": ok,
                       "fuente_material": fuente})
    print(f"[{'OK' if ok else 'FALLA'}] {nombre}: esperado {esperado}, obtenido {obtenido:.4f}")


# --- Ejemplo 1. Red amarilla de 8 actores y 7 enlaces (5.5, 5.7, 5.8, errores 1 y 3)
g8 = nx.Graph()
g8.add_edges_from([(8, 2), (7, 2), (2, 1), (1, 3), (1, 4), (4, 6), (4, 5)])
for u, v in g8.edges():
    g8[u][v]["weight"] = 1
c8 = rf.cohesion_global(g8)
chequear("Red 8 actores: n° enlaces", c8["n_enlaces"], 7, fuente="5.5")
chequear("Red 8 actores: densidad = 7/28", c8["densidad"], 0.25, fuente="5.5 y error 1")
chequear("Red 8 actores: grado medio = 2L/n", c8["grado_medio"], 1.75, fuente="5.6 y error 3")
chequear("Red 8 actores: grado medio = densidad*(n-1)", c8["densidad"] * 7, c8["grado_medio"], fuente="error 3")
chequear("Red 8 actores: distancia geodésica media (130/56)", c8["distancia_media_comp_principal"], 2.32, fuente="5.7")
chequear("Red 8 actores: diámetro", c8["diametro_comp_principal"], 4, fuente="5.8")
chequear("Red 8 actores: compacidad = eficiencia global", c8["compacidad"], nx.global_efficiency(g8), tol=1e-9, fuente="5.8")
chequear("Red 8 actores: conectividad (red conexa)", c8["conectividad"], 1.0, fuente="6.3")

# --- Ejemplo 2. Red de 6 nodos de centralidad (5.16, 5.17, 5.18)
g6 = nx.Graph()
g6.add_edges_from([(1, 6), (1, 4), (1, 2), (1, 3), (5, 2), (5, 3), (5, 4), (2, 3)])
for u, v in g6.edges():
    g6[u][v]["weight"] = 1
cen6 = rf.centralidad_nodos(g6).set_index("nodo")
for nodo, esp in {1: 4, 2: 3, 3: 3, 4: 2, 5: 3, 6: 1}.items():
    chequear(f"Red 6 nodos: grado nodo {nodo}", cen6.loc[nodo, "grado"], esp, fuente="5.16")
for nodo, esp in {1: 5, 2: 0.667, 3: 0.667, 4: 0.667, 5: 1, 6: 0}.items():
    chequear(f"Red 6 nodos: intermediación nodo {nodo}", cen6.loc[nodo, "intermediacion"], esp, fuente="5.18 y error 11")
dist6 = rf.distancias_todas(g6)
for nodo, esp in {1: 6, 2: 7, 3: 7, 4: 8, 5: 8, 6: 10}.items():
    chequear(f"Red 6 nodos: lejanía nodo {nodo}", sum(dist6[nodo].values()), esp, fuente="5.17")
# intermediación normalizada = bruta / [(n-1)(n-2)/2]
chequear("Red 6 nodos: intermediación normalizada nodo 1 = 5/10",
         cen6.loc[1, "intermediacion_norm"], 0.5, fuente="5.18 (normalización UCINET)")
chequear("Red 6 nodos: nodo 1 es el más cercano (cercanía armónica máxima)",
         float(cen6["cercania_armonica"].idxmax()), 1, fuente="5.17 y error 5")

# --- Ejemplo 3. Centralización de grado (5.12, error 8)
estrella = nx.star_graph(4)                      # 5 nodos, grados 4,1,1,1,1
chequear("Estrella de 5 nodos: centralización", rf.centralizacion_grado(estrella), 1.0, fuente="pregunta de repaso 14")
linea = nx.path_graph(5)                         # grados 1,2,2,2,1
chequear("Línea de 5 nodos: centralización", rf.centralizacion_grado(linea), 0.167, fuente="5.12")
g7 = nx.cycle_graph(7)
g7.add_edge(0, 3)                                # grados 3,2,2,3,2,2,2
chequear("Red de 7 nodos (grados 2,2,3,2,3,2,2): centralización", rf.centralizacion_grado(g7), 0.167, fuente="5.12")

# --- Ejemplo 4. Componentes: 20 actores, 6 componentes, principal de 12 (5.11)
gc = nx.path_graph(12)
gc.add_edges_from([(12, 13), (13, 14), (14, 15)])
gc.add_nodes_from([16, 17, 18, 19])
for u, v in gc.edges():
    gc[u][v]["weight"] = 1
ccomp = rf.cohesion_global(gc)
chequear("20 actores: n° de componentes", ccomp["n_componentes"], 6, fuente="5.11")
chequear("20 actores: ratio de componentes (6-1)/(20-1)", ccomp["ratio_componentes"], 0.26, fuente="5.11")
chequear("20 actores: % en componente principal", ccomp["pct_comp_principal"], 60, fuente="5.11")
chequear("20 actores: % aislados", ccomp["pct_aislados"], 20, fuente="5.10")
chequear("20 actores: conectividad = (66+6)/190", ccomp["conectividad"], 72 / 190, tol=1e-9, fuente="6.3")

# --- Ejemplo 5. Pregunta de repaso 8 y 9: 10 actores y 9 relaciones
g10 = nx.path_graph(10)
for u, v in g10.edges():
    g10[u][v]["weight"] = 1
c10 = rf.cohesion_global(g10)
chequear("10 actores y 9 relaciones: densidad", c10["densidad"], 0.2, fuente="pregunta de repaso 8")
chequear("10 actores y 9 relaciones: grado medio", c10["grado_medio"], 1.8, fuente="pregunta de repaso 9")

# --- Ejemplo 6. Proyección de 2 modos (4.1, error 7). Personas x sindicatos
afil = pd.DataFrame({"id_director": ["Pedro", "Juan", "Pilar", "Luis"],
                     "firm_iden": ["UGT", "CCOO", "UGT", "UGT"]})
m2 = rf.matriz_dos_modos(afil)
emp, per = rf.proyectar(m2)
chequear("Proyección: diagonal UGT = n° de miembros", emp.loc["UGT", "UGT"], 3, fuente="4.1")
chequear("Proyección: CCOO-UGT = 0 (nadie en ambos)", emp.loc["CCOO", "UGT"], 0, fuente="4.1")
chequear("Proyección: Pedro-Pilar = 1", per.loc["Pedro", "Pilar"], 1, fuente="4.1")
gp = rf.grafo_desde_matriz(per)
chequear("Proyección: diagonal excluida (sin lazos)", nx.number_of_selfloops(gp), 0, fuente="error 7")
# intensidad: dos empresas que comparten dos directores (ejemplo ACS-Acerinox)
afil2 = pd.DataFrame({"id_director": ["Aguirre", "Aguirre", "Martinez", "Martinez", "Blesa", "Blesa"],
                      "firm_iden": ["ACS", "Acerinox", "ACS", "Acerinox", "ACS", "Endesa"]})
emp2, _ = rf.proyectar(rf.matriz_dos_modos(afil2))
chequear("Proyección: ACS-Acerinox = 2 directivos compartidos", emp2.loc["ACS", "Acerinox"], 2, fuente="4.1 (España)")
chequear("Proyección: ACS-Endesa = 1 directivo compartido", emp2.loc["ACS", "Endesa"], 1, fuente="4.1 (España)")

# --- Ejemplo 7. Normalización de RUT
chequear("RUT '15.548.765-8' se normaliza", float(rf.normalizar_rut("15.548.765-8") == "155487658"), 1)
chequear("RUT con dígito verificador erróneo no es válido", float(rf.normalizar_rut("15.548.765-1") is None), 1)
chequear("Nombre extranjero no es RUT", float(rf.normalizar_rut("DAVID LEGHER") is None), 1)
chequear("Nombre normalizado sin tildes", float(rf.normalizar_texto("  José  Ñuñez ") == "JOSE NUNEZ"), 1)

tabla = pd.DataFrame(resultados)
tabla.to_csv(OUT / "validacion_funciones.csv", index=False, encoding="utf-8-sig")
n_fallas = (~tabla["ok"]).sum()
print(f"\n{len(tabla)} pruebas, {n_fallas} fallas")
if n_fallas:
    raise SystemExit("Hay pruebas que fallan: revisar antes de calcular sobre la base real.")
