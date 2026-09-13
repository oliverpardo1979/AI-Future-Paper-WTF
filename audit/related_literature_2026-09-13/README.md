# Auditoría de Related Literature

Fecha: 13 de septiembre de 2026. Archivo revisado: `sections_rewrite/02_literature.tex`, inicialmente sobre el commit `94fbc05`. Las correcciones se incorporaron en `9295ada`; posteriormente se verificó Liu y Wan con su texto completo.

## Resultado y alcance

La sección tiene 41 referencias distintas. Descargué 36 PDF completos, conservados únicamente en la carpeta local ignorada `tmp/related_literature_audit_2026-09-13/`. Leí los pasajes que sustentan las atribuciones y sus condiciones, identificados abajo. Consulté además el PDF completo de Melina y Villa mediante el lector web, aunque su descarga local falló. Cuatro referencias siguen sin verificación del texto completo.

**La auditoría no está cerrada.** La lectura fue dirigida a las afirmaciones de Related Literature; no significa que haya leído de principio a fin las 1.819 páginas descargadas ni que haya replicado las demostraciones o estimaciones de terceros. En varios artículos clásicos la copia accesible es una versión de trabajo anterior a la publicación: el respaldo señalado vale para esa versión y no certifica identidad con la edición final.

El informe inicial precedió a la edición del manuscrito. Las cinco correcciones enumeradas a continuación y las precisiones pertinentes quedaron incorporadas en `9295ada`, junto con el PDF actualizado. La verificación posterior de Liu y Wan no requirió modificar el manuscrito. No se modificaron la notación ni las simulaciones.

## Correcciones necesarias

### 1. No identificar sustitución CES con el desplazamiento de tareas

La explicación de Acemoglu y Restrepo (2019) es correcta, pero la frase “It captures the displacement and productivity forces” atribuye a nuestro modelo un mecanismo que no modela explícitamente. Ellos distinguen el desplazamiento por cambios en tareas de la sustitución dentro de tareas existentes. Nuestro modelo tiene una CES y no una frontera móvil de tareas. Confianza: **High**.

Propuesta:

> My model does not create new human tasks or explicitly reallocate a changing set of tasks between workers and machines. It instead studies how substitution between labor and AI services interacts with productivity gains.

