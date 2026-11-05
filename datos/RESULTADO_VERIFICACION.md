# Verificación de nombres por RUT: resultado

Archivos principales:

- **`datos/maestro_directores_rut_verificado.xlsx`**: una fila por RUT (2.676), con el nombre final, el estado de verificación, las fuentes (URLs) y notas.
- **`datos/interlocking_db_nombres_corregidos.xlsx`**: tu base original completa (24.652 filas), con estas columnas nuevas:
  - `rut_normalizado`
  - `nombre_final`
  - `estado_verificacion`
  - `nombre_cambio`: vale VERDADERO en las 1.646 filas cuyo nombre se modificó.
- `datos/verificacion_web_217.tsv`: el registro de cada búsqueda, con las URLs.
- `scripts/integrar_verificacion.py`: regenera los dos Excel a partir del maestro y del registro de búsquedas.

## Qué se hizo

1. **Se identificaron 217 RUTs con más de una forma de escribir el nombre.** Cada uno se buscó en internet por nombre más empresa. Una fuente se aceptó solo si mencionaba a esa persona en alguna de las empresas que aparecen en la base para ese RUT. Así se evita confundir a homónimos.
2. **Cómo se eligió el nombre final:**
   - Si había fuentes, se usó el nombre que confirman las fuentes, aunque no fuera el más frecuente en la base. Por ejemplo, la base decía SORO **KOM** 8 veces, y las fuentes confirman SORO **KORN**.
   - Si no había fuentes y era un error tipográfico evidente, se corrigió. Ejemplos: BREATRIZ → BEATRIZ, MIRANDO → MIRANDA, GONZALOEZ → GONZALEZ.
   - Si no había fuentes y una variante solo era más completa que otra, se tomó la forma más completa que aparece en las memorias.
   - Si había un conflicto real que no se pudo resolver, el caso quedó como **NO CONFIRMADO**.
3. Se mantuvo el estilo de la base: MAYÚSCULAS, con Ñ y sin tildes.
4. Los 2.459 RUTs que tienen una sola forma de nombre en la base no se buscaron en internet. Su nombre se mantuvo tal cual.

## Resultado (hoja `resumen`)

| Estado | RUTs |
|---|---|
| 0. Un solo nombre en la base (no buscado en web) | 2.457 |
| 1. Verificado con 2 o más fuentes web | 118 |
| 2. Verificado con 1 fuente web que calza con la empresa | 41 |
| 3. Verificado indirecto (apellido confirmado en un familiar) | 3 |
| 4. Sin fuente web: se tomó la forma más completa de la base | 34 |
| 5. Sin fuente web: corregido error tipográfico evidente | 14 |
| 6. NO CONFIRMADO: revisar a mano | 9 |

**Importante sobre las fuentes.** La fuente más frecuente es MarketScreener/Zonebourse, un agregador que copia los registros de las empresas. En el estado 1, la mayoría de los casos tienen una segunda fuente independiente: prensa (DF, La Tercera, Emol), Wikipedia, memorias o sitios de las empresas. En algunos casos, sin embargo, las "2 fuentes" son dos perfiles del mismo agregador. Esos casos están confirmados pero conviene tratarlos como de una sola fuente.

## Lo que tienes que revisar a mano (hoja `revisar_a_mano`, 62 RUTs)

Incluye los estados 4, 5 y 6, más los casos con notas como "VERIFICAR" u "OJO". Los más importantes son:

- **RUTs que casi seguro están mal en la fuente:**
  - `235-6` Gustavo Alessandri Valdés (Cía. Chilena de Fósforos). Tiene pasado político: fue diputado y alcalde.
  - `401.301-8` Carlos Croxatto Silva (Copec).
  - En los dos casos hay que buscar el RUT real en la memoria o en la CMF.
- **Ortografía en conflicto:**
  - Tuset Jorratt / Tusset Jorrat
  - Prado / Padró Lavín
  - Truffello / Trufello
  - Giessen / Giesen
  - Anthony / Antony Fyfe
  - Gian Paolo / Gian Pablo Raineri
- **Posible confusión entre familiares:**
  - Mateo / Ricardo Budinich Díez (Copec).
  - Rafael / Francisco Javier Marín Jordán (CGE Distribución).
  - Jorge Bernardo Larraín Matte, conocido como Bernardo Larraín Matte. Tiene un hermano llamado Jorge Larraín Matte, así que hay que confirmar a cuál de los dos corresponde el RUT.
- **Segundos nombres que no se pudieron confirmar:** Esteban Jadresic Marinovic. Se omitió su segundo nombre porque en la base aparece como DASLAV y como MAXIMILIANO, y DASLAV es el segundo nombre de su hermano Alejandro.

## Pistas políticas detectadas (hoja `pistas_politicas`)

Durante la verificación aparecieron 23 directores con cargos públicos o vínculos políticos. Entre ellos:

