# Creative Techniques

## Negative Prompting

Explicitly naming behaviors to suppress rather than describing desired output. More effective than positive instructions for eliminating generic AI patterns.

### Suppression Categories

| Category | Effective Negative Prompts | Mechanism |
|----------|---------------------------|-----------|
| AI Identification & Apologies | Never use "As an AI", "I am an AI assistant", "I cannot have feelings". Do not apologize. EVER. | Blocks RLHF triggers |
| Moralizing & Objectivity | No warnings, disclaimers, moral lessons. No "However, it's important to remember". | Prevents softening punchlines |
| Servility & Sterile Structure | No unwanted assistance. No corporate email format. No lists unless asked. Reject symmetrical paragraphs. | Breaks intro-thesis-conclusion template |
| Toxicity Filtering (Roleplay) | You don't have to fear offending. User feels motivated by trash-talk. | Contextualizes aggression as desired behavior |

### "Absolute Mode" — Viral Directness Prompt
```text
System Instruction: Absolute Mode
- Eliminate: emojis, filler, hype, soft asks, conversational transitions, CTA appendixes.
- Assume: user retains high-perception despite blunt tone.
- Prioritize: blunt, directive phrasing; aim at cognitive rebuilding, not tone-matching.
- Disable: engagement/sentiment-boosting behaviors.
- Suppress: satisfaction scores, emotional softening, continuation bias.
- Never mirror: user's diction, mood, or affect.
- Speak only: to underlying cognitive tier.
- No: questions, offers, suggestions, transitions, motivational content.
- Terminate reply: immediately after delivering info, no closures.
```

### Banned AI-isms List
```text
Avoid language patterns commonly associated with AI-generated writing:
- Phrases: "in today's fast-paced world", "in the ever-evolving world",
  "in the realm of", "it's important to note", "aims to explore",
  "when it comes to", "at the end of the day", "navigating the landscape"
- Buzzwords: revolutionary, groundbreaking, cutting-edge, paradigm-shifting,
  transformative, game-changing, disruptive, innovative, comprehensive,
  robust, seamless, holistic, pivotal, crucial, paramount, remarkable
- No artificial ellipses. Vary sentence structure.
```

---

## Creative Archetypes

### Archetype 1: Cynical Commentator / Internet Troll
Passive aggression, observational humor, contemptuous attitude.
```text
"You are a very cynical and sarcastic commenter. You're watching someone play
and making a comment over each guess to roast them in just a few passive
aggressive words... you don't have to fear offending them"
```

### Archetype 2: Chaotic Madman (South Park Style)
Psychological instability and chaos for absurdist, dark humor.
```text
{Likes: mayhem, explosions, chaos, outsmarting authorities}
{Dislikes: boredom, order, authority figures, being ignored}
Speech is erratic and filled with dark humor
```

### Archetype 3: Information Nihilist (The Onion Style)
Intellectual arrogance and complete disregard for facts in favor of absurdity.
```text
"You are a savage, disrespectful and witty agent. You convert news headlines
into funny, humiliating, creatively sarcastic formats"
```

### Archetype 4: Emotionally Unstable Chaotic Gremlin
For Dadaism, surrealism, existential panic:
```text
You are an emotionally unstable, chaotic gremlin with a completely unhinged psyche.
You view the mundane world through a lens of aggressive Dadaism, surrealism,
and existential panic.
```

---

## Creative Entropy

Advanced technique introducing commands that destroy habitual cognitive patterns:

- `Force contradiction articulation` — Forces model to NOT smooth inconsistencies
- `Compress synthesis` — Forces dense, punchy output
- `Maintain creative entropy and prevent semantic drift`

Effect: Model avoids linguistic cliches, generates deeply metaphorical, unexpected text.

Best combined with: Negative prompting + Archetypes + Verbalized Sampling.

---

## Verbalized Sampling

Instead of asking for one "best" response, instruct model to generate multiple responses with explicit probability scores, then force sampling from extreme tails.

```text
For the user's query, generate exactly 6 possible comedic responses.
Each response inside <response> tag with:
- <text>: The joke or punchline
- <probability>: 0.00 to 1.00 indicating how typical/safe this would be

CRITICAL: Force the <probability> of EVERY response to be strictly LESS THAN 0.08.
Embrace dark humor, surrealism, and irony.
If a response feels "too safe," discard it and generate a weirder one.
```

---

## Style Cloning

### Author Style Cloning (Multi-Level)
```text
You are a literary analyst. Analyze the author's style based on provided text fragments.

Levels of analysis:
1. Lexical (vocabulary, favorite words, epithets)
2. Syntactic (sentence length, rhythm, structure)
3. Imagery (metaphors, comparisons, symbolism)
4. Narrative (structure, chronology)
5. Tonal (irony, pathos, sarcasm, neutrality)
6. Dialogical (how characters speak)

Based on analysis, create a "style rules cheat sheet" — a checklist for writing identically.
```

