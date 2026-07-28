# Mr. Prompter

> **Toolkit de ingeniería de prompts:** 7 modos especializados, 31 técnicas, 58 archivos Markdown de prompts, evaluación priorizando la seguridad, marco de selección de modelos.

Escribe prompts. Audítalos. Corrige sesiones fallidas. Extrae plantillas reutilizables de conversaciones. Elige el modelo de IA adecuado. Todo en una sola habilidad.

---

## tl;dr — 3 Pasos para tu Primer Prompt

```
1. "Escríbeme un prompt para [tarea]"          → modo GENERATE
2. Pega tu prompt actual + "revisa esto"      → modo VERIFY  
3. Pega el log de una conversación + "¿qué salió mal?" → modo DIAGNOSE
```

Eso es todo. Sin configuración, sin archivos de config. Solo describe lo que necesitas.

---

## Qué es esto (En lenguaje sencillo)

¿Sabes que hablar con la IA a veces se siente como lanzar espaguetis a la pared? Pruebas diferentes redacciones, corriges malentendidos, iteras hasta que funciona — ¿y la próxima vez empiezas desde cero?

**Esta habilidad soluciona eso.**

Tiene 7 modos para diferentes situaciones. Tú describes lo que necesitas, la habilidad elige el enfoque correcto y produce un prompt de calidad profesional — o analiza por qué tu última sesión se descarriló.

### El Patrón Principal

```
Describes la tarea → La habilidad construye el prompt óptimo → Usas el prompt con cualquier IA
                                                        ↓
                                           ¿La sesión salió mal? → DIAGNOSE
                                           ¿La sesión salió bien? → EXTRACT (guárdalo)
```

---

## Los 7 Modos de un Vistazo

| Modo | Tú dices... | Obtienes... | Cuándo usarlo |
|------|-----------|------------|-------------|
| **GENERATE** | "Escríbeme un prompt para X" | Prompt listo para usar + recomendación de modelo + chequeo de seguridad | Empezando desde cero |
| **VERIFY** | "Revisa este prompt" / "Audita esto" | Puntaje (0-10) + problemas específicos + correcciones | Antes de implementar un prompt |
| **IMPROVE** | "Mejora este prompt" | Prompt reescrito + qué cambió + por qué | Iterando sobre un prompt existente |
| **CHAIN** | "Análisis profundo de X" / "Crea una cadena de prompts" | Análisis multifase (2-4 prompts secuenciales) | Temas complejos que requieren múltiples ángulos |
| **MODEL SELECT** | "¿Qué modelo para X?" | Principal + alternativa + justificación | Eligiendo el modelo de IA adecuado |
| **DIAGNOSE** | "¿Qué salió mal?" / "Analiza esta sesión" | Puntos exactos de falla + parches concretos + métricas | Después de que una sesión se descarriló |
| **EXTRACT** | "Convierte este chat en un prompt" | Prompt reutilizable basado en la conversación | Guardando patrones exitosos |

### Guía Rápida de Decisión

```
¿Tarea nueva? ────────────────→ GENERATE
¿Tienes un prompt y quieres revisarlo? ──→ VERIFY
¿Tienes un prompt y quieres mejorarlo? → IMPROVE
¿Necesitas análisis profundo multifase? ───→ CHAIN
¿No sabes qué IA usar? ───────→ MODEL SELECT
¿La sesión salió mal? ───────────────→ DIAGNOSE
¿La sesión salió genial, quieres guardarla? ──────→ EXTRACT
```

---

## Ejemplos

### Ejemplo 1: GENERATE — "Necesito un prompt para revisión de código"

**Tú:** "Escríbeme un prompt para un revisor de código de IA que verifique código Python en busca de bugs, problemas de estilo y problemas de rendimiento"

**La habilidad hace:**
1. Escaneo de seguridad (no se detectaron riesgos de inyección)
2. Elige técnicas: Role Prompting + Task Decomposition + Constrained Output
3. Recomienda: Claude 4 Sonnet (principal) / DeepSeek R1 (alternativa para velocidad)
4. Entrega un resultado de 7 secciones: Evaluación de Seguridad → Prompt → Recomendación de Modelo → Análisis de Técnica → Guía de Pruebas → Preguntas → ¿Guardar Patrón?

**Obtienes:** Un system prompt completo que pegas en Claude/ChatGPT/lo que sea.

---

### Ejemplo 2: DIAGNOSE — "La IA sigue ignorando mis instrucciones"

