# Red de interlocking de empresas chilenas con directores políticos, FY2010–FY2024

Este directorio contiene la red de empresas unidas por directores compartidos (una red por año), todos los indicadores de cohesión y de centralidad, las variables políticas de red y un panel empresa-año listo para unir con datos financieros por `firm_iden` + `fiscal_year`.

Las definiciones siguen el *Material de Análisis de Redes* de Julián Cárdenas (en adelante, "el material"), con las correcciones de su capítulo *Errores, imprecisiones y omisiones del curso*. Cada decisión cita la sección en que se apoya.

## Cómo reproducir

Desde la carpeta raíz del proyecto (donde están `new_interlocking2.xlsx` y `Cruce_politicos_interlocking.xlsx`):

```bash
pip install pandas networkx scipy openpyxl matplotlib
```

```bash
python scripts/ejecutar_todo.py
```

`ejecutar_todo.py` corre en orden:

| Script | Etapa | Qué hace |
|---|---|---|
| `scripts/00_validar_funciones.py` | 6 (parte 1) | Prueba las funciones con los ejemplos del material antes de tocar la base real. Se detiene si algo falla |
| `scripts/01_limpieza_diagnostico.py` | 1 | Limpieza, cruce de políticos y diagnóstico |
| `scripts/02_red_indicadores.py` | 2 a 5 | Matrices de 2 modos, proyecciones, cohesión, centralidad, variables políticas y comparación |
| `scripts/03_validacion_panel.py` | 6 (parte 2) | Valores imposibles, duplicados y cobertura del panel |
| `scripts/04_entregables.py` | 7 | Excel, archivos de Gephi, gráficos y este README |
| `scripts/red_funciones.py` | — | Funciones de red (comentadas, con las fórmulas) |
| `scripts/diccionario.py` | — | Diccionario de variables (alimenta el Excel y este README) |

Todas las rutas son relativas a la carpeta del proyecto. El proceso completo tarda unos dos minutos.

## Archivos generados

| Archivo | Contenido |
|---|---|
| `panel_red_empresa_anio.csv` | Panel empresa-año (3.026 filas): atributos del directorio, centralidad y variables políticas de red |
| `panel_red_director_anio.csv` | Panel director-año (15.707 filas): atributos, n° de directorios y centralidad en la red director × director |
| `cohesion_por_anio.csv` | Cohesión global de la red de empresas, una fila por año |
| `comparacion_politicos_vs_no_politicos.csv` | Medias y tests de diferencia por año y en pool |
| `diagnostico.csv` | Conteos por año de la etapa 1 |
| `diagnostico_cruce.csv` | Resumen de la limpieza y verificación del cruce de políticos |
| `problemas_base.csv` | Casos de la base que conviene revisar a mano |
| `validacion_funciones.csv`, `validacion_panel.csv` | Resultados de la etapa 6 |
| `resultados_red.xlsx` | Todas las tablas anteriores en hojas separadas, con hoja `Indice` y hoja `Diccionario` |
| `gephi/red_empresas_FY####.gexf` | Una red por año para Gephi |
| `graficos/red_2010.png`, `graficos/red_2024.png` | Sociogramas de 2010 y 2024 |
| `graficos/evolucion_cohesion.png` | Evolución de 12 indicadores de cohesión |
| `graficos/evolucion_politicos.png` | % de empresas con director político y % de enlaces que pasan por un político |
| `redes_por_anio/` | Por año: matriz de 2 modos director × empresa, matriz empresa × empresa valorada (con diagonal), lista de enlaces empresa–empresa (con n° de directores políticos compartidos) y lista de enlaces director–director |
| `intermedios/` | Base limpia director-empresa-año, cargas del índice de cohesión y grafos serializados |
| `resumen_resultados.md` | Hallazgos descriptivos en lenguaje simple |

## Reglas de limpieza (decisiones de la autora, 10 nov 2026)

