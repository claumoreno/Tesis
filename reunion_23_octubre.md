# Preparación para la reunión del viernes 23 de octubre

**Qué pidió el profesor Cid:** presentar la propuesta de tema, los objetivos y la metodología. Además, está disponible esta semana para consultas.

---

## 1. Lo más importante: aprovechar la tesis de Alejandro Capllonch

La tesis que se defendió el 16 de octubre construyó la **red de empresas chilenas conectadas por directores compartidos entre 2010 y 2024**. Para tu tesis esto es clave por dos razones:

1. **Ahorra la parte más pesada del trabajo.** Si el profesor puede compartir esa base (directores por empresa y por año), ya no tienes que armar la red desde cero. Solo te quedaría identificar cuáles de esos directores son políticos y agregar los datos financieros.
2. **Tu tesis queda como continuación natural de la suya.** Él describió *cómo evoluciona la red*; tú preguntas *si la red, y la presencia de políticos en ella, afecta la calidad de la información contable*. Pasas de un trabajo descriptivo a uno explicativo, dentro de la misma línea de investigación del profesor.

**Consecuencia:** conviene ajustar tu período a **2010–2024**, el mismo de esa base. Ese período incluye **3 elecciones presidenciales y parlamentarias (2013, 2017 y 2021)** y 4 municipales (2012, 2016, 2021 y 2024). Alcanza para responder la pregunta electoral.

---

## 2. Correo para pedir una consulta esta semana

Envíalo hoy o mañana, para alcanzar a reunirte antes del viernes.

> **Asunto:** Consulta propuesta de tesis – directores políticos y gestión de resultados
>
> Estimado profesor Cid:
>
> Junto con saludarlo, le escribo para coordinar una breve consulta esta semana antes de la reunión del viernes 23.
>
> Mi propuesta es estudiar si las empresas chilenas con directores con trayectoria política presentan diferencias en la gestión de resultados (*earnings management*), si esta relación cambia en los años electorales y si se transmite a través de la red de directores compartidos.
>
> Me gustaría consultarle tres puntos:
> 1. Si sería posible utilizar la base de directores y la red de empresas 2010–2024 que construyó Alejandro Capllonch en su tesis, para luego identificar a los directores con conexiones políticas.
> 2. Qué definición de "director político" le parece más adecuada (por ejemplo, exministros, exparlamentarios, exautoridades de servicios públicos y candidatos).
> 3. A qué bases de datos financieras tenemos acceso en la universidad (por ejemplo, Economática o Refinitiv) o si se recomienda trabajar con los estados financieros publicados por la CMF.
>
> Quedo a la espera de su disponibilidad. Muchas gracias.
>
> Saludos cordiales,
> [Tu nombre]

---

## 3. Contenido para presentar el viernes

Sirve para una presentación de 5 a 7 diapositivas o para un documento de 1 a 2 páginas.

### Diapositiva 1. Título
**Directores políticos, redes de directorio y gestión de resultados: evidencia de empresas chilenas en torno a los ciclos electorales**
Nombre, profesor guía Carlos Cid, fecha.

### Diapositiva 2. Motivación
- En Chile es frecuente que exministros, exparlamentarios y exautoridades lleguen a los directorios de empresas listadas (la "puerta giratoria").
- Las conexiones políticas pueden dar beneficios a la empresa, como acceso a información o a regulación, pero también pueden reducir la supervisión y la calidad de la información contable.
- Chile tiene un mercado concentrado, con grupos económicos y muchos directores compartidos, por lo que estos efectos pueden transmitirse por la red.
- **Vacío:** la literatura sobre conexiones políticas y calidad contable se ha hecho sobre todo en EE. UU. y Asia; hay poca evidencia para Chile que combine conexiones políticas, redes de directorio y ciclos electorales.

### Diapositiva 3. Preguntas de investigación
1. ¿Existen diferencias en la gestión de resultados entre empresas con y sin directores políticos?
2. ¿Se modifica esta relación durante los años electorales?
3. ¿La conexión indirecta con directores políticos a través de la red de directores compartidos, y la centralidad de la empresa en esa red, se relacionan con la gestión de resultados?

### Diapositiva 4. Objetivos
**Objetivo general:** determinar la relación entre la presencia de directores políticos y la gestión de resultados en empresas chilenas listadas entre 2010 y 2024, considerando el ciclo electoral y la red de directores compartidos.

**Objetivos específicos:**
1. Identificar a los directores con trayectoria política en las empresas de la muestra.
2. Estimar la gestión de resultados de cada empresa y año.
3. Comparar la gestión de resultados entre empresas con y sin directores políticos.
4. Evaluar si la relación cambia en los años electorales.
5. Evaluar el rol de la red de directores compartidos en esta relación.

