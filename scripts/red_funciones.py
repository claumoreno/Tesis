# -*- coding: utf-8 -*-
"""
Funciones de análisis de redes para la red de interlocking de directores.

Todas las definiciones siguen el material de Julián Cárdenas
(Material_Analisis_de_Redes_Julian_Cardenas.docx), ya con las correcciones
del capítulo "Errores, imprecisiones y omisiones del curso":

- Densidad no dirigida = L / [n(n-1)/2]                     (5.5, error 1)
- Grado medio = 2L / n = densidad * (n-1)                  (5.6, error 3)
- Distancia media y diámetro solo dentro del componente
  principal, porque la red está desconectada               (5.7, 5.8, error 4)
- Compacidad = media de 1/d con pares inalcanzables = 0    (5.8, 6.3)
- Conectividad = 1 - proporción de pares no alcanzables    (6.3)
- Ratio de componentes = (c - 1) / (n - 1)                  (5.11)
- Centralización de grado = Σ(Cmax - Ci) / [(n-1)(n-2)]    (5.12, error 8)
- Cercanía armónica (suma de 1/d) en vez de 1/lejanía      (5.17, error 5)
- Indicadores calculados con la matriz dicotomizada; la
  intensidad se reporta aparte                             (5.5, 6.2, error 6)
- Proyección 2 modos -> 1 modo con diagonal en 0           (4.1, error 7)
"""

import re
import unicodedata
from itertools import combinations

import networkx as nx
import numpy as np
import pandas as pd


# ---------------------------------------------------------------------------
# 1. Limpieza de identificadores
# ---------------------------------------------------------------------------

def normalizar_texto(texto):
    """Mayúsculas, sin tildes y sin espacios dobles."""
    if pd.isna(texto):
        return np.nan
    t = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    t = re.sub(r"\s+", " ", t.upper()).strip()
    return t


def digito_verificador(cuerpo):
    """Dígito verificador de un RUT chileno (algoritmo módulo 11)."""
    suma, factor = 0, 2
    for d in reversed(cuerpo):
        suma += int(d) * factor
        factor = 2 if factor == 7 else factor + 1
    resto = 11 - suma % 11
    return {11: "0", 10: "K"}.get(resto, str(resto))


def normalizar_rut(valor):
    """
    Devuelve el RUT normalizado (sin puntos ni guion, K mayúscula) si el valor
    es un RUT válido, o None si no lo es.

    Se considera RUT válido: entre 6 y 8 dígitos, un dígito verificador
    (0-9 o K) y que el dígito verificador calce con el algoritmo módulo 11.
    """
    if pd.isna(valor):
        return None
    s = re.sub(r"[\.\s]", "", str(valor)).upper()
    m = re.fullmatch(r"(\d{6,8})-?([\dK])", s)
    if not m:
        return None
    cuerpo, dv = m.groups()
    if digito_verificador(cuerpo) != dv:
        return None
    return cuerpo + dv


def identificador_director(director_iden, name_director):
    """
    Regla 3 de limpieza:
    - RUT válido -> RUT normalizado, sin_rut = 0.
    - No es RUT (directores extranjeros, viene el nombre) -> nombre normalizado
      como ID, sin_rut = 1. Si director_iden no es RUT pero contiene números
      (no es un nombre), se usa el nombre del director (name_director).
    """
    rut = normalizar_rut(director_iden)
    if rut is not None:
        return rut, 0
    texto = normalizar_texto(director_iden)
    if texto is None or pd.isna(texto) or re.search(r"\d", texto):
        texto = normalizar_texto(name_director)
    return texto, 1


# ---------------------------------------------------------------------------
# 2. Construcción de redes
# ---------------------------------------------------------------------------

def matriz_dos_modos(df, col_director="id_director", col_empresa="firm_iden"):
    """Matriz de afiliación director x empresa (1 si el director está en la empresa)."""
    a = pd.crosstab(df[col_director], df[col_empresa])
    return (a > 0).astype(int)


def proyectar(matriz_2m):
    """
    Proyección de la matriz de 2 modos (directores x empresas), sección 4.1 y error 7.

    Empresas x empresas = A' A : fuera de la diagonal, n° de directores compartidos
    (intensidad); en la diagonal, n° de directores de cada empresa.
    Directores x directores = A A' : fuera de la diagonal, n° de directorios
    compartidos; en la diagonal, n° de directorios de cada director.
    Devuelve las dos matrices valoradas CON su diagonal (para documentarla).
    """
    a = matriz_2m.values
    emp = pd.DataFrame(a.T @ a, index=matriz_2m.columns, columns=matriz_2m.columns)
    dirs = pd.DataFrame(a @ a.T, index=matriz_2m.index, columns=matriz_2m.index)
    return emp, dirs