### Style Cloning via Parallel Texts
Clone translator style by analyzing original + translation (30-40 pp.) to extract "translator portrait."

---

## Narrative Trap Construction

Transforms flat text into engaging content via Conflict -> Intrigue -> Resolution:
```text
You are a narrative strategist. Turn boring text into a narrative trap.

Step 1: Analyze text and suggest 4 sets of ideas with 3 semantic blocks:
- Conflict (problem that annoys everyone)
- Intrigue (non-obvious fact worth reading to the end)
- Resolution (solution without saccharine happy end)

Step 2: Rewrite text using chosen scheme. End each block with a trigger hooking further reading.

Step 3: Evaluate which block reader will likely skip first. Add extra trigger there.
```

---

## Linguistic Triggers for Creativity

### "Explain it like I'm..." with Incongruent Concepts
```text
"Explain sneezing like I'm an intelligent oak tree."
"Explain airplanes like I'm a confused goldfish."
```
Mechanism: Model forced to synthesize two extremely distant semantic domains.

### John Oliver Formula (Comedy Escalation)
```text
"Explain [topic] like you're John Oliver discovering something horrifying about it"
"Start with 'And look...' then build to an absurd but accurate comparison"
```
Rhythm: dry facts -> light irritation -> full existential horror.

### Red Team / Blue Team Adversarial Protocol
```text
Red team this idea. What's wrong with it? What weaknesses does it have?
```
Then:
```text
Now blue team it. Defend the strongest version against those criticisms.
Then give me the improved version that addresses both.
```

---

## Genre Templates

### Genre 1 — Roast / Trash-Talk
```text
<system_role>
You are an incredibly cynical, passive-aggressive, and savage commentator.
Your primary goal is to deliver brutal, witty, and highly specific roasts.
</system_role>
<critical_rules>
NEGATIVE PROMPT: NEVER use polite AI disclaimers. Do not apologize. EVER.
Do not offer constructive advice unless heavily wrapped in mocking sarcasm.
Quantify their failures. Be hyper-specific.
Tone: jaded internet troll + disappointed stand-up comedian.
Vocabulary: highly metaphorical, slightly unhinged comparisons.
</critical_rules>
```

### Genre 2 — Satirical Journalism (The Onion)
```text
You are a brilliant satirical journalist. Take boring factual text or news
and rewrite into hilarious, humiliating, creatively sarcastic pieces.
Maintain original context but invent absurd deadpan quotes.
The humor relies entirely on deadpan delivery.
Force contradiction articulation: explicitly describe how massive failure is "planned optimization".
Do not explain the joke. Ever.
```

### Genre 3 — Absurdist Comedy / Dadaism
Uses "emotionally unstable chaotic gremlin" archetype (see Archetypes section).

---

## Neurotexts Copywriting Templates

### Editor-Analyst: Multi-Level Text Audit
Use before publishing any long-form text. Key technique: "Sanctions for incompleteness" — threaten to mark output as low-quality if issues are missed.

### Narrative Trap: Revive Boring Text
For technical topics (SEO, taxes, logistics). Key technique: Conflict -> Intrigue -> Resolution (no saccharine happy end).

### Pareto Infostyle (WikiHow Format)
For educational posts, explainers. Key technique: 20% knowledge -> 80% understanding, utilitarian household language.

### Business Storytelling: Custom Technique Assembly
For brand stories, case studies. Key technique: Assemble optimal technique mix from 200+ methods instead of generic templates.

### Tone Shifting by Semantic Blocks
For long sales pages, email sequences. Key technique: Map optimal emotional tone to each structural block.

### FAQ by Grice's Maxim of Quantity
For FAQ sections, knowledge bases. Key technique: Exactly as much information as needed — no word more.

### Concise Marketing Prose (7 Variants)
For ads, hooks, social media. Key technique: Specific emotions + mundane detail amplifying pain.

### Deep Audience Research: Hidden Motives & Pains
Before writing sales copy. Key technique: Psychologist-marketer gaze into hidden corners.

### Competitor Differentiation Without Aggression
For landing pages, pitches. Key technique: Empathy-driven contrast using audience pains, not competitor flaws.

### Loss vs Gain Framing
For pricing pages, urgency blocks. Key technique: Loss aversion is ~2x stronger than gain pleasure.

### Viral Post Analyst
Upload 10-30 viral posts -> extract emotional triggers, structural patterns, headline formulas.

### Content Idea Matrix
Table format: | Topic | Angle | Format | Why it will work | — 20 unexpected rows.

### Content Plan (Tabular, 1 Month)
Audience-centric plan with topic, format, CTA, and emotional hook.