1. **Se excluyen todas las filas con `director = "CEO"`** (3.026 filas, una por empresa-año), incluidos los políticos que aparecen como CEO. El material deja abierto si se incluye al gerente (sección 6.2, tabla "Decisión / Qué hace Cárdenas / Lo que queda abierto"); aquí la red es solo de directorio.
2. **`D#/CHAIRMAN` es un director normal.** Se guarda `preside_algun_directorio` solo como dato informativo.
3. **ID del director = `director_iden`.** Si es un RUT válido (6 a 8 dígitos y dígito verificador que calza con el algoritmo módulo 11) se normaliza sin puntos ni guion y con K mayúscula. Si no es RUT (directores extranjeros, donde viene el nombre) se usa el nombre normalizado (mayúsculas, sin tildes, sin espacios dobles) y `sin_rut = 1`. Estos directores **nunca** se clasifican como políticos. El material pide un identificador único por director para no duplicar personas (error 7).
4. **Empresas con `^`** (dejaron de transarse) se mantienen tal cual. El panel queda no balanceado: la empresa está en la red de los años en que aparece en la base.
5. **Duplicados director-empresa-año**: se buscaron y no hay ninguno.

Resultado: 21.616 filas director-empresa-año, 3.026 empresa-año, 255 empresas (73 con `^`), 2.692 directores distintos (385 sin RUT).

## Decisiones metodológicas