def grafo_desde_matriz(m):
    """
    Grafo no dirigido a partir de una matriz cuadrada valorada.
    La diagonal se ignora (se deja en 0, error 7). El atributo 'weight' guarda
    la intensidad; la existencia de la arista es la versión dicotomizada.
    """
    g = nx.Graph()
    g.add_nodes_from(m.index)
    v = m.values.copy()
    np.fill_diagonal(v, 0)
    filas, cols = np.nonzero(np.triu(v, k=1))
    nombres = list(m.index)
    for i, j in zip(filas, cols):
        g.add_edge(nombres[i], nombres[j], weight=int(v[i, j]))
    return g


def binaria(g):
    """Copia dicotomizada del grafo (todas las aristas valen 1)."""
    h = nx.Graph()
    h.add_nodes_from(g.nodes())
    h.add_edges_from(g.edges())
    return h


# ---------------------------------------------------------------------------
# 3. Cohesión global (Módulo 5A y 6.3)
# ---------------------------------------------------------------------------

def densidad(n, enlaces):
    """Densidad de una red no dirigida, L / [n(n-1)/2] (error 1)."""
    posibles = n * (n - 1) / 2
    return enlaces / posibles if posibles > 0 else np.nan


def grado_medio(n, enlaces):
    """Grado medio en red no dirigida = 2L / n (error 3)."""
    return 2 * enlaces / n if n > 0 else np.nan


def centralizacion_grado(g):
    """Centralización de grado de Freeman, Σ(Cmax - Ci) / [(n-1)(n-2)] (5.12, error 8)."""
    n = g.number_of_nodes()
    if n < 3:
        return np.nan
    grados = np.array([d for _, d in g.degree()])
    return (grados.max() - grados).sum() / ((n - 1) * (n - 2))


def distancias_todas(g):
    """Diccionario {nodo: {nodo: distancia}} con todas las distancias geodésicas."""
    return dict(nx.all_pairs_shortest_path_length(g))


def compacidad(g, dist=None):
    """Media de las distancias recíprocas sobre los n(n-1) pares ordenados; inalcanzables = 0."""
    n = g.number_of_nodes()
    if n < 2:
        return np.nan
    dist = dist if dist is not None else distancias_todas(g)
    suma = sum(1 / d for u, dd in dist.items() for v, d in dd.items() if u != v)
    return suma / (n * (n - 1))


def conectividad(g):
    """Connectedness = proporción de pares (no ordenados) que se alcanzan por algún camino."""
    n = g.number_of_nodes()
    if n < 2:
        return np.nan
    alcanzables = sum(len(c) * (len(c) - 1) / 2 for c in nx.connected_components(g))
    return alcanzables / (n * (n - 1) / 2)


def componente_principal(g):
    """Conjunto de nodos del componente de mayor tamaño."""
    if g.number_of_nodes() == 0:
        return set()
    return max(nx.connected_components(g), key=len)


def cohesion_global(g_valorado):
    """
    Indicadores de cohesión de una red no dirigida. Los indicadores se calculan
    sobre la versión dicotomizada; la intensidad se reporta aparte (error 6).
    """
    g = binaria(g_valorado)
    n = g.number_of_nodes()
    L = g.number_of_edges()
    grados = np.array([d for _, d in g.degree()]) if n else np.array([])
    comps = list(nx.connected_components(g))
    principal = componente_principal(g)
    sub = g.subgraph(principal)
    aislados = list(nx.isolates(g))
    cortes = list(nx.articulation_points(g))
    pesos = np.array([d["weight"] for _, _, d in g_valorado.edges(data=True)]) if L else np.array([])

    r = {
        "n_nodos": n,
        "n_enlaces": L,
        "densidad": densidad(n, L),
        "grado_medio": grado_medio(n, L),
        "desv_est_grado": grados.std(ddof=0) if n else np.nan,
        "n_componentes": len(comps),
        "ratio_componentes": (len(comps) - 1) / (n - 1) if n > 1 else np.nan,
        "tam_comp_principal": len(principal),
        "pct_comp_principal": 100 * len(principal) / n if n else np.nan,
        "n_aislados": len(aislados),
        "pct_aislados": 100 * len(aislados) / n if n else np.nan,
        "conectividad": conectividad(g),
        "compacidad": compacidad(g),
        "coef_agrupamiento_global": nx.transitivity(g),
        "centralizacion_grado": centralizacion_grado(g),
        "pct_alcanzabilidad_actor_mas_central": 100 * grados.max() / (n - 1) if n > 1 else np.nan,
        "n_puntos_corte": len(cortes),
        "pct_puntos_corte": 100 * len(cortes) / n if n else np.nan,
        "distancia_media_comp_principal": (
            nx.average_shortest_path_length(sub) if len(principal) > 1 else np.nan),
        "diametro_comp_principal": nx.diameter(sub) if len(principal) > 1 else np.nan,
        # Intensidad (multiplicidad), reportada aparte de los indicadores binarios
        "total_directores_compartidos": int(pesos.sum()) if L else 0,
        "intensidad_media_por_enlace": pesos.mean() if L else np.nan,
        "pct_relaciones_multiples": 100 * (pesos >= 2).mean() if L else np.nan,
    }
    return r