### Diapositiva 5. Hipótesis y marco teórico
- **H1a (agencia, menor calidad contable):** las empresas con directores políticos gestionan más sus resultados (Faccio, 2006; Chaney, Faccio y Parsley, 2011).
- **H1b (costos políticos):** las empresas con directores políticos gestionan menos sus resultados, o los gestionan a la baja, porque están más expuestas al escrutinio (Watts y Zimmerman, 1978).
- **H2:** en los años electorales cambia la gestión de resultados de las empresas con directores políticos (Ramanna y Roychowdhury, 2010).
- **H3:** la gestión de resultados se transmite por la red de directores compartidos (Chiu, Teoh y Tian, 2013).

### Diapositiva 6. Metodología
- **Muestra:** sociedades anónimas abiertas no financieras que reportan a la CMF, de 2010 a 2024, en un panel empresa-año.
- **Datos:**
  - Directorios: base de la red 2010–2024, si está disponible, o memorias anuales de la CMF.
  - Trayectoria política: BCN, nóminas de ministros y subsecretarios, Servel y prensa.
  - Estados financieros: CMF, Economática o Refinitiv.
- **Variable dependiente:** acumulaciones discrecionales con el modelo de Jones modificado (Dechow et al., 1995), ajustado por desempeño (Kothari et al., 2005). Como robustez, gestión de actividades reales (Roychowdhury, 2006).
- **Variables principales:**
  - `POL`: la empresa tiene al menos un director político.
  - `ELEC`: año de elección presidencial y parlamentaria.
  - Variables de red: grado, centralidad y conexión indirecta con directores políticos.
- **Modelo:**
  `EM = β0 + β1·POL + β2·ELEC + β3·POL×ELEC + controles + efectos fijos de industria + ε`
  con errores estándar agrupados por empresa.
- **Controles:** tamaño, endeudamiento, ROA, crecimiento, auditor Big 4, tamaño e independencia del directorio y concentración de la propiedad.

### Diapositiva 7. Cronograma y factibilidad
| Período | Hito |
|---|---|
| Noviembre | Piloto de datos y anteproyecto |
| Diciembre | Recolección de datos |
| Enero | Cálculo de variables y marco teórico |
| Febrero | Regresiones y robustez |
| Marzo | Redacción final y entrega el 31 de marzo |

**Riesgo principal:** identificar a mano a los directores políticos. **Mitigación:** reutilizar la base de directores 2010–2024 y hacer un piloto temprano.

---

## 4. Preguntas que probablemente te hará el profesor (y cómo responderlas)

**¿Cómo vas a definir "director político"?**
Como una persona que ocupó un cargo de elección popular (parlamentario, alcalde o gobernador), un cargo de confianza en el Ejecutivo (ministro, subsecretario, intendente o superintendente), fue candidato o fue dirigente de partido. Como robustez se puede separar entre conexión actual y pasada, y entre conexión con el gobierno de turno y con la oposición.

**¿Cómo mides la gestión de resultados?**
Con las acumulaciones discrecionales: la parte de los ajustes contables que no se explica por la actividad normal de la empresa. Se estiman con el modelo de Jones modificado por industria y año. Uso el valor absoluto para medir la magnitud de la gestión y el valor con signo para su dirección.

**¿Por qué los años electorales?**
Porque en elecciones aumenta la visibilidad política de las empresas conectadas y cambian sus incentivos. Además, la fecha de la elección no la decide la empresa, así que funciona como un shock externo. Las elecciones presidenciales y parlamentarias en Chile son en noviembre y el año contable cierra el 31 de diciembre, así que los estados financieros del año electoral recogen el período de campaña.

**¿No será que las empresas que contratan políticos ya eran distintas? (endogeneidad)**
Sí, es un riesgo. Se puede abordar con:
- efectos fijos de empresa, que comparan a la misma empresa antes y después de incorporar a un director político;
- *propensity score matching*, que compara empresas similares;
- el diseño electoral, porque la elección es un shock externo.

**¿Cuántas observaciones vas a tener?**
Son unas 100 a 150 empresas no financieras en 15 años, es decir, del orden de 1.500 observaciones empresa-año. Hay que confirmarlo con el piloto.

**¿Qué aporta tu tesis respecto de la de Capllonch?**
Él describe cómo evoluciona la red. Yo uso esa red para explicar un resultado concreto, la calidad de la información contable, y le agrego la dimensión política y electoral.

---

## 5. Checklist de la semana

- [ ] **Lunes 19 o martes 20:** enviar el correo al profesor para coordinar la consulta.
- [ ] Leer al menos el resumen de Chaney, Faccio y Parsley (2011), Ramanna y Roychowdhury (2010) y Chiu, Teoh y Tian (2013), para citarlos con seguridad.
- [ ] Si es posible, conseguir el documento de la tesis de Capllonch y revisar su metodología y sus fuentes.
- [ ] Revisar en el sitio de la CMF la memoria anual de 2 o 3 empresas, por ejemplo una del grupo Luksic, una de Angelini y una eléctrica, para ver cómo se reporta el directorio. Sirve para decir en la reunión que los datos existen.
- [ ] Armar la presentación o el documento con el contenido de la sección 3.
- [ ] **Viernes 23:** reunión.