| Decisión | Qué se hizo | Por qué | Material |
|---|---|---|---|
| Población | Todas las empresas de la base en cada año (criterio nominalista) | El investigador define el límite de la red; Cárdenas usa las mayores empresas, aquí la población es la base de la tesis | 3.2 (tabla de criterios), 6.2 |
| Redes en el tiempo | Una red independiente por año fiscal, con la composición del directorio de ese año | El curso trata la red como una fotografía; con panel hay que armar una matriz por año | Omisiones ("redes en el tiempo"), error 7, 6.2 |
| Tipo de red | Red de afiliación (2 modos) director × empresa, proyectada a 1 modo | Es el método de Cárdenas para interlocking | 4.1, 6.2 |
| Proyección | Empresa × empresa = A'A; director × director = AA'. Celdas fuera de la diagonal = n° de directores (o directorios) compartidos | Proyección correcta de la matriz rectangular | 4.1, error 7 |
| Diagonal | Se guarda en `redes_por_anio/matriz_empresa_empresa_valorada_FY####.csv`, pero **se pone en 0 antes de calcular cualquier indicador** | La diagonal no es una relación con otro actor; si se deja, infla densidad, grado y centralización | 4.1, error 7 |
| Dirección | Red no dirigida (simétrica) | Compartir un director es una relación de pertenencia, sin ida ni vuelta | 4.2, 3.2, tabla "Ejemplo" del módulo 2 |
| Dicotomización | Todos los indicadores con la matriz dicotomizada (1 si comparten al menos un director). La intensidad se reporta aparte: `grado_ponderado`, `total_directores_compartidos`, `intensidad_media_por_enlace`, `pct_relaciones_multiples` | Recomendación de Cárdenas; con matriz valorada la densidad deja de ser proporción y el grado deja de ser n° de vecinos | 5.5, 5.6, 5.16, 6.2, error 6 |
| Densidad | L / [n(n−1)/2] | Red no dirigida. La lámina del curso dividía por 23 en vez de 28 | 5.5, error 1 |
| Grado medio | 2L/n, verificado con densidad × (n−1) | Cada enlace suma al grado de dos empresas; la lámina usa L/n | 5.6, error 3 |
| Componentes | Componentes conexos de la red no dirigida (equivalen a componentes débiles) | Interesa la comunicación potencial | 5.11 |
| Ratio de componentes | (c − 1)/(n − 1) | Fórmula del material | 5.11 |
| Distancia media y diámetro | **Solo dentro del componente principal** (`distancia_media_comp_principal`, `diametro_comp_principal`) | En redes desconectadas la distancia entre componentes es infinita; promediar solo pares alcanzables hace parecer compacta una red fragmentada. Siempre leer junto a `pct_comp_principal` | 5.7, 5.8, error 4, 6.3 (Centroamérica) |
| Indicadores tolerantes a la desconexión | Conectividad (1 − proporción de pares no alcanzables) y compacidad (media de 1/d con inalcanzables = 0) | Los usa Cárdenas en redes fragmentadas | 5.8, 6.3, error 4 |
| Centralización de grado | Freeman: Σ(Cmax − Ci)/[(n−1)(n−2)], con todas las empresas (incluidos aislados) | Se lee como "% de la centralización de una estrella", no como probabilidad, y no como más cohesión automáticamente: se lee junto a `pct_puntos_corte` y densidad | 5.12, errores 8 y 9 |
| Coeficiente de agrupamiento | Transitividad global (proporción de tríadas cerradas) | Definición de Cárdenas | 6.3 |
| Índice de cohesión | Primer componente principal de conectividad, densidad, grado medio, ratio de componentes, % comp. principal, % aislados y compacidad, estandarizados sobre los 15 años; puntaje = z·v₁/√λ₁ (puntaje de regresión de un componente), orientado para que más alto = más cohesión. Varianza explicada: 93.3%. Cargas: conectividad +0.38, densidad +0.38, grado_medio +0.38, ratio_componentes -0.39, pct_comp_principal +0.38, pct_aislados -0.35, compacidad +0.39 | Cárdenas lo usa para comparar redes. Con 15 años solo sirve para comparar años entre sí | 6.3 |
| Grado normalizado | grado/(n − 1), en proporción (×100 para %) | Compara empresas de años con distinto n | 5.16 |
| Intermediación | Freeman sobre caminos geodésicos, bruta y normalizada por (n−1)(n−2)/2 (igual que UCINET). No se calcula la de flujo | La intermediación simple es la más usada | 5.18, error 11 |
| Cercanía | **Cercanía armónica** Σ 1/dᵢⱼ (inalcanzables = 0), bruta y normalizada por (n − 1) | La red está desconectada; 1/lejanía es 0 o no existe fuera del componente | 5.17, error 5 |
| Eigenvector | Calculado **solo dentro del componente principal** (norma euclidiana 1). Fuera del componente principal queda **vacío** | El vector propio no está bien definido en una red desconectada (cada componente tiene su propio vector y no son comparables). No se completa con 0 para no inventar datos; si se quiere usar en regresiones se puede reemplazar por 0 y controlar con `en_comp_principal` | Omisiones (Bonacich), error 5 |
| Puntos de corte | Nodos de articulación de la red completa | — | 5.19 |
| Político en t | Director con "Pasado político antes del año (N1.1–N2.2)" = 1 en el cruce. Es un atributo de la persona en el año, igual en todas sus empresas. Niveles con las columnas "N# antes del año" | Definición de la tesis | 6.8, tabla "Idea clave" (cruzar la red con una lista de personas con trayectoria pública) |
| Exposición política | N° y % de empresas vecinas con director político; distancia mínima a **otra** empresa con director político (vacía si no hay camino); `puente_politico` = 1 si la empresa comparte un director político con otra | Lógica de exposición política a través de la red | 6.8 |
| Comparación políticos vs no políticos | Test principal: **t de Welch**, porque los grupos tienen tamaños muy distintos (≈50 políticos contra ≈1.000 no políticos por año) y varianzas distintas, y no conviene suponer varianzas iguales. Se agregan Mann-Whitney y un test de permutación (5.000 permutaciones) porque la intermediación es muy asimétrica (muchos ceros) y en redes las observaciones no son independientes | El curso compara a simple vista; el material advierte que no enseña a evaluar significancia | Omisiones ("comparación estadística"), 5.20 |
| Grupo de comparación | Dos versiones: todos los directores no políticos, y solo los que tienen RUT (los extranjeros nunca son políticos y suelen tener un solo directorio) | Robustez | — |

### Qué hay en la diagonal

