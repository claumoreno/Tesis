# Propuesta inicial de tesis

**Título tentativo:** Directores políticos, redes de directorio y gestión de resultados: evidencia de empresas chilenas en torno a los ciclos electorales

- **Carrera:** Ingeniería Comercial, mención Administración de Empresas (área Finanzas)
- **Profesor guía:** Carlos Cid
- **Escritura:** Word, con referencias en Zotero y formato APA 7 *(confirmar con el profesor)*
- **Fecha de entrega:** 31 de marzo de 2027

> Documento de trabajo. Sirve para ordenar la idea antes de redactar el anteproyecto formal. Todo lo que está marcado con **[DEFINIR]** depende de decisiones que hay que tomar con el profesor guía.

---

## 1. Idea central en una frase

Analizar si las empresas chilenas que tienen en su directorio a personas con trayectoria política gestionan sus resultados contables (*earnings management*) de forma distinta a las empresas sin esos directores, si esta diferencia cambia en los años electorales y si se transmite a otras empresas por medio de la red de directores compartidos (*board interlocks*).

## 2. Preguntas de investigación

1. **P1.** ¿Existen diferencias en la gestión de resultados entre empresas con y sin directores políticos?
2. **P2.** ¿Se modifica esta relación durante los años electorales?
3. **P3 (redes, alineada con la línea del profesor).** ¿La posición de la empresa en la red de directores, en particular su conexión con directores políticos a través de directores compartidos, se relaciona con su nivel de gestión de resultados?

## 3. Objetivos

**Objetivo general**
Determinar la relación entre la presencia de directores políticos en los directorios, y la red de directores en que se insertan, y la gestión de resultados de las empresas, y cómo esta relación varía en los años electorales.

**Objetivos específicos**
1. Identificar y caracterizar a los directores con conexiones políticas en las empresas de la muestra.
2. Construir la red de directorios (empresas conectadas por directores compartidos) para cada año del período de estudio.
3. Estimar la gestión de resultados mediante acumulaciones discrecionales y actividades reales.
4. Comparar la gestión de resultados entre empresas con y sin directores políticos.
5. Evaluar si el efecto se modifica en los años electorales.
6. Evaluar si la centralidad en la red y la conexión indirecta con directores políticos se asocian con la gestión de resultados.

## 4. Marco teórico (de dónde salen las hipótesis)

| Teoría | Qué predice | Autores base |
|---|---|---|
| **Teoría de la agencia** | Los directores deben supervisar a la gerencia. Si el director político fue elegido por sus contactos y no para supervisar, la supervisión es más débil y hay **más** gestión de resultados. | Jensen y Meckling (1976) |
| **Dependencia de recursos** | Las empresas incorporan políticos para obtener recursos externos (acceso a regulación, contratos, información). | Pfeffer y Salancik (1978); Hillman (2005) |
| **Conexiones políticas y calidad contable** | Las empresas conectadas enfrentan menor presión del mercado y pueden tener información contable de **menor** calidad. | Faccio (2006); Chaney, Faccio y Parsley (2011) |
| **Costos políticos (teoría contable positiva)** | Las empresas más visibles para el poder político gestionan sus resultados **a la baja** para no llamar la atención, sobre todo cuando aumenta el escrutinio. | Watts y Zimmerman (1978) |
| **Elecciones y gestión de resultados** | En torno a las elecciones cambian los incentivos de las empresas conectadas políticamente. | Ramanna y Roychowdhury (2010); Julio y Yook (2012) |
| **Redes de directorio** | Las prácticas, incluida la gestión de resultados, se difunden entre empresas que comparten directores. | Mizruchi (1996); Chiu, Teoh y Tian (2013); Larcker, So y Wang (2013) |

**Tensión teórica (y por qué la pregunta es interesante):** la literatura permite predecir tanto **más** gestión de resultados (por menor supervisión y menor presión del mercado) como **menos**, o en otra dirección (por mayor visibilidad y costos políticos). La tesis aporta evidencia empírica sobre cuál efecto domina.

## 5. Hipótesis

- **H1a:** Las empresas con directores políticos presentan mayor gestión de resultados que las empresas sin directores políticos.
- **H1b (hipótesis rival):** Las empresas con directores políticos presentan menor gestión de resultados, por su mayor exposición al escrutinio público.
- **H2:** En los años electorales, la gestión de resultados de las empresas con directores políticos difiere de la del resto. Siguiendo la hipótesis de costos políticos, se espera que sea **a la baja**.
- **H3:** Las empresas conectadas indirectamente con directores políticos (por medio de un director compartido con una empresa que tiene un director político) y las empresas más centrales en la red presentan niveles distintos de gestión de resultados.