Respaldo: [Acemoglu y Restrepo, pp. 3–5 de JEP](https://economics.mit.edu/sites/default/files/publications/Automation%20and%20New%20Tasks%20-%20How%20Technology%20Displace.pdf).

### 2. Hacer explícita la analogía con Karabarbounis y Neiman

Su CES combina capital y trabajo. Nuestro texto debe decirlo para no sugerir que su estimación identifica la elasticidad entre IA y trabajo. Confianza: **High**.

Propuesta para reemplazar “This mechanism is central…”:

> A related CES mechanism underlies Karabarbounis and Neiman (2014), who study how a decline in the relative price of investment induces substitution from labor toward capital and lowers labor’s income share.

Respaldo: [Karabarbounis y Neiman, introducción, PDF pp. 2–3](https://www.brentneiman.com/research/KN.pdf).

### 3. No llamar “proyectos completados” a repositorios

En Demirer, Musolff y Yang, el indicador intermedio cuenta repositorios en los que trabaja el desarrollador. No demuestra que todos esos proyectos hayan sido completados. La atenuación al llegar a lanzamientos de software sí está documentada. Confianza: **High**.

Propuesta:

> Consistent with this mechanism, Demirer, Musolff, and Yang (2026) find that large AI-induced gains in coding activity attenuate sharply when measured by software releases, and estimate strong complementarity between upstream output and downstream human effort.

Respaldo: [versión de septiembre de 2026, figura 1 e introducción, PDF pp. 3–6](https://www.nber.org/system/files/working_papers/w35275/w35275.pdf). Esa estimación sectorial no debe interpretarse como una calibración directa de nuestra elasticidad agregada.

### 4. Separar las dos bases tributarias de Korinek y Lockwood

Su primera etapa trata de la pérdida de importancia de los ingresos laborales como base tributaria; la segunda incorpora recursos absorbidos por IA que no se traducen en consumo humano. Nuestro resultado de participación laboral nula conecta con la primera, pero no demuestra la segunda. En nuestro régimen acotado dominado por IA, las constantes del apéndice implican una proporción de consumo positiva. Confianza: **High**.

Propuesta:

> The vanishing labor income share connects to Korinek and Lockwood’s (2026) analysis of the erosion of the labor-income tax base relative to output. Their additional concern about an economy centered on AI rather than human consumption goes beyond the mechanism studied here.

Respaldo: [Korinek y Lockwood, PDF pp. 3–5, tabla 1](https://www.nber.org/system/files/working_papers/w34873/w34873.pdf). La distinción entre niveles y proporciones también importa aquí.

### 5. Explicar el contraste de tasas de interés

La afirmación “can raise” no es falsa. Pero Melina y Villa encuentran respuestas más fuertes de la tasa natural con complementariedad, y pequeñas o incluso negativas con mayor sustituibilidad. Es mejor convertirlos en un contraste explícito que presentarlos solo como respaldo de tasas mayores. Estudian dinámica de corto plazo en un DSGE; nuestro resultado se refiere al retorno de largo plazo al capital. Confianza: **High**.

Propuesta de precisión, después de mencionar sus escenarios:

> Melina and Villa (2025) find a stronger increase in the short-run natural rate when ICT complements labor; greater substitutability can weaken or reverse that response. Their mechanism differs from the long-run return on capital studied here.

Respaldo: [Melina y Villa, PDF pp. 22 y 33–34](https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025224-source-pdf.pdf).

## Precisiones útiles, sin necesidad de extender la sección

- **Korinek y Suh:** añadir “In their baseline model” a la referencia a una frontera exógena. El artículo también contiene una extensión con innovación.
- **Pitchford, Jones–Manuelli y Rebelo:** separar el resultado CES de la tradición de crecimiento convexo/AK. No son tres pruebas de una condición tecnológica idéntica.
- **Hémous y Olsen:** su incentivo específico para automatizar aumenta con los salarios de trabajadores de baja cualificación; “rising low-skill wages” es más preciso que “rising wages”.
- **GATE:** conservar la descripción como problema del planificador, reconociendo sus cuñas opcionales de externalidades. No afirmar que allí la inversión es exógena.
- **Athey y Scott Morton:** no trasladar directamente a nuestro modelo de propiedad doméstica sus pérdidas de bienestar asociadas con rentas pagadas al exterior.
- **Demirer et al. (mercado de LLM):** sus datos de APIs respaldan la cautela frente al monopolio literal, no una descripción exhaustiva de todos los mercados de IA.

## Qué se sostiene de nuestra contribución

La decisión privada de invertir en investigación **no es novedosa por sí sola**: Romer, Aghion–Howitt, Acemoglu–Restrepo y Hémous–Olsen son antecedentes claros. Tampoco basta hablar de progreso de IA endógeno: GATE elige inversión, Davidson et al. modelan retroalimentación tecnológica y económica, y Jones–Tonetti endogeneizan ideas y automatización.

La distinción defendible es más concreta: nuestro desarrollador elige gasto en investigación comparando costo corriente y beneficio monopólico futuro, conjuntamente con ahorro y acumulación de capital, y esa decisión determina la transición de salarios y participaciones. En la aplicación de Davidson y en la tabla 9 de Jones–Tonetti, las participaciones de investigación e inversión están fijadas; en GATE las elige un planificador. Las fuentes apoyan esta distinción, pero esta auditoría no constituye una prueba de prioridad frente a toda la literatura.

La lectura de Liu y Wan confirma un antecedente cercano: sus proveedores de ANI y AGI eligen entrenamiento para maximizar beneficios descontados, ecuaciones (14) y (20). No puede distinguirse nuestro modelo del suyo diciendo simplemente que la investigación responde a beneficios futuros. Comparan sendas de crecimiento balanceado de una economía descentralizada —que ya incluye proveedores con poder de mercado—, un planificador y un supermonopolista. Este último internaliza el efecto de sus decisiones sobre la tasa de interés, a diferencia del desarrollador de nuestro modelo, que toma esa trayectoria como dada. Sus diferencias entre tipos de IA, uso de datos y estructura de mercado no equivalen a nuestra caracterización de salarios y participaciones bajo sustitución CES.

Hay además un antecedente importante para las transiciones aparentemente tranquilas: [Duffy y Papageorgiou, PDF p. 9, nota 7](https://www.chrispapageorgiou.com/papers/jeg6.pdf) ya advierten que una economía encaminada a crecimiento sostenido y participación laboral nula puede no haber acumulado suficientes observaciones para que eso sea visible. Jones–Tonetti desarrollan directamente el papel de los eslabones débiles. Nuestra contribución debe recaer en la caracterización e incentivos específicos, no en presentar la demora como una intuición sin precedentes.

La restricción “among the long-run regimes characterized here with a finite upper bound” debe mantenerse en la equivalencia entre prima de crecimiento salarial y participación laboral nula. La sección 5.2 de nuestro propio paper muestra por qué no puede extenderse sin esa restricción al caso no acotado de elasticidad unitaria.

## Pendientes para cerrar la revisión

Falta acceso al texto completo de:

1. Lu (2021), *The Impact of Artificial Intelligence on Economic Growth and Welfare*.
2. Gersbach, Komarov y von Maydell (2025), *Artificial Intelligence as Self-Learning Capital*.
3. Mullainathan y Rambachan (2025), *Science in the Age of Algorithms*.
4. Pitchford (1960), *Growth and the Elasticity of Factor Substitution*.

Sus registros, resúmenes o citas secundarias no se usan como sustitutos de la verificación solicitada. También falta guardar una copia local del PDF de Melina y Villa, que sí pude consultar por web. La comparación con las versiones finales de los trabajos marcados como “versión consultada” queda explícitamente pendiente.

## Registro de evidencia, referencia por referencia

Las páginas siguientes son páginas del PDF descargado, salvo indicación distinta. “Respaldada” significa que los pasajes consultados respaldan la atribución delimitada, no que se haya certificado todo resultado del artículo.

### 1. Romer, Paul M. (1990)

[Endogenous Technological Change](https://web.stanford.edu/~klenow/Romer_1990.pdf)

- Clave: `romer1990`.
- Versión: Artículo publicado, JPE 1990.
- Páginas consultadas: 2–5 (S71–S74).
- Atribución revisada: La inversión en investigación produce conocimiento no rival.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El modelo vincula decisiones de investigación con incentivos de mercado y conocimiento parcialmente excluible. Es un antecedente de B no rival, no de nuestro monopolista integrado ni de sus resultados distributivos.

### 2. Aghion, Philippe and Howitt, Peter (1992)

[A Model of Growth through Creative Destruction](https://www.nber.org/system/files/working_papers/w3223/w3223.pdf)

- Clave: `aghionhowitt1992`.
- Versión: NBER 3223, enero de 1990; antecedente del artículo de 1992.
- Páginas consultadas: 2–5.
- Atribución revisada: El cambio tecnológico responde a inversión privada en investigación.
- Dictamen: **Respaldada en la versión consultada**. Confianza: **Medium**.
- Conexión y límites: Las rentas monopólicas esperadas financian innovación; la destrucción creativa afecta esos incentivos. No se cotejó línea por línea con la versión final de Econometrica.

### 3. Jones, Charles I. (1995)

[R&D-Based Models of Economic Growth](https://web.stanford.edu/~chadj/JonesJPE95.pdf)

- Clave: `jones1995`.
- Versión: Artículo publicado, JPE 1995.
- Páginas consultadas: 2–4 (759–761), lectura visual.
- Atribución revisada: La investigación genera conocimiento endógenamente.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El artículo conserva investigación con incentivos privados, aunque elimina efectos de escala y hace depender el crecimiento de largo plazo de parámetros exógenos. Citarlo no obliga a renombrar nuestro modelo. El PDF es una imagen escaneada: se leyeron las páginas renderizadas.

### 4. Trammell, Philip and Korinek, Anton (2023)

[Economic Growth under Transformative AI](https://www.nber.org/system/files/working_papers/w31815/w31815.pdf)

- Clave: `trammellkorinek2023`.
- Versión: NBER 31815, revisión de abril de 2026.
- Páginas consultadas: 2–5.
- Atribución revisada: Distingue automatización de producción y automatización de investigación.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: La distinción organiza las secciones 2–4. El artículo también advierte que los efectos sobre salarios dependen de otros supuestos; no es un teorema universal de salarios crecientes.

### 5. Mullainathan, Sendhil and Rambachan, Ashesh (2025)

[Science in the Age of Algorithms](https://www.nber.org/books-and-chapters/economics-transformative-ai/science-age-algorithms)

- Clave: `mullainathanrambachan2025`.
- Versión: Capítulo identificado en NBER y en la página del autor en MIT.
- Páginas consultadas: No verificadas en texto completo.
- Atribución revisada: La IA reorganiza la generación de ideas y selección de teorías.
- Dictamen: **Pendiente: acceso**. Confianza: **Low**.
- Conexión y límites: La descarga pública del capítulo devuelve 403. La identificación bibliográfica y los extractos indexados no sustituyen la lectura del texto completo. No certifico todavía esta atribución.

### 6. Lu, Chia-Hui (2021)

[The Impact of Artificial Intelligence on Economic Growth and Welfare](https://doi.org/10.1016/j.jmacro.2021.103342)

- Clave: `lu2021ai`.
- Versión: Journal of Macroeconomics 69, 103342 (2021), registro editorial.
- Páginas consultadas: No verificadas en texto completo.
- Atribución revisada: La IA es un insumo no rival que contribuye a su propia acumulación.
- Dictamen: **Pendiente: acceso**. Confianza: **Low**.
- Conexión y límites: El resumen editorial concuerda con esta descripción general, pero no pude inspeccionar las ecuaciones ni la asignación de recursos del artículo completo. No usarlo todavía como evidencia precisa de una decisión intertemporal privada equivalente a la nuestra.

### 7. Gersbach, Hans and Komarov, Evgenij and von Maydell, Richard (2025)

[Artificial Intelligence as Self-Learning Capital](https://doi.org/10.1016/j.econmod.2025.107221)

- Clave: `gersbachetal2025`.
- Versión: Economic Modelling 153, 107221 (2025); existe antecedente CEPR 17221 (2022).
- Páginas consultadas: No verificadas en texto completo.
- Atribución revisada: Capital autoaprendiz que mejora por uso y asignación de trabajo cualificado a investigación.
- Dictamen: **Pendiente: acceso**. Confianza: **Low**.
- Conexión y límites: El repositorio ETH identifica el PDF publicado pero la descarga falla; CEPR tampoco permitió recuperar el texto. No certifico la parte específica sobre asignación de trabajo a partir del resumen.

### 8. Davidson, Tom and Halperin, Basil and Houlden, Thomas and Korinek, Anton (2026)

[When Does Automating AI Research Produce Explosive Growth? Feedback Loops in Innovation Networks](https://thomas-houlden.com/assets/DHHK_May2026.pdf)

- Clave: `davidsonetal2026`.
- Versión: PDF de los autores, mayo de 2026.
- Páginas consultadas: 2–7; 22; 39; 41–43.
- Atribución revisada: Dos circuitos de retroalimentación; ahorro y participaciones de recursos fijos en la aplicación; complementariedades generan bottlenecks.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: La p. 22 fija tasas de ahorro; la p. 39 fija participaciones de investigación y remite a GATE para endogeneizarlas. Las pp. 41–43 explican los cuellos de botella y condiciones de automatización que los superan. La comparación debe seguir referida a su aplicación, no negar toda endogeneidad tecnológica en el artículo.

### 9. Erdil, Ege and Potlogea, Andrei and Besiroglu, Tamay and Roldan, Edu and Ho, Anson and Sevilla, Jaime and Barnett, Matthew and Vrzla, Matej and Sandler, Robert (2025)

[GATE: An Integrated Assessment Model for AI Automation](https://arxiv.org/pdf/2503.04941)

- Clave: `erdiletal2025gate`.
- Versión: GATE, PDF de arXiv, 85 páginas.
- Páginas consultadas: 4–5; 8; 35–37; 65–67.
- Atribución revisada: Un planificador optimiza inversión y asignación de cómputo entre entrenamiento e inferencia.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El apéndice C enumera las decisiones. El módulo de externalidades introduce un planificador que infravalora retornos mediante cuñas; no es la solución del monopolista privado de nuestro modelo. No afirmar que GATE carece de inversión endógena.

### 10. Korinek, Anton and Suh, Donghyun (2024)

[Scenarios for the Transition to AGI](https://www.nber.org/system/files/working_papers/w32255/w32255.pdf)

- Clave: `korineksuh2024`.
- Versión: NBER 32255.
- Páginas consultadas: 3–6.
- Atribución revisada: Frontera de automatización exógena y transición con acumulación de capital.
- Dictamen: **Respaldada; precisar alcance**. Confianza: **High**.
- Conexión y límites: Es correcto para el modelo base. La p. 6 también anuncia una extensión con innovación y automatización del progreso tecnológico. Conviene escribir «In their baseline model» para no describir todo el artículo como tecnología exógena.

### 11. Korinek, Anton and Jones, Charles I. and Sacher, Szymon and Cotter, Tess and McCrory, Peter (2026)

[Economic Scenarios for Transformative AI](https://www-cdn.anthropic.com/files/4zrzovbb/website/cf58f84d46a4a76bf5a5b039ac695fba6b80041c.pdf)

- Clave: `korineketal2026scenarios`.
- Versión: Informe técnico Anthropic, 57 páginas, descargado desde su enlace oficial.
- Páginas consultadas: 4; 17; 35–36.
- Atribución revisada: Escenarios hasta 2030; RSI incorporado en la productividad asumida; salarios medios pueden subir mientras caen salarios cognitivos.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: La p. 17 declara que el efecto de RSI está incorporado en la trayectoria asumida. Las pp. 35–36 distinguen salarios, empleo y comparación con el contrafactual. Son escenarios condicionados, no pronósticos demostrados; el promedio salarial no es el ingreso medio incluyendo desempleados.

### 12. Aghion, Philippe and Jones, Benjamin F. and Jones, Charles I. (2019)

[Artificial Intelligence and Economic Growth](https://www.nber.org/system/files/working_papers/w23928/w23928.pdf)

- Clave: `aghionjonesjones2019`.
- Versión: NBER 23928 (2017), antecedente del capítulo de 2019.
- Páginas consultadas: 3–5.
- Atribución revisada: La lógica de Baumol limita la expansión agregada cuando quedan tareas esenciales difíciles de automatizar.
- Dictamen: **Respaldada en la versión consultada**. Confianza: **Medium**.
- Conexión y límites: El mecanismo se expone explícitamente en la introducción y organiza los modelos de bienes e ideas. No pude comparar esta copia de trabajo con toda la versión final del capítulo.

### 13. Jones, Benjamin F. (2025)

[Artificial Intelligence in Research and Development](https://www.nber.org/system/files/working_papers/w34312/w34312.pdf)

- Clave: `jones2025rd`.
- Versión: NBER 34312, octubre de 2025.
- Páginas consultadas: 1; 3–5.
- Atribución revisada: La cobertura de tareas, productividad de la IA y complementariedades determinan su aporte a investigación.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El título correcto es Artificial Intelligence in Research and Development. El artículo asigna un presupuesto dado de investigación; no elige mediante nuestro equilibrio general cuánto gastar en total.

### 14. Pitchford, John D. (1960)

[Growth and the Elasticity of Factor Substitution](https://doi.org/10.1111/j.1475-4932.1960.tb00537.x)

- Clave: `pitchford1960`.
- Versión: Economic Record 36(76), 491–504; reimpresión identificada en Cambridge.
- Páginas consultadas: No verificadas en texto completo.
- Atribución revisada: Sustituibilidad y posibilidad de crecimiento sostenido con factores acumulables.
- Dictamen: **Pendiente: acceso**. Confianza: **Low**.
- Conexión y límites: La atribución tiene respaldo indirecto explícito en Duffy y Papageorgiou, pero eso no cumple la exigencia de leer el original. Las descargas de la muestra y extracto de Cambridge no funcionaron. No certifico el original.

### 15. Jones, Larry E. and Manuelli, Rodolfo E. (1990)

[A Convex Model of Equilibrium Growth: Theory and Policy Implications](https://www.nber.org/system/files/working_papers/w3241/w3241.pdf)

- Clave: `jonesmanuelli1990`.
- Versión: NBER 3241, antecedente del artículo de JPE 1990.
- Páginas consultadas: 3–7.
- Atribución revisada: El crecimiento puede sostenerse con tecnología convexa y rendimientos marginales que no desaparecen.
- Dictamen: **Respaldada en la versión consultada**. Confianza: **Medium**.
- Conexión y límites: Es un resultado más general que una CES con elasticidad alta. Conviene distinguir esta tradición de crecimiento convexo/AK del resultado específico sobre elasticidad de Pitchford.

### 16. Rebelo, Sergio (1991)

[Long-Run Policy Analysis and Long-Run Growth](https://www.nber.org/system/files/working_papers/w3325/w3325.pdf)

- Clave: `rebelo1991`.
- Versión: NBER 3325, abril de 1990; antecedente del artículo de JPE 1991.
- Páginas consultadas: 2–4.
- Atribución revisada: Un núcleo de factores acumulables permite crecimiento con rendimientos constantes.
- Dictamen: **Respaldada en la versión consultada**. Confianza: **Medium**.
- Conexión y límites: El artículo parte de un modelo lineal en capital y lo generaliza. No es necesario atribuirle una condición CES idéntica a la nuestra. Falta cotejo con la edición final de JPE.

### 17. Duffy, John and Papageorgiou, Chris (2000)

[A Cross-Country Empirical Investigation of the Aggregate Production Function Specification](https://www.chrispapageorgiou.com/papers/jeg6.pdf)

- Clave: `duffypapageorgiou2000`.
- Versión: Borrador final de los autores, marzo de 2000.
- Páginas consultadas: 2–9; especialmente 9, sección 2.2 y nota 7.
- Atribución revisada: Una elasticidad alta no basta: la productividad del factor acumulable debe superar un umbral.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: La condición también depende de ahorro, población y depreciación. La nota 7 ya observa que el destino de crecimiento sostenido y participación laboral nula puede no ser visible aún en los datos. La demora en detectar el régimen no debe presentarse como una intuición enteramente nueva.

### 18. Nordhaus, William D. (2021)

[Are We Approaching an Economic Singularity? Information Technology and the Future of Economic Growth](https://www.nber.org/system/files/working_papers/w21547/w21547.pdf)

- Clave: `nordhaus2021`.
- Versión: NBER 21547, septiembre de 2015; antecedente del artículo de 2021.
- Páginas consultadas: 3–4; 8–13.
- Atribución revisada: La sustitución entre información e insumos convencionales es central para una singularidad económica.
- Dictamen: **Respaldada en la versión consultada**. Confianza: **Medium**.
- Conexión y límites: Las pp. 11–13 separan mecanismos de demanda y oferta y explican por qué el avance del cómputo no basta. La cita actual no atribuye a Nordhaus una prueba de inexistencia de nuestro equilibrio. Falta cotejo de la versión publicada.

### 19. Jones, Charles I. and Tonetti, Christopher (2026)

[Past Automation and Future A.I.: How Weak Links Tame the Growth Explosion](https://web.stanford.edu/~chadj/JonesTonetti_Automation.pdf)

- Clave: `jonestonetti2026`.
- Versión: Versión 0.5, mayo de 2026.
- Páginas consultadas: 1–3; 33–34; 37–39.
- Atribución revisada: Los eslabones débiles demoran la aceleración pese a la automatización.
- Dictamen: **Respaldada; conexión adicional útil**. Confianza: **High**.
- Conexión y límites: También endogeneizan ideas y automatización. La tabla 9 fija las proporciones de producto destinadas a investigación e inversión. Es un antecedente especialmente útil para distinguir tecnología endógena de gasto privado óptimo; no debe quedar descrito como un modelo sin investigación endógena.

### 20. Demirer, Mert and Musolff, Leon and Yang, Liyuan (2026)

[Writing Code vs. Shipping Code: Productivity Effects across Generations of AI Coding Tools](https://www.nber.org/system/files/working_papers/w35275/w35275.pdf)

- Clave: `demirermusolffyang2026`.
- Versión: NBER 35275, revisión de septiembre de 2026.
- Páginas consultadas: 2–6, figura 1.
- Atribución revisada: Las ganancias de codificación se atenúan al pasar a proyectos y lanzamientos.
- Dictamen: **Corregir precisión**. Confianza: **High**.
- Conexión y límites: El indicador de proyectos es repositorios en los que se trabaja, no necesariamente proyectos completados. Sustituir «completed software projects» por «repositories touched» o centrarse en «software releases». La elasticidad estimada es local a etapas de producción de software, no nuestra elasticidad macroeconómica IA–trabajo.

### 21. Restrepo, Pascual (2025)

[We Won't Be Missed: Work and Growth in the AGI World](https://www.nber.org/system/files/working_papers/w34423/w34423.pdf)

- Clave: `restrepo2025agi`.
- Versión: NBER 34423.
- Páginas consultadas: 3–5.
- Atribución revisada: Distingue trabajo indispensable para crecer de trabajo suplementario; con AGI la participación laboral puede desaparecer.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: Su premisa permite automatizar todo trabajo y acota los coeficientes de cómputo necesarios. Nuestro caso de servicios sustitutos no es idéntico a esa premisa. La cita conserva esa diferencia.

### 22. Gans, Joshua S. (2025)

[Growth in AI Knowledge](https://www.nber.org/system/files/working_papers/w33907/w33907.pdf)

- Clave: `gans2025aiknowledge`.
- Versión: NBER 33907, Growth in AI Knowledge.
- Páginas consultadas: 3–5.
- Atribución revisada: Un umbral de capacidad cambia la dirección de la investigación entre densificación y exploración.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El umbral se refiere a cobertura/precisión e incentivos para investigar en el espacio de conocimiento, no a reemplazar trabajo en producción final. El texto actual distingue correctamente ambos umbrales.

### 23. Acemoglu, Daron and Restrepo, Pascual (2019)

[Automation and New Tasks: How Technology Displaces and Reinstates Labor](https://economics.mit.edu/sites/default/files/publications/Automation%20and%20New%20Tasks%20-%20How%20Technology%20Displace.pdf)

- Clave: `acemoglurestrepo2019`.
- Versión: Artículo publicado, JEP 33(2), 2019.
- Páginas consultadas: 1–3 (3–5 de JEP).
- Atribución revisada: Distingue desplazamiento, productividad y reincorporación del trabajo mediante nuevas tareas.
- Dictamen: **Corregir conexión con nuestro modelo**. Confianza: **High**.
- Conexión y límites: La atribución al artículo es correcta. Lo impreciso es decir que nuestra CES contiene su displacement effect: ellos separan cambios del contenido de tareas y sustitución dentro de tareas existentes. Nuestro modelo no mueve una frontera de tareas ni crea tareas humanas.

### 24. Karabarbounis, Loukas and Neiman, Brent (2014)

[The Global Decline of the Labor Share](https://www.brentneiman.com/research/KN.pdf)

- Clave: `karabarbounisneiman2014`.
- Versión: Borrador de octubre de 2013 de los autores; artículo QJE 2014.
- Páginas consultadas: 1–3.
- Atribución revisada: La sustitución hacia un factor más barato puede reducir la participación laboral.
- Dictamen: **Precisar analogía**. Confianza: **High**.
- Conexión y límites: Su análisis usa capital y trabajo y una caída del precio relativo de inversión, no IA y trabajo. Sustituir «This mechanism is central» por una conexión explícita con la misma lógica CES aplicada a otros insumos. No importar su elasticidad como calibración de sigma.

### 25. Autor, David H. and Kausik, B. N. (2026)

[Resolving the Automation Paradox: Falling Labor Share, Rising Wages](https://arxiv.org/pdf/2601.06343)

- Clave: `autorkausik2026`.
- Versión: arXiv 2601.06343v1, enero de 2026.
- Páginas consultadas: 1–4, teorema 1 y aplicación CES.
- Atribución revisada: La automatización puede elevar salarios y reducir simultáneamente la participación laboral.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El verbo «can» es apropiado. No afirmar que nuestro resultado es un caso particular del teorema 1: su familia de tecnologías y su ejercicio sobre la participación laboral difieren de nuestro equilibrio con tres insumos y desarrollador.

### 26. Ray, Debraj and Mookherjee, Dilip (2022)

[Growth, Automation, and the Long-Run Share of Labor](https://www.nber.org/system/files/working_papers/w26658/w26658.pdf)

- Clave: `raymookherjee2022`.
- Versión: NBER 26658, enero de 2020; texto fechado diciembre de 2019.
- Páginas consultadas: 2–4.
- Atribución revisada: La acumulación de capital puede llevar la participación laboral a cero mientras los salarios crecen indefinidamente.
- Dictamen: **Respaldada en la versión consultada**. Confianza: **Medium**.
- Conexión y límites: Es explícitamente una posibilidad, no una predicción para cualquier parametrización. El mecanismo distingue capital reproducible y límites de capital humano. Falta cotejo de la versión publicada de 2022.

### 27. Farboodi, Maryam and Koh, Andrew J. and Xia, Anchi (2026)

[Data-Driven Automation](https://www.nber.org/system/files/working_papers/w35320/w35320.pdf)

- Clave: `farboodikohxia2026`.
- Versión: NBER 35320, Data-Driven Automation.
- Páginas consultadas: 3–6; 25–26; 39–40; pasaje de prueba en 72.
- Atribución revisada: Los datos generados por producción mejoran y amplían la automatización; pueden coexistir crecimiento explosivo y salarios estancados.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: Las proposiciones 3 y 7 respaldan la descripción. La p. 26 señala que el estancamiento también aplica con acumulación de capital. No equiparar sus datos acumulados como subproducto con nuestro gasto M elegido por el desarrollador, ni importar su definición de trayectoria óptima hacia nuestro equilibrio.

### 28. Korinek, Anton and Lockwood, Lee M. (2026)

[Public Finance in the Age of AI: A Primer](https://www.nber.org/system/files/working_papers/w34873/w34873.pdf)

- Clave: `korineklockwood2026`.
- Versión: NBER 34873, Public Finance in the Age of AI: A Primer.
- Páginas consultadas: 3–5, tabla 1.
- Atribución revisada: La transformación por IA puede erosionar bases tributarias laborales y de consumo humano.
- Dictamen: **Precisar conexión**. Confianza: **High**.
- Conexión y límites: La fuente distingue dos etapas. La desaparición de la base laboral como proporción del producto conecta directamente con nuestro modelo. La desaparición adicional del consumo humano requiere otro mecanismo; no se deriva automáticamente de participación laboral cero.

### 29. Chow, Trevor and Halperin, Basil and Mazlish, J. Zachary (2026)

[Transformative AI, Existential Risk, and Real Interest Rates](https://www.basilhalperin.com/papers/agi_emh.pdf)

- Clave: `chowhalperinmazlish2026`.
- Versión: Borrador de junio de 2026; primera versión enero de 2023.
- Páginas consultadas: 1–3.
- Atribución revisada: La expectativa de mayor crecimiento del consumo eleva tasas reales de largo plazo mediante suavización intertemporal.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El argumento incluye además riesgo existencial y se condiciona a un modelo de precios de activos. No identifica cualquier tasa observada con nuestro retorno neto al capital.

### 30. Rachel, Lukasz (2025)

[What Next for r*? A Capital Market Equilibrium Perspective on the Natural Rate of Interest](https://www.brookings.edu/wp-content/uploads/2025/09/3_Rachel_unembargoed.pdf)

- Clave: `rachel2025`.
- Versión: BPEA conference draft, septiembre de 2025.
- Páginas consultadas: 1–3; 7; 43; 46; 48.
- Atribución revisada: Un escenario de IA puede elevar la tasa natural mediante ahorro e inversión.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El escenario modifica crecimiento de productividad, markups y participación laboral. Es un ejercicio condicionado, no una estimación causal aislada del efecto de RSI.

### 31. Melina, Giovanni and Villa, Stefania (2025)

[From Servers to Rates: AI, ICT Capital, and the Natural Rate](https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025224-source-pdf.pdf)

- Clave: `melinavilla2025`.
- Versión: IMF WP/25/224, octubre de 2025.
- Páginas consultadas: 6–7; 22; 31–34 (PDF consultado por web).
- Atribución revisada: La inversión en IA/ICT puede elevar la tasa natural, con signo dependiente del régimen.
- Dictamen: **Texto consultado; descarga pendiente; precisar contraste**. Confianza: **High**.
- Conexión y límites: La fuente usa una tasa natural de corto plazo de un DSGE y encuentra respuestas más fuertes con complementariedad; con sustituibilidad pueden ser pequeñas o negativas. No avala directamente nuestra estática de largo plazo. El lector web permitió consultar el PDF, pero no se obtuvo copia local.

### 32. Wachter, Jessica and Wachter, Jonathan (2026)

[What Investment Data Implies about the AI Transition](https://www.nber.org/system/files/working_papers/w35290/w35290.pdf)

- Clave: `wachterwachter2026`.
- Versión: NBER 35290, junio de 2026.
- Páginas consultadas: 2–4.
- Atribución revisada: Datos de inversión disciplinan escenarios de expansión de IA y una tasa libre de riesgo mayor.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El resultado depende de calibración, preferencias y riesgo de booms. El título y los dos autores corresponden al PDF. No es una identidad entre gasto observado y crecimiento futuro seguro.

### 33. Korinek, Anton and McKelvey, Patrick (2026)

[Measuring the AI Economy](https://www.bankofcanada.ca/wp-content/uploads/2026/06/swp2026-20.pdf)

- Clave: `korinekmckelvey2026`.
- Versión: Bank of Canada Staff Working Paper 2026-20.
- Páginas consultadas: 4–6.
- Atribución revisada: Distingue cómputo físico y producción de IA ajustada por calidad en inferencia y entrenamiento.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: La metodología usa precios API a rendimiento constante y progreso algorítmico. Nuestro B común a ambos usos es una simplificación del modelo, no una variable que esos autores hayan medido exactamente.

### 34. Coyle, Diane and Poquiz, John Lourenze S. (2025)

[Making AI Count: The Next Measurement Frontier](https://www.nber.org/system/files/working_papers/w34330/w34330.pdf)

- Clave: `coylepoquiz2025`.
- Versión: NBER 34330.
- Páginas consultadas: 3–5.
- Atribución revisada: Medir insumos, producción, calidad y procesos transformados por IA plantea dificultades.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El artículo explica por qué las clasificaciones y matrices insumo-producto pueden mostrar tarde la transformación. No suministra una serie observada de nuestra eficiencia B ni una estimación de omega_X.

### 35. Acemoglu, Daron and Restrepo, Pascual (2018)

[The Race between Man and Machine: Implications of Technology for Growth, Factor Shares, and Employment](https://economics.mit.edu/sites/default/files/publications/The%20Race%20Between%20Man%20and%20Machine%20-%20Implications%20of.pdf)

- Clave: `acemoglurestrepo2018`.
- Versión: Artículo publicado, AER 108(6), 2018.
- Páginas consultadas: 24–28; 37.
- Atribución revisada: Una oferta fija de científicos se asigna entre automatización y nuevas tareas según beneficios esperados.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: La nota 25 explica que esta elección de insumo permite estudiar la dirección, no el volumen total de cambio tecnológico. Las ecuaciones 22 y 28 y los valores de innovación respaldan nuestra distinción.

### 36. Hémous, David and Olsen, Morten (2022)

[The Rise of the Machines: Automation, Horizontal Innovation, and Income Inequality](https://morten-olsen.com/wp-content/uploads/2025/10/Rise_of_the_machines_Hemous_olsen.pdf)

- Clave: `hemousolsen2022`.
- Versión: Artículo publicado, AEJ: Macroeconomics 14(1), 2022.
- Páginas consultadas: 1–3 (179–181).
- Atribución revisada: Innovación horizontal y automatización responden a incentivos, reforzados por salarios de baja cualificación mayores.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: Es importante conservar «low-skill wages» al describir su canal concreto. No es un modelo de investigación autónoma en IA. El antecedente de innovación privada y distribución sí es directo.

### 37. Korinek, Anton and Vipra, Jai (2025)

[Concentrating Intelligence: Scaling and Market Structure in Artificial Intelligence](https://www.nber.org/system/files/working_papers/w33139/w33139.pdf)

- Clave: `korinekvipra2025`.
- Versión: NBER 33139, texto de noviembre de 2024; antecedente de Economic Policy 2025.
- Páginas consultadas: 3–5.
- Atribución revisada: Fuerzas de escala y estructura de mercado pueden concentrar la provisión de IA.
- Dictamen: **Respaldada en la versión consultada**. Confianza: **Medium**.
- Conexión y límites: También describe competencia intensa y cambios de liderazgo. Justifica estudiar concentración como posibilidad, no afirmar que la no rivalidad obliga a un monopolio único. Falta cotejo con la edición final.

### 38. Gans, Joshua S. (2024)

[Market Power in Artificial Intelligence](https://www.nber.org/system/files/working_papers/w32270/w32270.pdf)

- Clave: `gans2024`.
- Versión: NBER 32270, Market Power in Artificial Intelligence.
- Páginas consultadas: 3–5.
- Atribución revisada: Revisa problemas de poder de mercado en IA.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: El foco es datos de entrenamiento, datos de entrada y predicciones. No atribuirle una prueba de que monopolizar toda la IA sea condición necesaria para innovar.

### 39. Athey, Susan and Scott Morton, Fiona (2025)

[Artificial Intelligence, Competition, and Welfare](https://www.nber.org/system/files/working_papers/w34444/w34444.pdf)

- Clave: `atheyscottmorton2025`.
- Versión: NBER 34444, Artificial Intelligence, Competition, and Welfare.
- Páginas consultadas: 3–4.
- Atribución revisada: El poder de mercado del proveedor de IA afecta precios, uso, remuneraciones y bienestar.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: Su IA importada y rentas que no se recirculan son relevantes para bienestar. Nuestro hogar posee el desarrollador; no trasladar automáticamente las pérdidas nacionales de su economía importadora a la nuestra.

### 40. Liu, Taoxiong and Wan, Ruidong (2026)

[AGI, ANI and Economic Growth](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=6776339)

- Clave: `liuwan2026`.
- Versión: SSRN 6776339; PDF de 107 páginas, fechado el 16 de mayo de 2026 en la portada.
- Páginas consultadas: 1–5, 8–10, 13–20, 28–31, 35–42 y 44. Son páginas del PDF; la numeración impresa es una unidad menor desde la introducción.
- Atribución revisada: Compara asignaciones descentralizada, planificada y de un supermonopolista con IA general y aplicaciones especializadas; vincula estructura de mercado e incentivos de innovación.
- Dictamen: **Respaldada**. Confianza: **High**.
- Evidencia: Las ecuaciones (14) y (20), PDF pp. 17 y 19, formulan decisiones de entrenamiento de los proveedores de ANI y AGI que maximizan beneficios descontados. La sección 4 caracteriza el planificador; la sección 5 introduce un supermonopolista que internaliza la tasa de interés (PDF p. 37 y problema (54), pp. 39–40). Las proposiciones 5–7 comparan sus sendas de crecimiento balanceado bajo las condiciones de cada resultado.
- Conexión y límites: La economía descentralizada ya incluye poder de mercado; no se compara una economía puramente competitiva con cualquier monopolio. La distinción adicional es la internalización estratégica de efectos macroeconómicos. Su mecanismo conecta IA general, aplicaciones especializadas y datos generados en la producción. Respalda la atribución actual y confirma que la inversión privada endógena en IA no es por sí sola nuestra contribución. No se verificaron todas sus pruebas ni se le atribuyen nuestros resultados CES sobre salarios y participaciones.
- Acceso: Tras el error 403 inicial, se descargó el PDF completo desde el enlace de SSRN abierto en el navegador. El manifiesto conserva el enlace público y el hash, no la URL firmada temporal.

### 41. Demirer, Mert and Fradkin, Andrey and Tadelis, Nadav and Peng, Sida (2025)

[The Emerging Market for Intelligence: Pricing, Supply, and Demand for LLMs](https://www.nber.org/system/files/working_papers/w34608/w34608.pdf)

- Clave: `demireretal2025`.
- Versión: NBER 34608, diciembre de 2025.
- Páginas consultadas: 2–4.
- Atribución revisada: Precios, entrada y diferenciación muestran un mercado distinto de un monopolio literal.
- Dictamen: **Respaldada**. Confianza: **High**.
- Conexión y límites: La evidencia procede de APIs de OpenRouter y Azure, no de todo uso mundial de IA. La cautela frente al monopolio es nuestra inferencia de esa evidencia, no un teorema del artículo.

## Reproducibilidad y conservación

- `source_manifest.json` registra URL de descarga, fecha, hash SHA-256 y errores de acceso. Su estado describe la descarga; no certifica la lectura.
- `attribution_review.json` contiene esta evaluación manual y su alcance.
- `download_urls.json` reúne enlaces públicos alternativos utilizados.
- `scripts/download_literature_audit.py` descarga y extrae texto por página; `scripts/read_literature_audit.py` permite recuperar las páginas señaladas.
- Los PDF y textos completos de terceros permanecen en `tmp/`, ignorado por Git. No se redistribuyen en el repositorio público.
- Los ejemplos de redacción documentan las propuestas originales; su implementación puede consultarse en `9295ada`. La entrada de Liu y Wan documenta la verificación posterior sin cambios adicionales al manuscrito.
- Ejecuté `scripts/validate_literature_audit.py`: comprobó cobertura de las 41 claves y hashes de los 36 PDF locales. Es una prueba de integridad y cobertura del registro, no una certificación automática de las atribuciones.
