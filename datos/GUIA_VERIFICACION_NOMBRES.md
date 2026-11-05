# Verificación de nombres de directores por RUT

> **Actualización:** ya se verificaron en internet los 217 RUTs con variantes de nombre. Ver `datos/RESULTADO_VERIFICACION.md` y `datos/maestro_directores_rut_verificado.xlsx`. Este documento describe el diagnóstico inicial.

Archivos:

- `datos/maestro_directores_rut.xlsx`: una fila por RUT, con diagnóstico de calidad.
- `scripts/maestro_ruts.py`: genera el maestro a partir de `interlocking_db.xlsx`.
- `scripts/aplicar_nombres.py`: lleva los nombres verificados de vuelta a la base completa.

## 1. Diagnóstico de la base (`interlocking_db.xlsx`)

| Indicador | Valor |
|---|---|
| Filas totales | 24.652 |
| Filas con RUT numérico | 23.172 |
| Filas sin RUT (extranjeros, excluidos) | 1.480 |
| **RUTs únicos** | **2.676** |
| RUTs con dígito verificador inválido (módulo 11) | 0 |
| RUTs sospechosamente cortos (< 1.000.000) | 2 |
| RUTs con una sola forma de nombre | 2.459 |
| RUTs con variantes que solo difieren en completitud (ej. "MICHELE LABBE" / "MICHELE ALIDA LABBE CID") | 152 |
| RUTs con variantes que tienen errores de ortografía | 64 |
| RUTs con nombres distintos (posiblemente dos personas) | 1 |
| Mismo RUT dos veces en la misma empresa-año | 0 |
| Pares de RUTs distintos con nombres muy parecidos (familiares) | 7 |
| Nombres con menos de 3 palabras (incompletos) | 103 |

Ningún nombre aparece asociado a dos RUTs distintos (en la comparación exacta).

### Hojas del Excel

- `resumen`: la tabla anterior.
- `maestro_rut`: una fila por RUT con: `nombre_candidato` (la variante más completa y, si hay empate, la más frecuente), todas las `variantes` con su frecuencia, los años y las empresas, el `tipo_diferencia` y la `prioridad_verificacion`. Las columnas vacías **`nombre_verificado`, `fuente_verificacion` y `notas`** son para ir completándolas.
- `variantes_nombre`: los 217 RUTs que tienen más de una forma de nombre.
- `nombres_parecidos`: RUTs distintos con nombres casi iguales (hermanos, primos, homónimos).
- `dv_invalido`: vacía, porque todos los dígitos verificadores son correctos.
- `sin_rut_excluidos`: los directores extranjeros que se dejaron fuera.

### Prioridad de verificación

- **1-alta (3 casos):** RUT sospechosamente corto o nombres incompatibles.
  - `235-6` GUSTAVO ALESSANDRI VALDEZ (Cía. Chilena de Fósforos, 2010–2013). El dígito verificador calza, pero un RUT de 3 dígitos no es plausible para un director nacido en 1929. Lo más probable es que el RUT esté truncado en la fuente. Además el apellido correcto es *Valdés*, con s. Ojo: es exdiputado y exalcalde, o sea un caso relevante para la tesis.
  - `401.301-8` CARLOS CROXATTO SILVA (Copec, 2010). Mismo problema: el RUT probablemente está truncado.
  - `14.596.123-8` aparece como "CARLOS INGHAM KOTTMEIER" (12 veces) y como "CARLOS GUSTAVO INGHAM" (1 vez). Probablemente es la misma persona, Carlos Gustavo Ingham Kottmeier, pero hay que confirmarlo.
- **2-media (181 casos):** errores de ortografía, nombres de menos de 3 palabras o nombres parecidos a los de otro RUT.
- **3-baja (2.492):** un solo nombre consistente o variantes que solo difieren en completitud. Aun así conviene confirmarlos, porque un mismo error repetido en todas las memorias no se detecta con este método.