## 6. Metodología

### 6.1 Muestra y período
- **País:** Chile.
- **Empresas:** sociedades anónimas abiertas no financieras que reportan a la CMF (Comisión para el Mercado Financiero). Se excluyen bancos, aseguradoras y AFP porque sus acumulaciones contables se comportan distinto. Se esperan entre 100 y 150 empresas, es decir, unas 1.500 observaciones empresa-año.
- **Período sugerido:** de 2010 a 2024, el mismo de la red de directores compartidos que construyó Alejandro Capllonch en su tesis guiada por el profesor Cid. Si esa base se puede reutilizar, se ahorra gran parte de la recolección.
  - Parte con la adopción de IFRS en Chile (2009–2010), así que no se mezclan normas contables.
  - Abarca **3 elecciones presidenciales y parlamentarias**: 2013, 2017 y 2021.
  - Como alternativa, se puede extender hasta 2025 para sumar la elección de ese año.
- **Unidad de análisis:** empresa-año (datos de panel).

**Calendario electoral chileno a considerar** (verificar en Servel):

| Año | Elección |
|---|---|
| 2013 | Presidencial y parlamentaria |
| 2016 | Municipal |
| 2017 | Presidencial y parlamentaria |
| 2021 | Presidencial, parlamentaria, municipal, de gobernadores y de convencionales constituyentes |
| 2024 | Municipal y regional |
| 2025 | Presidencial y parlamentaria |

En la variable principal conviene considerar solo las elecciones **presidenciales y parlamentarias**. Las municipales y los plebiscitos constitucionales (2020, 2022 y 2023) pueden usarse en pruebas de robustez.

**Contexto chileno que justifica el tema:** en Chile hay muchos grupos económicos, pocas empresas listadas y una alta concentración de la propiedad. Además, es frecuente que exministros y exautoridades lleguen a los directorios (la llamada "puerta giratoria"). Los casos de financiamiento irregular de la política de 2014–2015, como Penta y SQM, pusieron la relación entre empresas y política en el debate público. Todo esto hace que Chile sea un buen caso de estudio.

### 6.2 Fuentes de datos
- **Estados financieros:** sitio de la CMF (estados financieros IFRS de cada sociedad), Economática o Refinitiv/Eikon. Preguntar en la biblioteca de la facultad qué bases hay disponibles.
- **Composición de los directorios:** memorias anuales en el sitio de la CMF (sección "Directores" y "Hechos esenciales" para cambios de directorio) y reportes de la NCG 385/461 sobre gobierno corporativo.
- **Trayectoria política de los directores:**
  - Reseñas biográficas parlamentarias de la Biblioteca del Congreso Nacional (BCN).
  - Nóminas de ministros y subsecretarios de cada gobierno.
  - Candidatos inscritos en Servel.
  - Prensa: Ciper, Emol, La Tercera y Diario Financiero.
  - LinkedIn.
- **Calendario electoral:** Servel.

### 6.3 Variables

**Variable dependiente: gestión de resultados**
- **Principal:** acumulaciones discrecionales (DA) según el modelo de Jones modificado (Dechow, Sloan y Sweeney, 1995), ajustado por desempeño (Kothari, Leone y Wasley, 2005). Se estima por industria y año.
- **Alternativa:** gestión de actividades reales (Roychowdhury, 2006), que considera el flujo de caja operativo, los costos de producción y los gastos discrecionales anormales.
- Usar **|DA|** (valor absoluto) para medir la magnitud de la gestión y **DA con signo** para medir su dirección, al alza o a la baja. El signo es clave para H2.

**Variables independientes**
- `POL`: variable dicotómica, igual a 1 si la empresa tiene al menos un director político en el año. Se pueden usar alternativas como el número o la proporción de directores políticos.
- **Definición de director político [DEFINIR CON EL PROFESOR]:** persona que es o fue ministro, subsecretario, parlamentario (diputado o senador), intendente o delegado presidencial, gobernador regional, alcalde, superintendente o jefe de servicio, dirigente de partido o candidato a elección popular. Se puede distinguir entre conexión actual y pasada, y entre partido de gobierno y de oposición.
- `ELEC`: variable dicotómica, igual a 1 en los años de elección presidencial o parlamentaria. Se puede probar también con el año previo a la elección.
- **Variables de red**, calculadas por año:
  - `GRADO`: número de empresas con las que la empresa comparte directores.
  - `INTERMEDIACION` (*betweenness*) y `CENTRALIDAD_EIGEN` (*eigenvector*).
  - `POL_IND`: igual a 1 si la empresa está conectada, a través de un director compartido, con una empresa que tiene un director político.

