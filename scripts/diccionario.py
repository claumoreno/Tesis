# -*- coding: utf-8 -*-
"""
Diccionario de variables de los entregables. Se usa para escribir la hoja
"Diccionario" del Excel y la sección de variables del README.

Cada entrada: (tabla, variable, definición, fórmula, cómo se lee, sección del material de Cárdenas)
"""

D = []


def v(tabla, nombre, definicion, formula, lectura, seccion):
    D.append({"tabla": tabla, "variable": nombre, "definicion": definicion,
              "formula": formula, "como_se_lee": lectura, "seccion_material": seccion})


# ---------------------------------------------------------------------------
T = "panel_red_empresa_anio"
v(T, "firm_iden", "Identificador de la empresa tal como viene en la base (incluye '^' si dejó de transarse)", "-", "Llave para unir con datos financieros junto con fiscal_year", "-")
v(T, "company_name", "Nombre de la empresa (sin espacios sobrantes)", "-", "-", "-")
v(T, "fiscal_year", "Año fiscal (FY2010 a FY2024)", "-", "Llave para unir con datos financieros", "-")
v(T, "anio", "Año fiscal en número", "-", "-", "-")
v(T, "empresa_deslistada", "1 si firm_iden contiene '^' (empresa que dejó de transarse en bolsa)", "-", "Panel no balanceado: la empresa sale de la red el año en que deja de aparecer en la base", "-")
v(T, "n_empresas_red_anio", "N° de empresas (nodos) en la red de ese año", "n", "Sirve para comparar indicadores normalizados entre años", "Error 2")
v(T, "n_directores", "N° de directores de la empresa en el año (sin CEO)", "Diagonal de la matriz empresa x empresa", "Tamaño del directorio", "4.1, error 7")
v(T, "n_directores_sin_rut", "N° de directores sin RUT (extranjeros identificados por nombre)", "-", "-", "-")
v(T, "n_directores_interlock", "N° de directores de la empresa que se sientan en 2 o más directorios ese año", "-", "Directores que generan enlaces", "6.3")
v(T, "n_politicos", "N° de directores con pasado político en t", "Suma de politico", "-", "6.8")
v(T, "pct_politicos", "% de directores políticos en el directorio", "100 * n_politicos / n_directores", "-", "6.8")
v(T, "tiene_politico", "1 si la empresa tiene al menos un director político en t", "-", "-", "6.8")
for n, txt in [("N11", "N1.1"), ("N12", "N1.2"), ("N21", "N2.1"), ("N22", "N2.2")]:
    v(T, f"tiene_politico_{n}", f"1 si la empresa tiene al menos un director con cargo de nivel {txt} antes de t", "-", "Un director puede tener varios niveles", "6.8")
for n, txt in [("N11", "N1.1"), ("N12", "N1.2"), ("N21", "N2.1"), ("N22", "N2.2")]:
    v(T, f"n_politicos_{n}", f"N° de directores con cargo de nivel {txt} antes de t", "-", "-", "6.8")
v(T, "n_mujeres", "N° de directoras", "-", "-", "3.3 (atributos)")
v(T, "pct_mujeres", "% de mujeres en el directorio", "100 * n_mujeres / n_directores con género informado", "-", "3.3 (atributos)")
v(T, "grado", "N° de empresas con las que comparte al menos un director (red dicotomizada)", "Ci = Σj aij", "Poder local: más alto, más conexiones directas", "5.16")
v(T, "grado_norm", "Grado normalizado (proporción, multiplicar por 100 para %)", "grado / (n - 1)", "Comparable entre años con distinto n", "5.16")
v(T, "grado_ponderado", "Grado ponderado por intensidad: n° total de directores compartidos con otras empresas", "Σj wij", "No es n° de vecinos; una empresa con 4 vecinos puede sumar 9", "5.16 (intensidad), error 6")
v(T, "intermediacion", "Intermediación bruta (Freeman): veces que la empresa está en los caminos más cortos entre otras dos, repartiendo cuando hay varios caminos", "Σ(s<t) gst(i) / gst", "Poder de conexión o puente. Valor comparable con el 148 de Antofagasta en Cárdenas", "5.18, error 11")
v(T, "intermediacion_norm", "Intermediación normalizada (proporción)", "intermediacion / [(n-1)(n-2)/2]", "0 = nunca es puente; 1 = está en todos los caminos (centro de una estrella)", "5.18")
v(T, "cercania_armonica", "Cercanía armónica: suma de las distancias recíprocas a todas las demás empresas (inalcanzables suman 0)", "Σj 1/dij", "Acceso a la red; se usa porque la red está desconectada y 1/lejanía no se puede calcular", "5.17, error 5")
v(T, "cercania_armonica_norm", "Cercanía armónica normalizada", "cercania_armonica / (n - 1)", "Entre 0 (aislada) y 1 (a un paso de todas)", "5.17, error 5")
v(T, "eigenvector_comp_principal", "Centralidad de vector propio calculada solo dentro del componente principal (norma euclidiana = 1). Vacío fuera del componente principal", "x = (1/λ) A x en el componente principal", "Estar conectada con empresas a su vez centrales. No está definida en redes desconectadas, por eso queda vacía fuera del componente principal (no se completa con 0)", "Omisiones (Bonacich), error 5")
v(T, "punto_corte", "1 si al sacar la empresa la red se divide en más componentes", "Nodo de articulación", "Clave para la cohesión; su salida desconecta a otras empresas", "5.19")
v(T, "en_comp_principal", "1 si la empresa pertenece al componente principal", "-", "-", "5.11")
v(T, "aislado", "1 si la empresa no comparte directores con ninguna otra", "grado = 0", "-", "5.10")
v(T, "tam_componente", "N° de empresas del componente al que pertenece la empresa (1 si es aislada)", "-", "-", "5.11")
v(T, "n_vecinos_con_politico", "N° de empresas vecinas (a un paso) que tienen director político en t", "Σj aij · politicoj", "Exposición política indirecta a través de la red", "6.8 (lógica de exposición)")
v(T, "pct_vecinos_con_politico", "% de las empresas vecinas con director político. Vacío si la empresa es aislada (no tiene vecinos)", "100 * n_vecinos_con_politico / grado", "-", "6.8")
v(T, "dist_min_empresa_con_politico", "Distancia geodésica mínima a OTRA empresa con director político. Vacío si no hay camino", "min dij, j ≠ i con politicoj = 1", "1 = vecina directa de una empresa con político", "2 (distancia), 6.8")
v(T, "puente_politico", "1 si la empresa está unida a otra a través de un director político (el político se sienta en ambos directorios)", "∃ j: wpol_ij > 0", "El político es el puente del enlace", "6.8")
v(T, "n_vecinos_via_politico", "N° de empresas con las que comparte al menos un director político", "#{j: wpol_ij > 0}", "-", "6.8")
v(T, "n_vecinos_solo_via_politico", "N° de empresas con las que el ÚNICO vínculo son directores políticos", "#{j: wpol_ij = wij > 0}", "Enlaces que desaparecerían sin el político", "6.8")