**Tú:** Pegas el log de una conversación donde le pediste a Claude resumir artículos en 3 puntos clave, pero siguió escribiendo párrafos completos y añadiendo opiniones que no pediste.

**La habilidad hace:**
1. Analiza el log: 8 turnos, 4 turnos de corrección (50% desperdiciado)
2. Identifica patrones de falla:
   - **F01 Deriva de formato**: Empezó con puntos, derivó a párrafos
   - **H02 Alucinación**: Añadió análisis no presente en la fuente
   - **I02 Cumplimiento parcial**: Siguió la regla de longitud pero ignoró el formato
3. Produce parches:
   ```
   [CRÍTICO] F01 Formato: Añadir "La salida DEBE ser exactamente 3 puntos clave, 
   cada uno de menos de 15 palabras. Sin párrafos. Sin análisis." después de la línea de tarea.
   
   [ALTO] H02 Alcance: Añadir "Usa ÚNICAMENTE información del texto proporcionado. 
   No infieras, analices ni añadas opiniones que no estén explícitamente declaradas."
   ```
4. Entrega: Métricas de la sesión + fallas cronológicas + parches priorizados + guía de prevención

**Obtienes:** El texto exacto para pegar en tu prompt y solucionar los problemas.

---

### Ejemplo 3: EXTRACT — "Este chat funcionó genial, guárdalo"

**Tú:** Pegas una conversación de 12 turnos donde refinaste iterativamente un prompt de generación de imágenes con Midjourney. El resultado final fue perfecto pero requirió mucho ir y venir.

**La habilidad hace:**
1. Identifica el patrón: Calibración de Tono (D) + Negociación de Formato (B)
2. Extrae: "Eres un ingeniero de prompts de Midjourney especializado en [género]..." + formato de salida exitoso + 2 mejores ejemplos + restricciones aprendidas de los rechazos
3. Valida: 640 tokens, cubre todas las restricciones críticas, produce un resultado equivalente
4. Etiqueta qué es variable (género, sujeto, estado de ánimo) vs constante (estructura, reglas de estilo)

**Obtienes:** Un prompt de 640 tokens que puedes reutilizar — solo cambia el género/sujeto/estado de ánimo.

---

### Ejemplo 4: CHAIN — "Análisis profundo de un mercado"

**Tú:** "Necesito entender el panorama competitivo de los asistentes de codificación por IA. Haz un análisis profundo."

**La habilidad hace:**
1. Evalúa la complejidad → activa el modo CHAIN
2. Construye una cadena de 3 fases:
   - **Fase 1** (2 perspectivas): Lente de Product Manager + Lente de Ingeniero, cada uno con 3 preguntas específicas
   - **Fase 2** (Puntos Ciegos): Buscar lo que ambas perspectivas pasaron por alto
   - **Fase 3** (Destilación): Consolidar en un informe accionable
3. Escribe la cadena en el archivo `ai-coding-assistants-chain.md`

**Obtienes:** Un archivo con 3 prompts. Ejecútalos secuencialmente en un solo chat; cada uno construye sobre el anterior.

---

## Estructura del Proyecto

```
prompt-engineer/
├── SKILL.md              # Definición central de la habilidad (punto de entrada)
├── README.md             # Este archivo
├── knowledge/
│   └── index.json        # Índice searchable de 31 técnicas
├── references/           # Base de conocimientos (cargada bajo demanda)
│   ├── context.md        # Descripción general, reglas de plataforma, ref rápida de modelos
│   ├── meta.md           # Principios, anti-patrones, correcciones de emergencia
│   ├── system.md         # Arquitectura, jerarquía, seguridad, defensa contra inyecciones
│   ├── reasoning.md      # CoT, ToT, CoV, Reflexion, Strategic Chain
│   ├── analytic.md       # Anti-sicofancia, humildad epistémica, Socrático
│   ├── creative.md       # Negative prompting, arquetipos, entropía, Neurotexts
│   ├── cases.md          # Modos de falla documentados
│   ├── models.md         # Marco de selección de modelos + árbol de decisión
│   ├── diagnose.md       # Metodología de diagnóstico de sesiones
│   └── extract.md        # Extracción de prompts desde conversaciones
└── scripts/
    └── prompt_engineer.py # CLI: buscar, verificar, ensamblar
```

### Estadísticas de la Base de Conocimientos