**Variables de control** (estándar en la literatura)
Tamaño (logaritmo de activos), endeudamiento, ROA, pérdida, crecimiento de ventas o *market-to-book*, auditor Big 4, tamaño del directorio, proporción de directores independientes, concentración de la propiedad y si la empresa pertenece a un grupo económico.

### 6.4 Modelos

**Modelo para P1 y P2**

```
EM_it = b0 + b1·POL_it + b2·ELEC_t + b3·(POL_it × ELEC_t) + Controles_it + EF_industria + e_it
```

- `b1` responde la P1 y `b3` responde la P2.
- **Detalle técnico importante:** `ELEC_t` es igual para todas las empresas en un mismo año, así que **no se puede incluir junto con efectos fijos de año**. Hay dos opciones:
  - incluir efectos fijos de año y estimar solo `POL` y la interacción `POL × ELEC`, o
  - no incluir efectos fijos de año y controlar por variables macroeconómicas como el crecimiento del PIB.
- Usar errores estándar agrupados (*cluster*) por empresa.

**Modelo para P3 (redes)**

```
EM_it = b0 + b1·POL_it + b2·POL_IND_it + b3·CENTRALIDAD_it + Controles_it + EF + e_it
```

### 6.5 Endogeneidad (lo que preguntará el comité)
Las empresas no eligen a sus directores al azar. Por ejemplo, las empresas reguladas pueden contratar políticos y también tener más incentivos para gestionar resultados. Algunas formas de abordarlo:
- Efectos fijos de empresa, que identifican el efecto a partir de los cambios en el directorio.
- *Propensity score matching* o *entropy balancing* para comparar empresas similares.
- Un análisis en torno a la llegada o salida de un director político, del tipo diferencias en diferencias.
- Usar la elección como shock exógeno, que es justamente la ventaja de H2.

### 6.6 Herramientas
- **Análisis estadístico:** Stata, R (paquetes `fixest` y `plm`) o Python (`linearmodels`).
- **Redes:** R (`igraph`) o Python (`networkx`). Se construye una red bipartita de directores y empresas por año y se proyecta en una red de empresa a empresa.
- **Referencias:** Zotero.

## 7. Posible estructura de la tesis

1. Introducción (motivación, preguntas, contribución)
2. Marco teórico y revisión de literatura
   - 2.1 Gestión de resultados
   - 2.2 Conexiones políticas y directorios
   - 2.3 Redes de directorio
   - 2.4 Ciclos electorales
   - 2.5 Hipótesis
3. Contexto institucional del país (gobierno corporativo, sistema electoral, regulación)
4. Datos y metodología
5. Resultados (estadística descriptiva, análisis de la red, regresiones)
6. Pruebas de robustez
7. Conclusiones, limitaciones e investigación futura

## 8. Cronograma hasta el 31 de marzo de 2027

Son unas 24 semanas. Ojo con enero y febrero: el profesor puede tomar vacaciones, así que conviene tener **el capítulo de datos listo antes de diciembre**.

| Fechas | Tarea | Producto |
|---|---|---|
| 12 – 25 oct 2026 | Reunión con el profesor Cid: validar las preguntas, el período, la definición de director político y las bases de datos. Empezar las lecturas base. | Decisiones de la sección 10 cerradas |
| 26 oct – 15 nov | Matriz de literatura (25 a 40 artículos). **Prueba piloto:** 20 empresas en 2 años, para revisar memorias, directores y datos financieros. | Matriz de literatura; piloto que confirma que los datos existen |
| 16 – 29 nov | Redactar la introducción, el planteamiento del problema, los objetivos, las hipótesis y la metodología. | **Anteproyecto** para el profesor |
| 30 nov – 3 ene 2027 | Recolección completa: directorios por año, trayectoria política de cada director y estados financieros. | Base de datos en Excel (empresa-año y director-empresa-año) |
| 4 – 24 ene | Calcular la gestión de resultados (Jones modificado o Kothari), construir la red y sus medidas de centralidad, y la estadística descriptiva. Redactar el marco teórico. | Variables listas; capítulo 2 en borrador |
| 25 ene – 21 feb | Regresiones principales (H1, H2, H3) y pruebas de robustez. | Tablas de resultados; capítulo 5 en borrador |
| 22 feb – 14 mar | Redactar los resultados, la discusión y las conclusiones. Revisión completa del profesor. | Borrador completo |
| 15 – 31 mar | Correcciones, formato APA, resumen, índice y anexos. **Entrega.** | Tesis final |