# ---------------------------------------------------------------------------
T = "panel_red_director_anio"
v(T, "id_director", "ID del director: RUT sin puntos ni guion (K mayúscula) o, si no tiene RUT, el nombre normalizado", "-", "-", "Error 7 (ID único)")
v(T, "nombre_director", "Nombre del director en la base", "-", "-", "-")
v(T, "fiscal_year / anio", "Año fiscal", "-", "-", "-")
v(T, "sin_rut", "1 si el director no tiene RUT (se identifica por nombre)", "-", "Nunca se clasifica como político", "-")
v(T, "genero", "Género (M/F)", "-", "-", "3.3")
v(T, "politico", "1 si el director tiene pasado político en t (columna 'Pasado político antes del año' del cruce)", "-", "-", "6.8")
v(T, "politico_N11 ... politico_N22", "1 si tuvo un cargo de ese nivel antes de t", "-", "Pueden ser varios a la vez", "6.8")
v(T, "n_directorios", "N° de directorios en que se sienta en t (sin contar cargos de CEO)", "Diagonal de la matriz director x director", "Director con más asientos = conector", "6.3")
v(T, "empresas", "Lista de firm_iden de sus directorios en t", "-", "-", "-")
v(T, "preside_algun_directorio", "1 si es D#/CHAIRMAN en alguna empresa (informativo; se trata como director normal)", "-", "-", "-")
v(T, "grado_red_directores", "N° de directores distintos con los que comparte al menos un directorio", "Σj aij en la red director x director", "Poder local del director", "5.16")
v(T, "grado_norm_red_directores", "Grado normalizado en la red de directores", "grado / (n - 1)", "-", "5.16")
v(T, "intermediacion_red_directores", "Intermediación bruta en la red de directores", "Σ gst(i)/gst", "Directores que unen directorios distintos", "5.18")
v(T, "intermediacion_norm_red_directores", "Intermediación normalizada en la red de directores", "bruta / [(n-1)(n-2)/2]", "-", "5.18")