# ---------------------------------------------------------------------------
# 4. Centralidad (Módulo 5B)
# ---------------------------------------------------------------------------

def centralidad_nodos(g_valorado):
    """
    Indicadores de centralidad por nodo. Grado, intermediación, cercanía y punto
    de corte se calculan sobre la red dicotomizada; el grado ponderado usa la
    intensidad. Eigenvector solo dentro del componente principal (NaN fuera).
    """
    g = binaria(g_valorado)
    n = g.number_of_nodes()
    grado = dict(g.degree())
    grado_pond = dict(g_valorado.degree(weight="weight"))
    inter_bruta = nx.betweenness_centrality(g, normalized=False)
    inter_norm = nx.betweenness_centrality(g, normalized=True) if n > 2 else {v: np.nan for v in g}
    armonica = nx.harmonic_centrality(g)
    cortes = set(nx.articulation_points(g))
    principal = componente_principal(g)
    comp_de = {}
    for c in nx.connected_components(g):
        for v in c:
            comp_de[v] = len(c)
    eig = {}
    if len(principal) > 2:
        eig = nx.eigenvector_centrality_numpy(g.subgraph(principal))
    filas = []
    for v in g.nodes():
        filas.append({
            "nodo": v,
            "grado": grado[v],
            "grado_norm": grado[v] / (n - 1) if n > 1 else np.nan,
            "grado_ponderado": grado_pond[v],
            "intermediacion": inter_bruta[v],
            "intermediacion_norm": inter_norm[v],
            "cercania_armonica": armonica[v],
            "cercania_armonica_norm": armonica[v] / (n - 1) if n > 1 else np.nan,
            "eigenvector_comp_principal": eig.get(v, np.nan),
            "punto_corte": int(v in cortes),
            "en_comp_principal": int(v in principal),
            "aislado": int(grado[v] == 0),
            "tam_componente": comp_de[v],
        })
    return pd.DataFrame(filas)


def centralidad_directores(g_valorado):
    """Grado e intermediación en la red director x director (dicotomizada)."""
    g = binaria(g_valorado)
    n = g.number_of_nodes()
    grado = dict(g.degree())
    inter = nx.betweenness_centrality(g, normalized=False)
    inter_n = nx.betweenness_centrality(g, normalized=True)
    return pd.DataFrame({
        "nodo": list(g.nodes()),
        "grado_red_directores": [grado[v] for v in g.nodes()],
        "grado_norm_red_directores": [grado[v] / (n - 1) for v in g.nodes()],
        "intermediacion_red_directores": [inter[v] for v in g.nodes()],
        "intermediacion_norm_red_directores": [inter_n[v] for v in g.nodes()],
    })


# ---------------------------------------------------------------------------
# 5. Tests de diferencia de medias
# ---------------------------------------------------------------------------

def comparar_grupos(x_si, x_no, n_perm=5000, semilla=12345):
    """
    Compara medias de dos grupos.
    - Welch t-test (no asume varianzas iguales; grupos de tamaño muy distinto).
    - Mann-Whitney U (robustez, distribuciones muy asimétricas con muchos ceros).
    - Test de permutación de la diferencia de medias (no supone normalidad ni
      independencia distribucional; se permutan las etiquetas dentro del año).
    """
    from scipy import stats
    x_si = np.asarray(x_si, dtype=float)
    x_no = np.asarray(x_no, dtype=float)
    x_si = x_si[~np.isnan(x_si)]
    x_no = x_no[~np.isnan(x_no)]
    r = {"n_politicos": len(x_si), "n_no_politicos": len(x_no),
         "media_politicos": x_si.mean() if len(x_si) else np.nan,
         "media_no_politicos": x_no.mean() if len(x_no) else np.nan,
         "mediana_politicos": np.median(x_si) if len(x_si) else np.nan,
         "mediana_no_politicos": np.median(x_no) if len(x_no) else np.nan}
    r["diferencia_medias"] = r["media_politicos"] - r["media_no_politicos"]
    if len(x_si) >= 2 and len(x_no) >= 2:
        t = stats.ttest_ind(x_si, x_no, equal_var=False)
        r["t_welch"], r["p_welch"] = t.statistic, t.pvalue
        u = stats.mannwhitneyu(x_si, x_no, alternative="two-sided")
        r["p_mann_whitney"] = u.pvalue
        rng = np.random.default_rng(semilla)
        todos = np.concatenate([x_si, x_no])
        k = len(x_si)
        obs = abs(r["diferencia_medias"])
        cuenta = 0
        for _ in range(n_perm):
            p = rng.permutation(todos)
            if abs(p[:k].mean() - p[k:].mean()) >= obs - 1e-12:
                cuenta += 1
        r["p_permutacion"] = (cuenta + 1) / (n_perm + 1)
    else:
        r.update({"t_welch": np.nan, "p_welch": np.nan,
                  "p_mann_whitney": np.nan, "p_permutacion": np.nan})
    return r