**Lo más riesgoso es la recolección de datos sobre directores políticos**, porque se hace a mano. Por eso la prueba piloto va en noviembre: si los datos no alcanzan, todavía hay tiempo para ajustar el período o la definición.

## 9. Lecturas base (empezar por estas)

**Gestión de resultados**
- Healy, P. M., & Wahlen, J. M. (1999). A review of the earnings management literature and its implications for standard setting. *Accounting Horizons*, 13(4), 365–383.
- Jones, J. J. (1991). Earnings management during import relief investigations. *Journal of Accounting Research*, 29(2), 193–228.
- Dechow, P. M., Sloan, R. G., & Sweeney, A. P. (1995). Detecting earnings management. *The Accounting Review*, 70(2), 193–225.
- Kothari, S. P., Leone, A. J., & Wasley, C. E. (2005). Performance matched discretionary accrual measures. *Journal of Accounting and Economics*, 39(1), 163–197.
- Roychowdhury, S. (2006). Earnings management through real activities manipulation. *Journal of Accounting and Economics*, 42(3), 335–370.
- Leuz, C., Nanda, D., & Wysocki, P. D. (2003). Earnings management and investor protection: An international comparison. *Journal of Financial Economics*, 69(3), 505–527.

**Conexiones políticas**
- Fisman, R. (2001). Estimating the value of political connections. *American Economic Review*, 91(4), 1095–1102.
- Faccio, M. (2006). Politically connected firms. *American Economic Review*, 96(1), 369–386.
- Hillman, A. J. (2005). Politicians on the board of directors: Do connections affect the bottom line? *Journal of Management*, 31(3), 464–481.
- Goldman, E., Rocholl, J., & So, J. (2009). Do politically connected boards affect firm value? *Review of Financial Studies*, 22(6), 2331–2360.
- Chaney, P. K., Faccio, M., & Parsley, D. (2011). The quality of accounting information in politically connected firms. *Journal of Accounting and Economics*, 51(1–2), 58–76.

**Elecciones y costos políticos**
- Watts, R. L., & Zimmerman, J. L. (1978). Towards a positive theory of the determination of accounting standards. *The Accounting Review*, 53(1), 112–134.
- Ramanna, K., & Roychowdhury, S. (2010). Elections and discretionary accruals: Evidence from 2004. *Journal of Accounting Research*, 48(2), 445–475.
- Julio, B., & Yook, Y. (2012). Political uncertainty and corporate investment cycles. *Journal of Finance*, 67(1), 45–83.

**Redes de directorio**
- Mizruchi, M. S. (1996). What do interlocks do? An analysis, critique, and assessment of research on interlocking directorates. *Annual Review of Sociology*, 22, 271–298.
- Chiu, P.-C., Teoh, S. H., & Tian, F. (2013). Board interlocks and earnings management contagion. *The Accounting Review*, 88(3), 915–944.
- Larcker, D. F., So, E. C., & Wang, C. C. Y. (2013). Boardroom centrality and firm performance. *Journal of Accounting and Economics*, 55(2–3), 190–211.

**Teoría general**
- Jensen, M. C., & Meckling, W. H. (1976). Theory of the firm: Managerial behavior, agency costs and ownership structure. *Journal of Financial Economics*, 3(4), 305–360.
- Pfeffer, J., & Salancik, G. R. (1978). *The External Control of Organizations: A Resource Dependence Perspective*. Harper & Row.

> Verificar cada referencia en Google Scholar antes de citarla. Buscar además estudios chilenos y latinoamericanos con términos como "gobierno corporativo Chile", "grupos económicos Chile",  "conexiones políticas", "directorios entrelazados", "gestión de resultados" y "political connections Latin America", en Scopus, SciELO y Redalyc.

## 10. Decisiones pendientes con el profesor

- [x] País: Chile
- [ ] Período de estudio (sugerido: 2010–2024) y elecciones que se van a considerar
- [ ] Acceso a la base de directores y red 2010–2024 de la tesis de Capllonch
- [ ] Definición operativa de "director político"
- [ ] Bases de datos financieras a las que tiene acceso la universidad
- [ ] Medida principal de gestión de resultados (acumulaciones discrecionales, actividades reales o ambas)
- [ ] Software de análisis
- [ ] Si la tesis puede ser de un integrante o en pareja (el volumen de recolección de datos es alto)
- [ ] Formato y extensión exigidos por la universidad (¿APA 7?); fecha de entrega del anteproyecto
- [x] Entrega final: 31 de marzo de 2027