**Importante:** `nombre_candidato` es una propuesta automática, no un nombre verificado. Hay casos en que la variante más frecuente es la que está mal escrita (ej. "JUAN FERNANDO SORO KOM" ×8 frente a "FERNANDO SORO KORN" ×2) o en que el segundo apellido cambia por completo ("SERGIO DE LA CUADRA FABRES" frente a "…ZALAQUETT"). Por eso estos casos están en prioridad 2.

## 2. Cómo verificar: orden recomendado de fuentes

1. **CMF (fuente oficial, recomendada como primera fuente).** Para cada sociedad anónima abierta, la Comisión para el Mercado Financiero publica el directorio con RUT y nombre completo de cada director (cmfchile.cl → Entidades fiscalizadas → la empresa → pestaña de Directorio/Administración). Es la misma información que reportan las propias empresas, pero en registro oficial y con el RUT al lado. Sirve como fuente citable en la tesis, a diferencia de un rutificador comercial. Los hechos esenciales de nombramiento de directores también traen los nombres completos.
2. **Rutificador (nombrerutyfirma.com u otro), consultando a mano** los casos de prioridad 1 y 2 (184 RUTs). Anota en `fuente_verificacion` "rutificador" y la fecha de consulta. Copia solo el nombre; no guardes dirección ni otros datos personales que muestra la página, porque no los necesitas para la tesis.
3. **Otras fuentes públicas** cuando lo anterior no basta: memorias anuales en PDF (suelen traer nombre completo y RUT), Diario Oficial, prensa económica (DF, La Tercera, Emol), Wikipedia y la BCN para quienes tuvieron cargos. **Regla: un nombre se da por verificado solo si coincide en al menos dos fuentes independientes.** Si no se llega a dos, deja `nombre_verificado` vacío y escribe en `notas` "verificar a mano".

Por qué no se automatizó la consulta masiva a nombrerutyfirma: desde este entorno el sitio no es accesible (la red está restringida). Además, se trata de un sitio de búsqueda de personas que entrega también domicilio y otros datos personales, y que suele bloquear las consultas automáticas. Hacer miles de consultas automáticas sobre él no es lo apropiado. La CMF entrega lo mismo (RUT ↔ nombre completo de directores) de forma oficial.

## 3. Flujo de trabajo

Requisitos: `pip install pandas openpyxl rapidfuzz unidecode`

1. Abrir `datos/maestro_directores_rut.xlsx`, hoja `maestro_rut`, ordenada por prioridad.
2. Completar `nombre_verificado` (nombre completo en mayúsculas, con tildes y Ñ si corresponde) y `fuente_verificacion`.
3. Ejecutar:
   ```bash
   python scripts/aplicar_nombres.py interlocking_db.xlsx datos/maestro_directores_rut.xlsx interlocking_db_nombres.xlsx
   ```
   El resultado es la base original con tres columnas nuevas: `rut_normalizado`, `nombre_final` y `fuente_nombre`. La columna `fuente_nombre` indica qué filas siguen "sin verificar".
4. Para la búsqueda de pasado político, usar `nombre_final` y, siempre que la fuente lo permita, cruzar por RUT y no por nombre.

## 4. Ideas para la etapa de pasado político

- **Cruzar por RUT en vez de por nombre** siempre que se pueda: es lo que evita confundir a primos y homónimos. Varias fuentes oficiales identifican a las personas por RUT o con nombre completo:
  - Servel: candidaturas y electos.
  - InfoProbidad: declaraciones de intereses y patrimonio de autoridades.
  - BCN: reseñas biográficas parlamentarias.
  - Nombramientos publicados en el Diario Oficial y transparencia activa de ministerios y servicios.
- Para cada director, registrar el cargo político, el período y la URL de la fuente, y exigir también aquí dos fuentes independientes.
- Los familiares detectados en `nombres_parecidos` (Matte, Solari, Lecaros, Valdés Raczynski, etc.) son justamente los casos donde más fácil se atribuye un cargo a la persona equivocada.