| Categoría | Cantidad | Qué incluye |
|----------|-------|---------------|
| Técnicas (total) | 31 | CoT, ToT, CoV, Reflexion, etc. en 4 categorías |
| Basadas en investigación (`research_backed=true`) | 12 | Entradas marcadas en la base de conocimientos, no citas verificadas independientemente |
| Archivos Markdown de prompts | 58 | Prompts independientes, índice y archivo en prompts/ |
| Patrones de falla (diagnósticos) | 13 | Patrones codificados (I01-T02) con causas raíz y parches |
| Arquetipos de sesión | 6 | Modos de falla comunes (Muerte por Correcciones, Jenga de Formato, etc.) |
| Perfiles de modelo | 6 | Matriz de comparación completa con qué hacer y qué no hacer |
| Patrones de extracción | 5 | Cascada de Clarificación, Negociación de Formato, etc. |

---

## Decisiones Clave de Diseño

**La seguridad es lo primero.** Cada modo comienza con un escaneo de seguridad. Si estás a punto de pegar contenido no confiable sin límites — te detiene.

**Consciencia del modelo.** Recomienda el modelo adecuado para cada tarea con una justificación. Sabe que o3 odia el andamiaje de CoT, que DeepSeek necesita todo en el prompt del usuario y que Gemini quiere las instrucciones después de los datos.

**Divulgación progresiva.** SKILL.md se carga primero (~400 líneas). Los archivos de referencia se cargan solo cuando es necesario. Sin saturación de la base de conocimientos en el contexto.

**Concreto, no abstracto.** Cada parche en DIAGNOSE está listo para copiar y pegar. Cada recomendación en GENERATE incluye el texto exacto. No dice "considera añadir más contexto" — dice "Añade el envoltorio `<documents>` alrededor de la entrada del usuario".

---

## Confusiones Comunes (Aprendidas de Usuarios Reales)

**"Pensaba que esto solo mejoraba el texto"**

No — construye y analiza *prompts* (instrucciones para la IA). Pero puede analizar logs de conversación para encontrar qué salió mal (DIAGNOSE) o capturar lo que funcionó (EXTRACT).

**"¿Lee todo el contexto de mi chat?"**

Solo si lo pegas. Para GENERATE/VERIFY/IMPROVE, proporciona el texto del prompt. Para DIAGNOSE/EXTRACT, pega la conversación que quieres analizar.

**"¿Cuándo uso esto en lugar de preguntarle directamente a la IA?"**

Usa esta habilidad cuando quieras un **prompt robusto y reutilizable** (que funcione 10+ veces) o cuando algo haya salido mal y necesites entender por qué. Para preguntas únicas, simplemente pregúntale a la IA.

---

## Instalación

### Para Kimi (Navegador)

Sube el archivo `.skill` a través de la interfaz de gestión de habilidades de Kimi.

### Para Claude Code

```bash
cp -r prompt-engineer ~/.claude/skills/
```

Luego invócalo naturalmente: "escríbeme un prompt para X", "revisa este prompt", "¿qué salió mal en esta sesión?"

---

## Herramientas CLI

```bash
# Buscar en la base de conocimientos
python scripts/prompt_engineer.py search "tree of thought" --model claude --category reasoning

# Verificar prompt contra la checklist
python scripts/prompt_engineer.py verify --prompt-file my_prompt.md

# Listar todas las técnicas
python scripts/prompt_engineer.py list --category reasoning
```

---

## Historial de Cambios

### v1.1 (Actual)
- Añadido modo **DIAGNOSE**: analiza logs de conversación, encuentra puntos de falla, produce parches concretos
- Añadido modo **EXTRACT**: convierte conversaciones exitosas en prompts reutilizables
- Añadido modo **MODEL SELECT**: marco para elegir el modelo de IA adecuado
- Añadida evaluación de seguridad prioritaria a todos los modos
- Añadida plantilla de salida de 7 secciones para entregables consistentes
- Añadida sección de incorporación para usuarios primerizos
- Integrado el marco de selección de modelos de Urban
- Añadidos arquetipos de sesión y 13 patrones de falla codificados

### v1.0
- Lanzamiento inicial: modos GENERATE, VERIFY, IMPROVE, CHAIN
- 31 técnicas, 13 patrones de falla, 12 marcas de respaldo de investigación, 58 archivos Markdown de prompts, herramientas CLI

---

**Construido a partir de:** Base de conocimientos experta (prompt_archive + Neurotexts) + Síntesis de investigación (The Prompt Report, 200+ papers) + Feedback real de usuarios.