# ---------------------------------------------------------------------------
T = "cohesion_por_anio"
v(T, "n_nodos", "N° de empresas en la red del año", "n", "Siempre reportar junto a cada indicador", "Error 2")
v(T, "n_enlaces", "N° de pares de empresas que comparten al menos un director (n° de interlocks)", "L", "-", "5.5, tabla de cinco países")
v(T, "densidad", "Proporción de enlaces existentes sobre los posibles (red dicotomizada)", "L / [n(n-1)/2]", "↑ cohesión. Baja mecánicamente si n crece", "5.5, errores 1 y 6")
v(T, "grado_medio", "Promedio de empresas vecinas por empresa", "2L / n = densidad × (n-1)", "↑ cohesión. Más comparable que la densidad si n cambia", "5.6, error 3")
v(T, "desv_est_grado", "Desviación estándar del grado (poblacional)", "sd(Ci)", "Dispersión de las conexiones", "Tabla de cinco países (5.13)")
v(T, "n_componentes", "N° de componentes (débiles; la red no es dirigida). Un aislado es un componente", "-", "↓ cohesión", "5.11")
v(T, "ratio_componentes", "Ratio de componentes", "(c - 1) / (n - 1)", "0 = un solo componente; 1 = todos aislados. ↑ fragmentación", "5.11")
v(T, "tam_comp_principal", "N° de empresas en el componente principal", "-", "-", "5.11")
v(T, "pct_comp_principal", "% de empresas en el componente principal", "100 × tam / n", "↑ inclusión y cohesión", "5.11")
v(T, "n_aislados / pct_aislados", "N° y % de empresas sin ningún director compartido", "100 × aislados / n", "↓ cohesión", "5.10")
v(T, "conectividad", "Connectedness: proporción de pares de empresas que se alcanzan por algún camino", "Σcomp s(s-1)/2 / [n(n-1)/2]", "0 a 1. Funciona con aislados", "6.3")
v(T, "compacidad", "Media de las distancias recíprocas entre todos los pares (inalcanzables = 0)", "Σ(i≠j) (1/dij) / [n(n-1)]", "0 a 1. ↑ compacidad. Tolera la desconexión", "5.8, 6.3, error 4")
v(T, "coef_agrupamiento_global", "Proporción de tríadas cerradas (transitividad)", "3 × triángulos / tríadas conectadas", "Cohesión local", "6.3")
v(T, "centralizacion_grado", "Centralización de grado de Freeman (red dicotomizada y simétrica)", "Σ(Cmax - Ci) / [(n-1)(n-2)]", "% de la centralización de una estrella perfecta (no es una probabilidad). Mide dependencia de pocos actores, no más cohesión", "5.12, errores 8 y 9")
v(T, "pct_alcanzabilidad_actor_mas_central", "% de empresas que la empresa de mayor grado alcanza a un paso", "100 × Cmax / (n-1)", "↑ centralización", "5.12 (otros indicadores)")
v(T, "n_puntos_corte / pct_puntos_corte", "N° y % de empresas cuya salida divide la red", "100 × cortes / n", "↑ fragilidad, ↓ cohesión (robustez)", "5.12, 5.19")
v(T, "distancia_media_comp_principal", "Distancia geodésica media SOLO dentro del componente principal", "Σ dij / [m(m-1)] con m = tam_comp_principal", "↓ cohesión. No se calcula para toda la red porque está desconectada", "5.7, error 4")
v(T, "diametro_comp_principal", "Diámetro SOLO dentro del componente principal", "max dij en el componente principal", "↓ cohesión", "5.8, error 4")
v(T, "total_directores_compartidos", "Suma de las intensidades de todos los enlaces (intensidad, reportada aparte)", "Σ(i<j) wij", "Multiplicidad", "Error 6")
v(T, "intensidad_media_por_enlace", "N° medio de directores compartidos por par conectado", "Σ wij / L", "Multiplicidad", "Error 6")
v(T, "pct_relaciones_multiples", "% de enlaces con 2 o más directores compartidos", "100 × #{wij ≥ 2} / L", "↑ multiplicidad, ↑ cohesión", "5.12 (otros indicadores), error 6")
v(T, "red_dir_*", "N° de nodos, enlaces, densidad, grado medio y % en componente principal de la red director x director", "Mismas fórmulas", "Contexto", "4.1")
v(T, "n_empresas_con_politico / pct_empresas_con_politico", "N° y % de empresas con al menos un director político", "-", "-", "6.8")
v(T, "n_enlaces_via_politico / pct_enlaces_via_politico", "N° y % de enlaces en que al menos un director compartido es político", "-", "Peso de los políticos en la cohesión", "6.8")
v(T, "indice_cohesion_acp", "Índice de cohesión: puntaje del 1er componente principal de conectividad, densidad, grado medio, ratio de componentes, % comp. principal, % aislados y compacidad (estandarizados, 15 años)", "z · v1 / √λ1", "Media 0 y desviación 1 en el período. ↑ cohesión. Solo compara años entre sí", "6.3")

# ---------------------------------------------------------------------------
T = "comparacion_politicos_vs_no_politicos"
v(T, "nivel", "director: directores políticos vs no políticos; empresa: empresas con vs sin director político", "-", "-", "5.20, omisiones (comparación estadística)")
v(T, "periodo", "Año o pool de todos los años", "-", "En el pool las observaciones no son independientes (misma persona en varios años)", "-")
v(T, "muestra", "Grupo de comparación usado", "-", "'solo directores con RUT' excluye a los extranjeros, que nunca son políticos", "-")
v(T, "media_*, mediana_*, diferencia_medias", "Estadísticos descriptivos por grupo", "media políticos - media no políticos", "-", "-")
v(T, "t_welch / p_welch", "Test t de Welch (test principal)", "t = (x̄1 - x̄2) / √(s1²/n1 + s2²/n2)", "p < 0,05: diferencia de medias significativa al 5%", "-")
v(T, "p_mann_whitney", "Test de Mann-Whitney (robustez, no paramétrico)", "-", "Robusto a la asimetría y a los muchos ceros de la intermediación", "-")
v(T, "p_permutacion", "Test de permutación de la diferencia de medias (5.000 permutaciones de la etiqueta político)", "-", "No supone normalidad; apropiado para datos de redes", "-")
