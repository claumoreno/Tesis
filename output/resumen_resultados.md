# Resumen de resultados: la red de directorios en Chile, FY2010–FY2024

Lo que sigue es descriptivo. Todas las cifras vienen de `cohesion_por_anio.csv`, `panel_red_empresa_anio.csv`, `panel_red_director_anio.csv` y `comparacion_politicos_vs_no_politicos.csv`. Cada año es una red distinta, con las empresas y los directores (sin CEO) de ese año.

## 1. La red se volvió menos cohesionada

Entre 2010 y 2024 la red de empresas unidas por directores compartidos se fue soltando de forma sostenida.

| Indicador | FY2010 | FY2017 | FY2024 | Cómo leerlo |
|---|---|---|---|---|
| Empresas (n) | 219 | 208 | 176 | La base pierde empresas que dejan de transarse |
| Enlaces (pares de empresas que comparten un director) | 679 | 427 | 287 | Cae a menos de la mitad |
| Densidad | 0,028 | 0,020 | 0,019 | Existe el 2,8% de los enlaces posibles en 2010 y el 1,9% en 2024 |
| Grado medio (2L/n) | 6,20 | 4,11 | 3,26 | En 2010 una empresa típica estaba unida a 6 empresas; en 2024 a 3 |
| % en el componente principal | 83,1% | 74,5% | 72,7% | Menos empresas en el bloque conectado |
| % de empresas aisladas | 14,6% | 16,3% | 19,3% | Una de cada cinco empresas no comparte ningún director en 2024 |
| Conectividad | 0,69 | 0,56 | 0,53 | Proporción de pares de empresas que pueden alcanzarse por algún camino |
| Compacidad | 0,23 | 0,16 | 0,14 | La red es más "larga" |
| Distancia media (solo componente principal) | 3,5 | 4,2 | 4,8 | Dentro del bloque conectado se necesitan más pasos para llegar de una empresa a otra |
| % de puntos de corte | 8,7% | 12,5% | 12,5% | Más empresas cuya salida rompe la red: la red es más frágil |
| Índice de cohesión (ACP) | 1,46 | −0,42 | −1,15 | Resume todo lo anterior; cae casi sin interrupciones |

La caída no es solo porque haya menos empresas. La densidad baja mecánicamente cuando la red crece, pero aquí la red se achica y la densidad igual baja; el grado medio, que es más comparable entre años de distinto tamaño, cae a la mitad. La caída más fuerte ocurre entre 2013 y 2017; desde 2018 la red se estabiliza en un nivel bajo.

Dos cosas se mantienen: el coeficiente de agrupamiento (≈0,45, es decir, las empresas vecinas de una empresa suelen estar unidas entre sí, típico de grupos económicos) y la intensidad de los enlaces (≈26% de los pares conectados comparten dos o más directores). La centralización de grado es baja todo el período (entre 4% y 9% de la de una estrella perfecta): la red no depende de una sola empresa, sino de varios grupos conectados.

Para comparar con Cárdenas: su red chilena de 90 grandes empresas (2016) tenía densidad 0,04, grado medio 3,53, 78,9% en el componente principal y 16,7% de aislados. Esta red es más grande (incluye todas las empresas de la base) y su densidad es menor, pero el % en el componente principal y el % de aislados son muy parecidos a los de él en los primeros años.

## 2. Empresas más centrales

Considerando las empresas presentes al menos 10 años, las que más funcionan como **puente** (mayor intermediación promedio) son Embotelladora Andina, Cristalerías de Chile, Compañía Sud Americana de Vapores, SQM, Entel, Pesquera Coloso, Elecmetal, CMPC, Viña Santa Rita y Sonda. Las con más **conexiones directas** (grado promedio) son Cristalerías de Chile (≈16 empresas vecinas), Vapores (≈15), Elecmetal (≈14), Entel (≈13), Navarino, SAAM y Santa Rita (≈12). Varias pertenecen a los mismos grupos económicos (Claro: Cristalerías, Elecmetal, Navarino, Santa Rita; Luksic: Vapores, SAAM, Invexans), (según la propiedad conocida de estos grupos, que no está en la base), lo que calza con la lectura de Cárdenas de que la cohesión chilena se sostiene en empresas conectoras de grandes grupos.

Por año, la empresa con mayor intermediación es CMPC en 2010, Banmédica en 2017 y Entel en 2024. En 2024 la intermediación está más concentrada: Entel está en el 10% de los caminos más cortos entre pares de empresas, contra 6% de la primera empresa en 2010. Con menos enlaces, unas pocas empresas sostienen más la conexión de la red.

## 3. Los directores políticos

- Cada año hay entre 45 y 54 directores con pasado político (de unos 1.000 directores), y entre 45 y 73 empresas con al menos uno (entre 25,6% y 33,8% de las empresas). Desde 2021 ambas cifras bajan.
- **Los políticos se sientan en más directorios.** Entre el 27% y el 47% de los directores políticos está en dos o más directorios cada año, contra cerca del 20% de los no políticos. La diferencia se achica desde 2021.
- **Los políticos son más centrales en la red de directores.** En los 15 años, el grado medio de los directores políticos es mayor que el de los no políticos (en el pool, 10,7 contra 8,2 directores con los que comparten directorio) y su intermediación normalizada es casi el triple (0,0054 contra 0,0019). La diferencia es significativa al 5% en 12 a 13 de los 15 años con el test de permutación (9 a 11 años con el t de Welch), y se mantiene si se excluye a los directores extranjeros sin RUT. En el n° de directorios la diferencia es positiva todos los años pero significativa solo en 5 a 7 años.
- **Las empresas con director político son más centrales.** Tienen mayor grado, intermediación y cercanía todos los años (en el pool: grado 5,8 contra 4,0; cercanía armónica normalizada 0,22 contra 0,16). Con el test de permutación, la cercanía es significativamente mayor en los 15 años, y el grado y la intermediación en 12. El eigenvector (dentro del componente principal) es mayor en 11 de 15 años, pero significativo solo en 7: esa diferencia no es robusta. Además, solo el 7% de las empresa-año con director político está aislada, contra el 20% de las que no tienen.
- **Los políticos sirven de puente.** El 70% de las empresa-año con director político comparte ese director con otra empresa. Entre el 6,6% y el 14,9% de todos los enlaces de la red pasan por un director político; ese porcentaje subió hasta 2014 y bajó a 6,6% en 2024.
- **Exposición indirecta.** En promedio, entre 27% y 42% de las empresas vecinas de una empresa tiene director político. La mitad de las empresas (49% en 2024, 69% en 2010) está a un paso de otra empresa con director político.
- **La ventaja se debilita al final del período.** En 2024 las diferencias entre políticos y no políticos ya no son significativas con el test principal (Welch), salvo la cercanía de las empresas.

## 4. Cuidados al interpretar

- Son asociaciones descriptivas, no efectos causales. Una empresa más grande o de un grupo económico grande puede tener a la vez más interlocks y más probabilidad de tener un ex político.
- En la red las observaciones no son independientes y en el pool la misma persona o empresa aparece varios años. Por eso se agregan el test de Mann-Whitney y el de permutación al t de Welch; las conclusiones son las mismas con los tres, pero el pool sobrestima la precisión.
- La distancia media y el diámetro se calculan solo dentro del componente principal; deben leerse junto al % de empresas en ese componente.
- El eigenvector queda vacío fuera del componente principal. Para usarlo en regresiones hay que decidir cómo tratar esas empresas (por ejemplo, 0 y una dummy de `en_comp_principal`).