- **Matriz empresa × empresa** (A'A): la diagonal es el **número de directores de cada empresa** en ese año (sin CEO). Fuera de la diagonal, el número de directores que comparten las dos empresas (intensidad del enlace).
- **Matriz director × director** (AA'): la diagonal es el **número de directorios en que se sienta cada director** (`n_directorios`). Fuera de la diagonal, el número de directorios que comparten los dos directores.
- La diagonal **no es una relación**: antes de calcular indicadores se pone en 0 (error 7). Las matrices guardadas en `redes_por_anio/` conservan la diagonal para que se pueda revisar; los grafos de Gephi y todos los indicadores no tienen lazos.

### Cómo abrir los archivos de Gephi

`gephi/red_empresas_FY####.gexf` → *Archivo > Abrir*, como red no dirigida. Los nodos ya vienen con color (naranjo = tiene director político, azul = no), tamaño (4 + 2 × grado) y una posición inicial. El peso de cada enlace es el n° de directores compartidos. Los atributos de cada empresa (grado, intermediación, cercanía, eigenvector, punto de corte, n° y % de políticos, etc.) están en el *Laboratorio de datos*. Los valores vacíos (por ejemplo eigenvector fuera del componente principal) se omiten en el archivo.

## Diccionario de variables


### `panel_red_empresa_anio.csv`

| Variable | Definición | Fórmula | Cómo se lee | Material |
|---|---|---|---|---|
| `firm_iden` | Identificador de la empresa tal como viene en la base (incluye '^' si dejó de transarse) | - | Llave para unir con datos financieros junto con fiscal_year | - |
| `company_name` | Nombre de la empresa (sin espacios sobrantes) | - | - | - |
| `fiscal_year` | Año fiscal (FY2010 a FY2024) | - | Llave para unir con datos financieros | - |
| `anio` | Año fiscal en número | - | - | - |
| `empresa_deslistada` | 1 si firm_iden contiene '^' (empresa que dejó de transarse en bolsa) | - | Panel no balanceado: la empresa sale de la red el año en que deja de aparecer en la base | - |
| `n_empresas_red_anio` | N° de empresas (nodos) en la red de ese año | n | Sirve para comparar indicadores normalizados entre años | Error 2 |
| `n_directores` | N° de directores de la empresa en el año (sin CEO) | Diagonal de la matriz empresa x empresa | Tamaño del directorio | 4.1, error 7 |
| `n_directores_sin_rut` | N° de directores sin RUT (extranjeros identificados por nombre) | - | - | - |
| `n_directores_interlock` | N° de directores de la empresa que se sientan en 2 o más directorios ese año | - | Directores que generan enlaces | 6.3 |
| `n_politicos` | N° de directores con pasado político en t | Suma de politico | - | 6.8 |
| `pct_politicos` | % de directores políticos en el directorio | 100 * n_politicos / n_directores | - | 6.8 |
| `tiene_politico` | 1 si la empresa tiene al menos un director político en t | - | - | 6.8 |
| `tiene_politico_N11` | 1 si la empresa tiene al menos un director con cargo de nivel N1.1 antes de t | - | Un director puede tener varios niveles | 6.8 |
| `tiene_politico_N12` | 1 si la empresa tiene al menos un director con cargo de nivel N1.2 antes de t | - | Un director puede tener varios niveles | 6.8 |
| `tiene_politico_N21` | 1 si la empresa tiene al menos un director con cargo de nivel N2.1 antes de t | - | Un director puede tener varios niveles | 6.8 |
| `tiene_politico_N22` | 1 si la empresa tiene al menos un director con cargo de nivel N2.2 antes de t | - | Un director puede tener varios niveles | 6.8 |
| `n_politicos_N11` | N° de directores con cargo de nivel N1.1 antes de t | - | - | 6.8 |
| `n_politicos_N12` | N° de directores con cargo de nivel N1.2 antes de t | - | - | 6.8 |
| `n_politicos_N21` | N° de directores con cargo de nivel N2.1 antes de t | - | - | 6.8 |
| `n_politicos_N22` | N° de directores con cargo de nivel N2.2 antes de t | - | - | 6.8 |
| `n_mujeres` | N° de directoras | - | - | 3.3 (atributos) |
| `pct_mujeres` | % de mujeres en el directorio | 100 * n_mujeres / n_directores con género informado | - | 3.3 (atributos) |
| `grado` | N° de empresas con las que comparte al menos un director (red dicotomizada) | Ci = Σj aij | Poder local: más alto, más conexiones directas | 5.16 |
| `grado_norm` | Grado normalizado (proporción, multiplicar por 100 para %) | grado / (n - 1) | Comparable entre años con distinto n | 5.16 |
| `grado_ponderado` | Grado ponderado por intensidad: n° total de directores compartidos con otras empresas | Σj wij | No es n° de vecinos; una empresa con 4 vecinos puede sumar 9 | 5.16 (intensidad), error 6 |
| `intermediacion` | Intermediación bruta (Freeman): veces que la empresa está en los caminos más cortos entre otras dos, repartiendo cuando hay varios caminos | Σ(s<t) gst(i) / gst | Poder de conexión o puente. Valor comparable con el 148 de Antofagasta en Cárdenas | 5.18, error 11 |
| `intermediacion_norm` | Intermediación normalizada (proporción) | intermediacion / [(n-1)(n-2)/2] | 0 = nunca es puente; 1 = está en todos los caminos (centro de una estrella) | 5.18 |
| `cercania_armonica` | Cercanía armónica: suma de las distancias recíprocas a todas las demás empresas (inalcanzables suman 0) | Σj 1/dij | Acceso a la red; se usa porque la red está desconectada y 1/lejanía no se puede calcular | 5.17, error 5 |
| `cercania_armonica_norm` | Cercanía armónica normalizada | cercania_armonica / (n - 1) | Entre 0 (aislada) y 1 (a un paso de todas) | 5.17, error 5 |
| `eigenvector_comp_principal` | Centralidad de vector propio calculada solo dentro del componente principal (norma euclidiana = 1). Vacío fuera del componente principal | x = (1/λ) A x en el componente principal | Estar conectada con empresas a su vez centrales. No está definida en redes desconectadas, por eso queda vacía fuera del componente principal (no se completa con 0) | Omisiones (Bonacich), error 5 |
| `punto_corte` | 1 si al sacar la empresa la red se divide en más componentes | Nodo de articulación | Clave para la cohesión; su salida desconecta a otras empresas | 5.19 |
| `en_comp_principal` | 1 si la empresa pertenece al componente principal | - | - | 5.11 |
| `aislado` | 1 si la empresa no comparte directores con ninguna otra | grado = 0 | - | 5.10 |
| `tam_componente` | N° de empresas del componente al que pertenece la empresa (1 si es aislada) | - | - | 5.11 |
| `n_vecinos_con_politico` | N° de empresas vecinas (a un paso) que tienen director político en t | Σj aij · politicoj | Exposición política indirecta a través de la red | 6.8 (lógica de exposición) |
| `pct_vecinos_con_politico` | % de las empresas vecinas con director político. Vacío si la empresa es aislada (no tiene vecinos) | 100 * n_vecinos_con_politico / grado | - | 6.8 |
| `dist_min_empresa_con_politico` | Distancia geodésica mínima a OTRA empresa con director político. Vacío si no hay camino | min dij, j ≠ i con politicoj = 1 | 1 = vecina directa de una empresa con político | 2 (distancia), 6.8 |
| `puente_politico` | 1 si la empresa está unida a otra a través de un director político (el político se sienta en ambos directorios) | ∃ j: wpol_ij > 0 | El político es el puente del enlace | 6.8 |
| `n_vecinos_via_politico` | N° de empresas con las que comparte al menos un director político | #{j: wpol_ij > 0} | - | 6.8 |
| `n_vecinos_solo_via_politico` | N° de empresas con las que el ÚNICO vínculo son directores políticos | #{j: wpol_ij = wij > 0} | Enlaces que desaparecerían sin el político | 6.8 |

### `panel_red_director_anio.csv`

| Variable | Definición | Fórmula | Cómo se lee | Material |
|---|---|---|---|---|
| `id_director` | ID del director: RUT sin puntos ni guion (K mayúscula) o, si no tiene RUT, el nombre normalizado | - | - | Error 7 (ID único) |
| `nombre_director` | Nombre del director en la base | - | - | - |
| `fiscal_year / anio` | Año fiscal | - | - | - |
| `sin_rut` | 1 si el director no tiene RUT (se identifica por nombre) | - | Nunca se clasifica como político | - |
| `genero` | Género (M/F) | - | - | 3.3 |
| `politico` | 1 si el director tiene pasado político en t (columna 'Pasado político antes del año' del cruce) | - | - | 6.8 |
| `politico_N11 ... politico_N22` | 1 si tuvo un cargo de ese nivel antes de t | - | Pueden ser varios a la vez | 6.8 |
| `n_directorios` | N° de directorios en que se sienta en t (sin contar cargos de CEO) | Diagonal de la matriz director x director | Director con más asientos = conector | 6.3 |
| `empresas` | Lista de firm_iden de sus directorios en t | - | - | - |
| `preside_algun_directorio` | 1 si es D#/CHAIRMAN en alguna empresa (informativo; se trata como director normal) | - | - | - |
| `grado_red_directores` | N° de directores distintos con los que comparte al menos un directorio | Σj aij en la red director x director | Poder local del director | 5.16 |
| `grado_norm_red_directores` | Grado normalizado en la red de directores | grado / (n - 1) | - | 5.16 |
| `intermediacion_red_directores` | Intermediación bruta en la red de directores | Σ gst(i)/gst | Directores que unen directorios distintos | 5.18 |
| `intermediacion_norm_red_directores` | Intermediación normalizada en la red de directores | bruta / [(n-1)(n-2)/2] | - | 5.18 |

### `cohesion_por_anio.csv`

| Variable | Definición | Fórmula | Cómo se lee | Material |
|---|---|---|---|---|
| `n_nodos` | N° de empresas en la red del año | n | Siempre reportar junto a cada indicador | Error 2 |
| `n_enlaces` | N° de pares de empresas que comparten al menos un director (n° de interlocks) | L | - | 5.5, tabla de cinco países |
| `densidad` | Proporción de enlaces existentes sobre los posibles (red dicotomizada) | L / [n(n-1)/2] | ↑ cohesión. Baja mecánicamente si n crece | 5.5, errores 1 y 6 |
| `grado_medio` | Promedio de empresas vecinas por empresa | 2L / n = densidad × (n-1) | ↑ cohesión. Más comparable que la densidad si n cambia | 5.6, error 3 |
| `desv_est_grado` | Desviación estándar del grado (poblacional) | sd(Ci) | Dispersión de las conexiones | Tabla de cinco países (5.13) |
| `n_componentes` | N° de componentes (débiles; la red no es dirigida). Un aislado es un componente | - | ↓ cohesión | 5.11 |
| `ratio_componentes` | Ratio de componentes | (c - 1) / (n - 1) | 0 = un solo componente; 1 = todos aislados. ↑ fragmentación | 5.11 |
| `tam_comp_principal` | N° de empresas en el componente principal | - | - | 5.11 |
| `pct_comp_principal` | % de empresas en el componente principal | 100 × tam / n | ↑ inclusión y cohesión | 5.11 |
| `n_aislados / pct_aislados` | N° y % de empresas sin ningún director compartido | 100 × aislados / n | ↓ cohesión | 5.10 |
| `conectividad` | Connectedness: proporción de pares de empresas que se alcanzan por algún camino | Σcomp s(s-1)/2 / [n(n-1)/2] | 0 a 1. Funciona con aislados | 6.3 |
| `compacidad` | Media de las distancias recíprocas entre todos los pares (inalcanzables = 0) | Σ(i≠j) (1/dij) / [n(n-1)] | 0 a 1. ↑ compacidad. Tolera la desconexión | 5.8, 6.3, error 4 |
| `coef_agrupamiento_global` | Proporción de tríadas cerradas (transitividad) | 3 × triángulos / tríadas conectadas | Cohesión local | 6.3 |
| `centralizacion_grado` | Centralización de grado de Freeman (red dicotomizada y simétrica) | Σ(Cmax - Ci) / [(n-1)(n-2)] | % de la centralización de una estrella perfecta (no es una probabilidad). Mide dependencia de pocos actores, no más cohesión | 5.12, errores 8 y 9 |
| `pct_alcanzabilidad_actor_mas_central` | % de empresas que la empresa de mayor grado alcanza a un paso | 100 × Cmax / (n-1) | ↑ centralización | 5.12 (otros indicadores) |
| `n_puntos_corte / pct_puntos_corte` | N° y % de empresas cuya salida divide la red | 100 × cortes / n | ↑ fragilidad, ↓ cohesión (robustez) | 5.12, 5.19 |
| `distancia_media_comp_principal` | Distancia geodésica media SOLO dentro del componente principal | Σ dij / [m(m-1)] con m = tam_comp_principal | ↓ cohesión. No se calcula para toda la red porque está desconectada | 5.7, error 4 |
| `diametro_comp_principal` | Diámetro SOLO dentro del componente principal | max dij en el componente principal | ↓ cohesión | 5.8, error 4 |
| `total_directores_compartidos` | Suma de las intensidades de todos los enlaces (intensidad, reportada aparte) | Σ(i<j) wij | Multiplicidad | Error 6 |
| `intensidad_media_por_enlace` | N° medio de directores compartidos por par conectado | Σ wij / L | Multiplicidad | Error 6 |
| `pct_relaciones_multiples` | % de enlaces con 2 o más directores compartidos | 100 × #{wij ≥ 2} / L | ↑ multiplicidad, ↑ cohesión | 5.12 (otros indicadores), error 6 |
| `red_dir_*` | N° de nodos, enlaces, densidad, grado medio y % en componente principal de la red director x director | Mismas fórmulas | Contexto | 4.1 |
| `n_empresas_con_politico / pct_empresas_con_politico` | N° y % de empresas con al menos un director político | - | - | 6.8 |
| `n_enlaces_via_politico / pct_enlaces_via_politico` | N° y % de enlaces en que al menos un director compartido es político | - | Peso de los políticos en la cohesión | 6.8 |
| `indice_cohesion_acp` | Índice de cohesión: puntaje del 1er componente principal de conectividad, densidad, grado medio, ratio de componentes, % comp. principal, % aislados y compacidad (estandarizados, 15 años) | z · v1 / √λ1 | Media 0 y desviación 1 en el período. ↑ cohesión. Solo compara años entre sí | 6.3 |

### `comparacion_politicos_vs_no_politicos.csv`

| Variable | Definición | Fórmula | Cómo se lee | Material |
|---|---|---|---|---|
| `nivel` | director: directores políticos vs no políticos; empresa: empresas con vs sin director político | - | - | 5.20, omisiones (comparación estadística) |
| `periodo` | Año o pool de todos los años | - | En el pool las observaciones no son independientes (misma persona en varios años) | - |
| `muestra` | Grupo de comparación usado | - | 'solo directores con RUT' excluye a los extranjeros, que nunca son políticos | - |
| `media_*, mediana_*, diferencia_medias` | Estadísticos descriptivos por grupo | media políticos - media no políticos | - | - |
| `t_welch / p_welch` | Test t de Welch (test principal) | t = (x̄1 - x̄2) / √(s1²/n1 + s2²/n2) | p < 0,05: diferencia de medias significativa al 5% | - |
| `p_mann_whitney` | Test de Mann-Whitney (robustez, no paramétrico) | - | Robusto a la asimetría y a los muchos ceros de la intermediación | - |
| `p_permutacion` | Test de permutación de la diferencia de medias (5.000 permutaciones de la etiqueta político) | - | No supone normalidad; apropiado para datos de redes | - |

## Problemas encontrados en la base

Ninguno obliga a cambiar las decisiones, pero conviene revisarlos (detalle en `problemas_base.csv`):

1. **Cruce de políticos, una persona duplicada.** Carlos Mladinic Alonso (RUT 6.100.558-7) aparece dos veces en la base de políticos (P0137 "Mladinic" con N1.1 y P0526 "Mladinich" con N1.2). Por eso el cruce tiene 1.413 filas pero 1.411 combinaciones únicas director-empresa-año, y 129 ID_persona para 128 RUT. Como el RUT es el mismo, se tratan como una persona y los niveles se unen con el máximo (N1.1 = 1 y N1.2 = 1 en IAM, FY2017–FY2018).
2. **Las 1.413 filas del cruce calzan con la base board** por `firm_iden` + `fiscal_year` + `director_iden`. Al sacar los CEO se pierden 17 filas: 15 de José Francisco Pérez Mackenna (CEO de Quiñenco, sin pasado político antes del año) y 2 de Jaime Mañalich Muxi (CEO de Clínica Las Condes FY2017–FY2018, con pasado político). Quedan 1.394 filas únicas, 1.202 con pasado político = 1.
3. **`director_iden = "235-6"`** para Gustavo Alessandri Valdés (FOSFOROS.SN, FY2010–FY2013). No es un RUT plausible (3 dígitos); se trató como sin RUT usando el nombre como ID. Solo está en una empresa, así que no cambia la red.
4. **RUT inusualmente bajo**: Carlos Croxatto Silva, `401.301-8` (COPEC.SN, FY2010). El dígito verificador calza, pero 6 dígitos es raro y puede ser un error de digitación. Está en una sola empresa y se mantuvo.
5. **Filas "EMPRESA SIN CEO 20##"** (ESPANOLVAL.SN, FY2011–FY2020, sin género): son filas de relleno con rol CEO y quedan fuera con la regla 1.
6. **Nombre de empresa con espacio sobrante**: VALORES.SN^H20 tiene dos versiones de `company_name` en FY2014; se quitaron los espacios.
7. **Directores sin RUT con nombres parecidos** que podrían ser la misma persona: "THOMAS O FLYNN" y "TOM O FLYNN". No se fusionaron (no hay forma de confirmarlo con la base). Si fueran la misma persona, podría faltar algún enlace.
8. Para directores sin RUT, `director_iden` trae una versión corta del nombre (p. ej. "DIEGO PAREDES" para "DIEGO FERNANDO PAREDES"). Se usó `director_iden` como ID, como se pidió. Ningún nombre de un director sin RUT coincide exactamente con el nombre de un director con RUT, así que no hay personas obvias con dos identificadores.

## Validación

- **Ejemplos del material** (`validacion_funciones.csv`, 48 pruebas, todas correctas): red de 8 actores y 7 enlaces con densidad 0,25, grado medio 1,75, distancia media 2,32 y diámetro 4; red de 6 nodos con grados 4, 3, 3, 2, 3, 1, intermediación 5, 0,667, 0,667, 0,667, 1, 0 y lejanías 6, 7, 7, 8, 8, 10; centralización 1 en la estrella y 0,167 en la línea de 5 nodos y en la red de 7 nodos; ratio de componentes 0,26 y 60% en el componente principal; proyección personas × sindicatos (diagonal UGT = 3) y ACS–Acerinox con 2 directivos compartidos.
- **Base real** (`validacion_panel.csv`, 42 verificaciones, todas correctas): densidades y proporciones dentro de rango, sin grados negativos, grado medio = densidad × (n − 1) = media del grado del panel, suma de grados = 2L, sin empresa-año ni director-año repetidos, y **3.026 empresa-año en el panel = 3.026 empresa-año en la base sin CEO**.