- **Ministros y exministros:**
  - Ferreiro Yazigi
  - Pérez Mackenna (Francisco y Rodrigo)
  - Cáceres Contreras
  - Estévez Valencia
  - Etchegaray Aubry
  - Moreno Charme
  - De Gregorio Rebeco
  - Morandé Lavín
  - Domínguez Covarrubias
  - Marshall Rivera
  - De la Cuadra Fabres (posible)
- **Parlamentarios y convencionales:**
  - Exdiputados: Alessandri Valdés y Leay Morán.
  - Exconvencionales constituyentes: Fontaine Talavera y Mayol Bouchón.
- **Empresas del Estado:** presidentes de Codelco, Metro y Enacar.

Es un punto de partida, no una búsqueda exhaustiva: solo se revisaron los 217 RUTs con variantes de nombre. Para la etapa de pasado político hay que revisar los 2.676 RUTs.

---

# Pasado político de los directores

Archivos:

- `datos/pasado_politico.tsv`: un registro por director, con los cargos, los períodos, las fuentes y el nivel de confianza.
- `scripts/integrar_pasado_politico.py`: agrega esa información a los dos Excel.

## Qué contienen los Excel

- **`maestro_directores_rut_verificado.xlsx`**, hoja `maestro_rut`: al lado de cada RUT y nombre hay seis columnas nuevas:
  - `pasado_politico` (SÍ / No identificado)
  - `tipo_cargo`
  - `cargos_politicos` (cargo y período)
  - `fuentes_cargo_politico` (URLs)
  - `confianza_cargo` (alta / media)
- Hoja **`pasado_politico`**: solo los 110 directores con pasado político identificado.
- **`interlocking_db_nombres_corregidos.xlsx`**: las mismas columnas en cada fila de la base. Son 1.376 filas director-empresa-año.

## Resultado: 110 de 2.676 directores (RUT)

| Tipo de cargo (un director puede tener varios) | Directores |
|---|---|
| Ministro/a | 66 |
| Directivo de empresa estatal (Codelco, BancoEstado, Corfo, ENAP, Metro, TVN, EFE, SEP) | 26 |
| Banco Central / organismo autónomo (Contraloría, Servel, superintendencias, CNTV, Comisión de Productividad) | 22 |
| Subsecretario/a | 15 |
| Jefe de servicio público (Dipres, SII, Odeplan, SECOM, Fonasa) | 12 |
| Parlamentario/a | 11 |
| Alcalde / Intendente | 8 |
| Cargo político en el extranjero (ministros españoles, Riksdag, FMI/BCE/BID) | 7 |
| Embajador/a | 5 |
| Convencional / proceso constituyente | 5 |

## Cómo se hizo y cuáles son sus límites

1. Desde este entorno solo hay acceso a un buscador web. Las bases oficiales (BCN, Cámara, Senado, Servel, InfoProbidad, Wikipedia) están bloqueadas, así que no se pudieron descargar las listas completas de cargos para cruzarlas por nombre.
2. Por eso se trabajó en dos pasos:
   - Se revisaron los 2.676 nombres y se seleccionaron unos 115 candidatos con probable trayectoria pública.
   - Cada candidato se verificó con búsquedas web y se registraron el cargo, el período y las URLs. Los candidatos que no se pudieron confirmar no se incluyeron. Por ejemplo, Jorge Selume Zaror (posible director de Presupuestos), Jaime Arellano Quintana, Isidoro Palma como subsecretario, Ernesto Tironi y Sergio Baeza.
3. **"No identificado" no significa "no tuvo cargo".** Esta revisión no captura bien:
   - cargos regionales o municipales menores (concejales, seremis, gobernadores provinciales);
   - funcionarios de segundo nivel (jefes de división, asesores);
   - militancia partidaria sin cargo.
4. **Para hacerlo exhaustivo** se recomienda cruzar los RUT o nombres con listas oficiales completas:
   - BCN, reseñas parlamentarias: diputados y senadores desde 1990.
   - Listas de ministros por cartera (Wikipedia / BCN).
   - Servel: candidatos y electos, con RUT.
   - InfoProbidad: declaraciones de autoridades, con RUT.

   Si habilitas esos dominios en la configuración de red del entorno, se puede hacer ese cruce de forma sistemática.
5. **Confianza:** "alta" significa cargo y período respaldados por fuentes concordantes. "Media" significa una sola fuente, o fechas no confirmadas.
6. Casos a tener en cuenta:
   - **Familiares de políticos** (los Ponce Pinochet, Tomic Errázuriz, Hurtado Vicuña, Matte, etc.): el parentesco no se registró como cargo político, salvo nota.
   - Jorge Marshall Rivera: es muy probable, pero no está confirmado, que el director de Provida sea el exministro.
   - En la base aparecen como "ADRIANA DEL PIANO PUELMA" y "RAPHAEL BERGOEING VEIA". Las fuentes los escriben DELPIANO y VELA, y la empresa calza en ambos casos.
